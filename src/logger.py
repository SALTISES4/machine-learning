import logging
import os
from typing import Any, Dict

logger = logging.getLogger("machine-learning")


def init_logging(config: Dict[str, Any]) -> None:
    os.makedirs(
        os.path.join(os.path.dirname(__file__), os.pardir, "logs"),
        exist_ok=True,
    )
    logging.config.dictConfig(config)
