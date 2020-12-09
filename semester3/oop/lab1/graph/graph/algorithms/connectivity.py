# coding=utf-8

from graph.types import *
from .bfs import BFS


def isConnected(graph: GraphABC) -> bool:
    """
    Checks graph's connectivity

    Args:
        graph (GraphABC): Graph you want to check

    Returns:
        bool: Is graph connected
    """

    vertices = set(graph)
    part = BFS(graph, next(iter(vertices)))

    return set(graph) == part
