from __future__ import annotations

import io
import json
from datetime import datetime, timedelta
from pprint import pprint
from time import sleep
from typing import TYPE_CHECKING
from urllib.parse import urlencode, urljoin

from PIL import Image
from requests.exceptions import ConnectionError
from requests.models import Request, Response
from requests.sessions import Session
from websockets.sync.client import connect
from websockets.typing import Data

from ccc.components.models.config import Config
from ccc.components.models.enums import NodeID
from ccc.components.models.workflow import WorkflowState, WorkflowStatus
from ccc.config import app_config
from ccc.constants import DEFAULT_WORKFLOW_TIMEOUT
from ccc.utils.logger import logger

if TYPE_CHECKING:
    from typing import Callable, Generator, Iterator

    from PIL.ImageFile import ImageFile


class BaseEndpoint:
    config: Config
    session: Session

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or app_config()
        self.session = Session()

    def send(self, request: Request) -> Response | None:
        prepared_request = self.session.prepare_request(request)
        try:
            response = self.session.send(prepared_request)
        except ConnectionError as e:
            logger.info(e.request)
            logger.info(e.response)
            return None
        else:
            logger.info(response.status_code)
            logger.info(response.raw)
            return response

    def build(
        self,
        method: str = "GET",
        path: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict[str, str] | None = None,
    ) -> Request:
        full_url = urljoin(self.config.connection.uri_http, path)
        logger.info(full_url)
        if json:
            return Request(
                method,
                full_url,
                json=json,
            )

        return Request(
            method,
            full_url,
            data=data,
            params=params,
        )

    def build_and_send(self, *args, **kwargs) -> Response | None:
        return self.send(self.build(*args, **kwargs))

    def ws[CallbackReturn](
        self,
        url: str,
        callback: Callable[[Data], CallbackReturn],
        params: dict[str, str] | None = None,
        timeout: timedelta = DEFAULT_WORKFLOW_TIMEOUT,
    ) -> Generator[CallbackReturn, None, None]:
        recieved: Data

        if params:
            params_encoded: str = urlencode(params)
            url = "?".join([url, params_encoded])

        started: datetime = datetime.now()
        with connect(url) as connection:
            while recieved := connection.recv():
                if not recieved:
                    return None

                yield callback(recieved)

                if datetime.now() >= started + timeout:
                    logger.info(f"Waiting for workflow at url {url} timed out after {timeout}")
                    return None

                if self.config.connection.sleep:
                    sleep(self.config.connection.sleep)


class ComfyUI(BaseEndpoint):
    client_id: str
    prompt_id: str

    def __init__(
        self,
        client_id: str,
        prompt_id: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.prompt_id = prompt_id
        self.status()

    def status(self):
        return self.build_and_send(path="/system_stats")

    def prompt(
        self,
        prompt: dict,
    ) -> Response | None:
        data = {
            "prompt": prompt,
            "client_id": self.client_id,
            "prompt_id": self.prompt_id,
        }
        logger.info("prompt")
        # logger.info(data)
        pprint(data)

        return self.build_and_send(path="/prompt", json=data, method="POST")

    def history(self):
        return self.build_and_send(path=f"/history/{self.prompt_id}")

    def view(
        self,
        filename: str,
        subfolder: str,
        folder_type: str,
    ):
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type,
        }
        return self.build_and_send(path="view", params=params)

    def workflow_status(self) -> Iterator[WorkflowState]:
        for status in self.ws(
            url=self.config.connection.uri_ws,
            params={"client_id": self.client_id},
            callback=self._handle_ws,
        ):
            yield status

    def _handle_ws(self, recieved: Data) -> WorkflowState:
        message = json.loads(recieved)
        match message.get("type", "unknown"):
            case "executing":
                return WorkflowState(
                    complete=(
                        "data" in message
                        and message["data"]["node"] is None
                        and message["data"]["prompt_id"] == self.prompt_id
                    ),
                    status=WorkflowStatus.executing,
                )
            case "progress":
                # https://github.com/yushan777/comfyui-websockets-api-part1/blob/main/basic_workflow_websockets_api_1.py#L48-L52
                return WorkflowState(
                    complete=False,
                    progress=message["data"]["value"],
                    total=message["data"]["max"],
                    status=WorkflowStatus.progress,
                )
            case "status":
                queue_remaining = message["data"]["status"]["exec_info"]["queue_remaining"]
                return WorkflowState(
                    complete=True if queue_remaining == 0 else False,
                    status=WorkflowStatus.status,
                )
            case _:
                return WorkflowState()

    def image(self, output_node_id: NodeID) -> ImageFile | None:
        images: list[dict[str, str]] | None = self._images(output_node_id)
        if not images:
            return

        single_image: dict[str, str] = images.pop()
        image_response: Response | None = self.view(
            filename=single_image["filename"],
            subfolder=single_image["subfolder"],
            folder_type=single_image["type"],
        )

        if image_response:
            logger.info(image_response)
            return self._load_image(image_response.content)

        return None

    def _images(self, output_node_id: NodeID) -> list[dict[str, str]] | None:
        history = self.history()
        if not history:
            return None
        logger.debug("History...")
        logger.debug(history.json())
        outputs = history.json().get(self.prompt_id, {}).get("outputs", {})
        logger.debug("Outputs...")
        logger.debug(outputs)
        images: list[dict[str, str]] | None = outputs[output_node_id.value].get("images")
        logger.debug("Images...")
        logger.debug(images)
        return images

    def _load_image(self, image: bytes) -> ImageFile:
        return Image.open(io.BytesIO(image))
