import os
from typing import Any, Dict

import yaml

from .logger import init_logging, logger


def read_config(config_name: str) -> Dict[str, Any]:
    path = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "config",
        f"{config_name}-config.yml",
    )

    try:
        with open(path) as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        msg = (
            "There is no configuration file named "
            f"config/{config_name}-config.yml."
        )
        logger.error(msg)
        raise FileNotFoundError(msg) from e

    if config is None:
        msg = (
            f"The configuration file config/{config_name}-config.yml is empty."
        )
        logger.error(msg)
        raise ValueError(msg)

    try:
        init_logging(config["logging"])
    except KeyError as e:
        msg = (
            "The configuration for logging is missing from the config "
            f"file {config_name}-config.yml."
        )
        logger.error(msg)
        raise KeyError(msg) from e
    return config


def update_config(config_name: str, config: Dict[str, Any]) -> None:
    path = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "config",
        f"{config_name}-config.yml",
    )
    with open(path, "w") as f:
        yaml.safe_dump(config, f)
