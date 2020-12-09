# coding=utf-8

from typing import List, Set

from graph.types import *


def BFS(graph: GraphABC, vertex: Vertex) -> Set[Vertex]:
    """
    BFS algorithm

    Args:
        graph (Graph): Graph
        vertex (Vertex): Start vertex

    Returns:
        Set[Vertex]: Found vertices
    """

    # Add start vertex to used and queue
    used: Set[Vertex] = {vertex}
    queue: List[Vertex] = [vertex]

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
