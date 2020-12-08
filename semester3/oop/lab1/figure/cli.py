# coding=utf-8

import sys
import json
from pathlib import Path
from typing import Union
import multiprocessing as mp

from figure import Figure, AxisFigure
from figure.expression import Expression, ExpressionError


def processArea(
        start: float,
        end: float,
        parts: int,
        targetFigure: Union[Figure, AxisFigure],
        resultQueue: mp.Queue
) -> None:
    """
    Area calculation for different processes

    Args:
        start (float): Start point
        end (float): End point
        parts (int): Number of area parts
        targetFigure (Union[Figure, AxisFigure]): Figure you calculate
        resultQueue (mp.Queue): Queue for putting result

    Notes:
        This function used in different processes, so it puts result in queue instead of returning it
    """

    resultQueue.put(targetFigure.area(
        start,
        end,
        parts=parts
    ))


# Load config
with (Path() / "config.json").open("rt") as configFile:
    CONFIG = json.load(configFile)


if __name__ == "__main__":
    # Set recursion limit
    sys.setrecursionlimit(CONFIG["maxRecursionLimit"])

    # Input first function
    while True:
        firstString = input("Type first expression: f(x) = ")

        try:
            first = Expression(firstString)
        except (ExpressionError, BaseException) as Error:
            print(f"Invalid expression given ({Error}), try again")
        else:
            break

    # Input second function
    while True:
        secondString = input("Type second expression (Or press <Enter> to create Axis Figure): g(x) = ")

        try:
            assert secondString
            second = Expression(secondString)
        except AssertionError:
            second = None
            break
        except (ExpressionError, BaseException) as Error:
            print(f"Invalid expression given ({Error}), try again")
        else:
            break

    # Get figure
    if second is None:
        figure = AxisFigure(first)
    else:
        figure = Figure(first, second)

    # Multiprocessing variables
    queue = mp.Queue()
    processes = []

    response = {}

    # Process user requests
    while True:
        try:
            # Set shape limit
            a, b = map(float, input("Type shape start and end x: ").split(" "))
            a, b = min(a, b), max(a, b)
        except BaseException:
            # If limits are invalid
            print("Invalid start and end values, try again")
        else:
            # Process for every part
            for part in range(CONFIG["processes"]):
                process = mp.Process(
                    target=processArea,
                    args=(
                        a + (b - a) * part / CONFIG["processes"],
                        a + (b - a) * (part + 1) / CONFIG["processes"],
                        CONFIG["parts"],
                        figure,
                        queue
                    )
                )
                processes.append(process)
                process.start()

            result = 0.0

            # Get results from process
            for _ in range(CONFIG["processes"]):
                result += queue.get()

            # Join processes
            for process in processes:
                process.join()

            print("Shape area =", result)
