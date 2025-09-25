from enum import Enum, auto, unique
from typing import Any


class Strint(Enum):
    @property
    def value(self) -> Any:
        return str(self._value_)


@unique
class NodeID(Strint):
    checkpoint_id = auto()
    clip_text_pos_id = auto()
    clip_text_neg_id = auto()
    vae_id = auto()
    sampler_id = auto()
    vae_decode_id = auto()
    vae_encode_id = auto()
    empty_latent_id = auto()
    load_image_id = auto()
    save_image_id = auto()


@unique
class NodeClassType(Enum):
    CLIPTextEncode = auto()
    CheckpointLoaderSimple = auto()
    EmptyLatentImage = auto()
    KSampler = auto()
    LoadImage = auto()
    SaveImage = auto()
    VAEDecodeTiled = auto()
    VAEEncodeTiled = auto()
    VAELoader = auto()


NCT = NodeClassType
