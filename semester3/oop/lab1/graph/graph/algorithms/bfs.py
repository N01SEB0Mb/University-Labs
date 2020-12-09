# coding=utf-8

from typing import Optional, Set

from graph.types import *


def BFS(graph: GraphABC, vertex: Vertex, used: Optional[Set[Vertex]] = None) -> Set[Vertex]:
    """
    BFS algorithm

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

    # Next vertices queue
    queue = [vertex]

    while queue:
        # Get vertex from queue
        vertex = queue.pop(0)

        # Iterate neighbours
        for found in graph[vertex]:
            # Check if found vertex is new
            if found not in used:
                used.add(found)
                queue.append(found)

    return used
