# coding=utf-8

from typing import Optional, List, Dict, Set

from graph.types import *
from graph.exceptions import *


def MST(graph: GraphABC) -> GraphABC:
    """
    Minimal spanning tree (Kruskal's algorithm)

    Args:
        graph (GraphABC): Graph

    Returns:
        GraphABC: MST
    """

    # Save edges
    edges: Dict[Tuple[Vertex, Vertex], float] = dict()

    for vertex in graph:
        for found, weight in graph[vertex].items():
            if not (found, vertex) in edges:
                edges[(vertex, found)] = weight

    # Sort edges
    edges: Dict[Tuple[Vertex, Vertex], float] = {
        edge: weight for edge, weight in sorted(edges.items(), key=lambda edge: edge[1])
    }
    used: Set[Vertex] = set()

    # Create new graph
    mstGraph: GraphABC = graph.__class__()

    # Add vertices
    for vertex in graph:
        mstGraph.add(vertex, [])

    # Iterate edges
    for edge, weight in edges.items():
        start, end = edge

        # Check cycle
        if start not in used or end not in used:
            # Connect
            mstGraph.connect(start, end, weight)
            # Add vertices
            used.add(start)
            used.add(end)

    return mstGraph
