# coding=utf-8

import time
import logging
import traceback
from pathlib import Path
from flask_api import status
from flask import Flask, request, current_app

from parser.funcs import search_article, search_brand, init, search_currency
from parser import CONFIG


app = Flask(__name__)
app.clients = list()

nextDay = int(time.strftime("%j"))
hour, minute = map(int, time.strftime("%H:%M").split(":"))
nextDay += int(CONFIG["autoAuth"]["hour"] * 60 + CONFIG["autoAuth"]["minute"] <= hour * 60 + minute)


if CONFIG["logging"]["enabled"]:
    loggingPath = Path(".").resolve() / CONFIG["logging"]["path"].format("server")
    loggingPath.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(loggingPath)),
            logging.StreamHandler()
        ]
    )


def get_parameters_list(parameters_str):
    parameters_list = list()
    if parameters_str:
        if parameters_str[0] == "[" and parameters_str[-1] == "]":
            parameter = ""
            for char in parameters_str[1:]:
                if char in (",", "]") and parameter:
                    parameters_list.append(parameter)
                    parameter = ""
                else:
                    parameter += char
    return parameters_list


@app.before_request
def relogin():
    global nextDay
    if int(time.strftime("%j")) == nextDay and CONFIG["autoAuth"]["enabled"]:
        hour, minute = map(int, time.strftime("%H:%M").split(":"))
        if CONFIG["autoAuth"]["hour"] * 60 + CONFIG["autoAuth"]["minute"] <= hour * 60 + minute:
            print("Time to login...")
            app.clients = init()
            nextDay += 1


@app.route("/parser/search", methods=["GET"])
def search_by_parameters():
    articles = get_parameters_list(request.args.get("article"))
    brands = get_parameters_list(request.args.get("brand"))
    clients_list = get_parameters_list(request.args.get("sites"))

    total_start_time = time.time()
    clients_time = {}

    if articles:
        try:
            response = []
            if not brands:
                for article in articles:
                    start_time = time.time()
                    response.append(search_article(
                        article,
                        list(filter(lambda client: client.name in clients_list or not clients_list, app.clients))
                    ))
            elif len(articles) == len(brands):
                for number in range(len(articles)):
                    start_time = time.time()
                    response.append(search_brand(
                        articles[number], brands[number],
                        list(filter(lambda client: client.name in clients_list or not clients_list, app.clients))
                    ))
            else:
                return {"message": str(articles) + str(brands)}, status.HTTP_400_BAD_REQUEST
            for client in response[-1].keys():
                try:
                    clients_time[client] += float(response[-1][client]["site_time"].replace(" s", ""))
                except KeyError:
                    clients_time[client] = float(response[-1][client]["site_time"].replace(" s", ""))
            response[-1]["item_time"] = "%.3f s" % (time.time() - start_time)
            for client in clients_time.keys():
                clients_time[client] = "%.3f s" % (clients_time[client] / len(articles))
        except BaseException:
            logging.error(traceback.format_exc())
            return {"message": "{}".format(traceback.format_exc())}, status.HTTP_400_BAD_REQUEST
        else:
            return {"message": "Ok", "response": response,
                    "total_time": "%.3f s" % (time.time() - total_start_time),
                    "average_time": clients_time}, status.HTTP_200_OK
    else:
        return {"message": "No articles were given"}, status.HTTP_400_BAD_REQUEST


@app.route("/parser/currency", methods=["GET"])
def get_currency():
    clients_list = get_parameters_list(request.args.get("sites"))

    total_start_time = time.time()

    response = search_currency(filter(lambda client: client.name in clients_list or not clients_list, app.clients))

    return {"message": "Ok", "response": response,
            "total_time": "%.3f s" % (time.time() - total_start_time)}, status.HTTP_200_OK


@app.route("/parser/config", methods=["GET"])
def get_config():
    return {"message": "Ok", "config": CONFIG}, status.HTTP_200_OK


@app.route("/parser/login", methods=["GET", "POST"])
def login():
    try:
        app.clients = init()
    except BaseException:
        logging.error(traceback.format_exc())
        return {"message": "{}".format(traceback.format_exc())}, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return {"message": "Ok"}, status.HTTP_200_OK


@app.route("/parser/test", methods=["GET"])
def test():
    return {"message": "Ok"}, status.HTTP_200_OK


@app.route('/parser/exit', methods=['POST'])
def shutdown():
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    shutdown_server()
    return 'Server shutting down...'
