# coding=utf-8

import requests

from parser import CONFIG
from parser.funcs import init
from parser.server import app


if __name__ == "__main__":
    app.clients = init()

    app.run(
        host=CONFIG["server"]["host"],
        port=int(CONFIG["server"]["port"]),
        threaded=True
    )
