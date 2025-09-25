import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="|".join(
        [
            "%(asctime)s",
            "%(module)s",
            "%(levelname)s",
            "%(message)s",
        ]
    ),
    level=logging.DEBUG,
)
