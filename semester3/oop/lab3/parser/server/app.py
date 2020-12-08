# coding=utf-8

import time
import logging
import traceback
from flask_api import status

from .baseserver import ParserServer
from parser.funcs import login
from parser.server.blueprints import parserRoute, configRoute


app = ParserServer(__name__)
app.register_blueprint(parserRoute)
app.register_blueprint(configRoute)

# Auto auth time

nextDay = app.day + int(app.autoAuthHour * 60 + app.autoAuthMinute <= app.hour * 60 + app.minute)


@app.before_request
def autoAuth():
    global nextDay

    if app.autoAuth and nextDay == app.day:
        if app.autoAuthHour * 60 + app.autoAuthMinute <= app.hour * 60 + app.minute:
            print("Time to login...")

            try:
                app.clients = login()
            except BaseException:
                return {
                    "message": traceback.format_exc(),
                }, status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                nextDay += 1

                return {
                    "message": "Ok"
                }, status.HTTP_200_OK


@app.route("/parser/login", methods=["GET", "POST"])
def login():
    try:
        app.clients = login()
    except BaseException:
        return {
            "message": traceback.format_exc(),
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return {
            "message": "Ok"
        }, status.HTTP_200_OK


@app.route("/parser/test", methods=["GET"])
def test():
    return {
        "message": "Ok"
    }, status.HTTP_200_OK


@app.route("/parser/exit", methods=["POST"])
def shutdown():
    def shutdownServer():
        func = request.environ.get('werkzeug.server.shutdown')

        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        func()

    shutdownServer()

    return 'Server shutting down...'
