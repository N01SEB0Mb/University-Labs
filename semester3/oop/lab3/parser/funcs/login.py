# coding=utf-8

import multiprocessing as mp
from time import time
from tabulate import tabulate

from parser.client import CLIENT_CLASSES


def run(client_class, queue):
    queue.put(client_class())


def init(clientsSet=None):
    client_classes = clientsSet or CLIENT_CLASSES
    clients = list()

    start_time = time()

    queue = mp.Queue()
    processes = []

    for client_class in client_classes:
        process = mp.Process(target=run, args=(client_class, queue))
        processes.append(process)
        process.start()

    for _ in client_classes:
        client = queue.get()
        clients.append(client)

    for process in processes:
        process.join()

    print(tabulate([{
        "Name": client.name,
        "Connected": client.connected,
        "Signed in": client.logged,
        "Time": client.login_time
    } for client in clients], headers="keys"))

    print("Total authorization time: %.3f s" % (time() - start_time))

    return clients
