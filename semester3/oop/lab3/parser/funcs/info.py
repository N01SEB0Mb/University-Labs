# coding=utf-8

import traceback
import multiprocessing as mp
from time import time
from typing import Iterable
from functools import partial
from requests.exceptions import ReadTimeout, ConnectionError

from parser.types.clients import BaseClient
from parser.types.response import ResponseStatus, ResponseInfo


def run(
        article: str,
        brand: str,
        client: BaseClient,
        queue: mp.Queue
) -> None:
    """
    Runs searching for target client with specified article. Used in separate processes

    Args:
        article (str): Article of item you want to find
        brand (str): Brand of item you want to find
        client (BaseClient): Client for searching item
        queue (mp.Queue): Queue for saving result

    Notes:
        This function puts result in queue, instead of returning it
    """

    # Time measuring

    startTime = time()

    try:
        # Trying to search article
        result = client.info(article, brand)
    except (ReadTimeout, ConnectionError):
        # If timeout expired

        result = ResponseInfo.Item(
            status=ResponseStatus(
                ResponseStatus.TIMEOUT_EXPIRED
            )
        )
    except BaseException:
        # Other error

        result = ResponseInfo.Item(
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


def info(
        article: str,
        brand: str,
        clients: Iterable[BaseClient]
) -> dict:
    """
    Get info about item with specified article and brand from given clients

    Args:
        article (str): Article of item you want to find
        brand (str): Brand of item you want to find
        clients (Iterable[BaseClient]): Getting info clients

    Returns:
        dict: Searching results

    Notes:
        Getting info is performed using multiprocessing
    """

    queue = mp.Queue()
    processes = []

    response = {}

    for client in clients:
        process = mp.Process(
            target=run,
            args=(
                article,
                brand,
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
