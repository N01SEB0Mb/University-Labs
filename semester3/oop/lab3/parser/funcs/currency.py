# coding=utf-8

import traceback
import multiprocessing as mp
from time import time
from functools import partial


def run(func, queue, client_name):
    start_time = time()

    try:
        result = func()
    except BaseException:
        result = {"error": traceback.format_exc()}

    queue.put([result, client_name, "%.3f s" % (time() - start_time)])


def search_currency(clients):
    queue = mp.Queue()
    processes = []
    response = {}

    for client in clients:
        process = mp.Process(target=run, args=(partial(client.get_currency), queue, client.name))
        processes.append(process)
        process.start()

    for _ in clients:
        result, client_name, client_time = queue.get()
        response[client_name] = result
        response[client_name]["site_time"] = client_time

    for process in processes:
        process.join()

    return response
