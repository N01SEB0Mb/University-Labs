# coding=utf-8

from typing import Optional, List, Dict

from graph.types import *
from graph.exceptions import *


def Dijkstra(graph: GraphABC, start: Vertex, end: Vertex) -> float:
    """
    Dijkstra's algorithm

    Args:
        graph (GraphABC): Graph
        start (Vertex): Start vertex
        end (Vertex): End vertex

    Returns:
        float: Shortest path weight. If there are no path, returns None

    Raises:
        GraphExistenceError: If start or end vertex does not exist
    """

    # Get all vertices and add start to queue
    vertices: Dict[Vertex, Optional[float]] = {item: 0.0 if item == start else None for item in iter(graph)}
    queue: List[Vertex] = [start]
    used: Set[Vertex] = {start}

    # Check existence
    if start not in vertices or end not in vertices:
        raise GraphExistenceError("'start' or 'end' vertex does not exists")

    while queue:
        # Get vertex from queue
        vertex = queue.pop(0)
        used.add(vertex)

        # Iterate neighbours
        for found, weight in graph[vertex].items():
            if vertices[found] is None or vertices[vertex] + weight < vertices[found]:
                vertices[found] = vertices[vertex] + weight
                if found in used:
                    used.remove(found)

            if found not in used:
                queue.append(found)

    return vertices[end]
