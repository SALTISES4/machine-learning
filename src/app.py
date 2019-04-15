from sanic import Sanic

from .api import add_routes
from .config import read_config
from .logger import logger


def create_app(config_name: str) -> Sanic:
    app = Sanic("machine-learning")
    app.config.app = read_config(config_name)
    app = add_routes(app)
    return app


def run_server(config_name: str) -> Sanic:
    app = create_app(config_name)
    try:
        app.run(
            host=app.config.app["server"]["host"],
            port=app.config.app["server"]["port"],
            auto_reload=app.config.app["server"]["reload"],
        )
    except KeyError:
        msg = (
            "There are missing fields for the server configuration in "
            f"{config_name}-config.yml. An example can be found at "
            "config/dev-config.yml."
        )
        logger.error(msg)
        raise KeyError(msg)
