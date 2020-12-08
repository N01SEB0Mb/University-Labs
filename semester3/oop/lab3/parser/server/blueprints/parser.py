# coding=utf-8

import time
from flask_api import status
from flask import Blueprint, request

from topauto_parser.server.funcs import *
from topauto_parser.funcs import *
from topauto_parser.types.clients import CLIENT_CLASSES


parserRoute = Blueprint(
    "searching",
    __name__,
    url_prefix="/parser"
)


@parserRoute.route("/search", methods=["GET"])
def searchByParameters():
    articles = getParametersList(request.args.get("article"))
    brands = getParametersList(request.args.get("brand"))
    clients = getClients(
        getParametersList(
            request.args.get("sites")
        )
    )

    totalStartTime = time.perf_counter()

    response = []

    if articles and brands:  # Get info
        if not len(articles) == len(brands):
            return {"message": "Number of articles and brands does not match"}, status.HTTP_400_BAD_REQUEST

        for number in range(len(articles)):
            response.append(
                info(
                    articles[number],
                    brands[number],
                    clients
                )
            )
    elif articles:  # Search item
        for article in articles:
            response.append(
                search(
                    article,
                    clients
                )
            )
    else:
        return {"message": "No articles were given"}, status.HTTP_400_BAD_REQUEST

    return {
        "message": "Ok",
        "response": response,
        "totalTime": "%.3f s" % (time.perf_counter() - totalStartTime)
    }, status.HTTP_200_OK


@parserRoute.route("/currency")
def getCurrency():
    clients = getClients(
        getParametersList(
            request.args.get("sites")
        )
    )

    totalStartTime = time.perf_counter()

    response = currency(
        clients
    )

    return {
        "message": "Ok",
        "response": response,
        "totalTime": "%.3f s" % (time.perf_counter() - totalStartTime)
    }, status.HTTP_200_OK
