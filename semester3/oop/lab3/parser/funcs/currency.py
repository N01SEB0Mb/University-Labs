# coding=utf-8

import traceback
import multiprocessing as mp
from time import time
from typing import Iterable
from functools import partial
from requests.exceptions import ReadTimeout, ConnectionError

from parser.types.clients import BaseClient
from parser.types.response import ResponseStatus, ResponseCurrency


def run(
        client: BaseClient,
        queue: mp.Queue
) -> None:
    """
    Get currency from specified client. Used in separate processes

    Args:
        client (BaseClient): Client from which you want to get currency
        queue (mp.Queue): Queue for saving result

    Notes:
        This function puts result in queue, instead of returning it
    """

    # Time measuring

    startTime = time()

    try:
        # Trying to search article
        result = client.currency()
    except (ReadTimeout, ConnectionError):
        # If timeout expired

        result = ResponseCurrency.List(
            status=ResponseStatus(
                ResponseStatus.TIMEOUT_EXPIRED
            )
        )
    except BaseException:
        # Other error

        result = ResponseCurrency.List(
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


def currency(
        clients: Iterable[BaseClient]
) -> dict:
    """
    Get currency from specified clients

    Args:
        clients (Iterable[BaseClient]): Get currency clients

    Returns:
        dict: Currency getting result

    Notes:
        Getting currency is performed using multiprocessing
    """

    queue = mp.Queue()
    processes = []

    response = {}

    for client in clients:
        process = mp.Process(
            target=run,
            args=(
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
