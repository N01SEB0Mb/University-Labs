# coding=utf-8

import multiprocessing.dummy as mp
from time import time
from tabulate import tabulate
from typing import Optional, Iterable, List

from topauto_parser.types.clients import CLIENT_CLASSES, BaseClient


def run(
        clientClass: type,
        queue: mp.Queue
) -> None:
    """
    Runs initialization for client class. Used in separate processes

    Args:
        clientClass (type): Class of client you want to init
        queue (mp.Queue): Queue for saving result

    Notes:
        This function puts result in queue, instead of returning it
    """

    queue.put(clientClass())


def login(
        clientClasses: Iterable[type]
) -> List[BaseClient]:
    """
    Initialize clients

    Args:
        clientClasses (Iterable[type]): Set of client classes you want to initialize

    Returns:
        List[BaseClient]: Initialized clients

    Notes:
        Initializing is performed using multiprocessing
    """

    clientsList = list()

    startTime = time()

    queue = mp.Queue()
    processes = []

    for clientClass in clientClasses:
        process = mp.Process(
            target=run,
            args=(clientClass, queue)
        )
        processes.append(process)
        process.start()

    for _ in clientClasses:
        client = queue.get()
        clientsList.append(client)

    for process in processes:
        process.join()

    print(tabulate([{
        "Name": client.name,
        "Connected": client.connected,
        "Signed in": client.loggedIn,
        "Time": "%.3f s" % client.loginTime
    } for client in clientsList], headers="keys"))

    print("Total authorization time: %.3f s" % (time() - startTime))

    return clientsList
