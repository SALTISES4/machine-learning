from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json


def add_routes(app: Sanic) -> Sanic:
    app.add_route(ping, "/ping", ["GET", "HEAD"])
    return app


async def ping(req: Request) -> HTTPResponse:
    return json({"msg": "Pong!"})
