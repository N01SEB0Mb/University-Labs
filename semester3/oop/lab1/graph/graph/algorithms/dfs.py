# coding=utf-8

from typing import Optional, Set

from graph.types import *


def DFS(graph: GraphABC, vertex: Vertex, used: Optional[Set[Vertex]] = None) -> Set[Vertex]:
    """
    DFS algorithm

    Args:
        graph (Graph): Graph
        vertex (Vertex): Start vertex
        used (Optional[Set[Vertex]]): Used vertices

    Returns:
        Set[Vertex]: Found vertices

    Notes:
        This is recursive function
    """

    # Init used vertices and add starting
    used: Set[Vertex] = used or set()
    used.add(vertex)

    for found in graph[vertex]:
        if found not in used:
            used |= DFS(graph, found, used)

    return used
