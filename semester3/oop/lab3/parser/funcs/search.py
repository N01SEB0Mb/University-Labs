# coding=utf-8

import traceback
import multiprocessing as mp
import requests.exceptions
from time import time
from functools import partial

from parser import CONFIG


def run(func, queue, client_name):
    start_time = time()

    try:
        result = func()
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        result = {"code": CONFIG["codes"]["connectionError"],
                  "message": "Время ожидания истекло"}
    except BaseException:
        result = {"code": CONFIG["codes"]["pythonError"],
                  "message": traceback.format_exc()}

    queue.put([result, client_name, "%.3f s" % (time() - start_time)])


def search_article(article, clients):
    queue = mp.Queue()
    processes = []
    response = {}

    for client in clients:
        process = mp.Process(target=run, args=(partial(client.search, article), queue, client.name))
        processes.append(process)
        process.start()

    for _ in clients:
        result, site_name, site_time = queue.get()
        response[site_name] = result
        response[site_name]["site_time"] = site_time

    for process in processes:
        process.join()

    return response


def search_brand(article, brand, clients):
    queue = mp.Queue()
    processes = []
    response = {}

    for client in clients:
        process = mp.Process(target=run, args=(partial(client.get_info, article, brand), queue, client.name))
        processes.append(process)
        process.start()

    for _ in clients:
        result, site_name, site_time = queue.get()
        response[site_name] = result
        response[site_name]["site_time"] = site_time

    for process in processes:
        process.join()

    return response
