# coding=utf-8

import traceback
import multiprocessing as mp
from time import time
from typing import Iterable
from functools import partial
from requests.exceptions import ReadTimeout, ConnectionError

from parser.types.clients import BaseClient
from parser.types.response import ResponseStatus, ResponseSearch


def run(
        article: str,
        client: BaseClient,
        queue: mp.Queue
) -> None:
    """
    Runs searching for target client with specified article. Used in separate processes

    Args:
        article (str): Article of item you want to find
        client (BaseClient): Client for searching item
        queue (mp.Queue): Queue for saving result

    Notes:
        This function puts result in queue, instead of returning it
    """

    # Time measuring

    startTime = time()

    try:
        # Trying to search article
        result = client.search(article)
    except (ReadTimeout, ConnectionError):
        # If timeout expired

        result = ResponseSearch.List(
            status=ResponseStatus(
                ResponseStatus.TIMEOUT_EXPIRED
            )
        )
    except BaseException:
        # Other error

        result = ResponseSearch.List(
            status=ResponseStatus(
                ResponseStatus.INTERNAL_ERROR,
                description=traceback.format_exc()
            )
        )

    # Put into queue

    queue.put([
        result,
        "%.3f s" % (time() - startTime),
        client
    ])


def search(
        article: str,
        clients: Iterable[BaseClient]
) -> dict:
    """
    Search specified article with given clients

    Args:
        article (str): Article of item you want to find
        clients (Iterable[BaseClient]): Searching clients

    Returns:
        dict: Searching results

    Notes:
        Searching is performed using multiprocessing
    """

    queue = mp.Queue()
    processes = []

    response = {}

    for client in clients:
        process = mp.Process(
            target=run,
            args=(
                article,
                client,
                queue
            )
        )
        processes.append(process)
        process.start()

    for _ in clients:
        result, searchingTime, client = queue.get()
        response[client.name] = result

    for process in processes:
        process.join()

    return response
