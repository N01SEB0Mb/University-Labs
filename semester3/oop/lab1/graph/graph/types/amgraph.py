# coding=utf-8

from warnings import warn
from typing import *

import graph.exceptions
from .vertex import Vertex
from .graph import GraphABC


class AMGraph(GraphABC):
    """
    Graph represented with adjacency list
    """

    __slots__ = ["__am"]

    def __init__(self) -> None:
        """
        Inits AMGraph
        """

        self.__am: List[List[float]] = []

        super(AMGraph, self).__init__()

    def add(self, vertex: Vertex, connections: Iterable[Tuple[Vertex, float]]) -> None:
        # Check existence
        if vertex in self:
            raise graph.exceptions.GraphExistenceError("Vertex already exists")
        elif vertex > len(self.__am):
            raise graph.exceptions.GraphExistenceError("Could not add unordered vertex")

        # Set connections
        self.__am.append(list())

        # Iterare every vertex connection
        for connection in range(vertex + 1):
            for connect, weight in connections:
                if connect == connection:
                    break
            else:
                weight = 0.0

            self.__am[vertex].append(weight)

            if connection != vertex:
                self.__am[connection].append(weight)
            else:
                # If connecting to itself
                if vertex in map(lambda item: item[0], connections) and self.LOOP_WARN:
                    warn(graph.exceptions.LoopWarning("Connecting vertex to itself"))

    def remove(self, vertex: Vertex):
        # Check existence
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        # Delete vertex
        self.__al.pop(vertex)

        # Delete connections
        for connection in self.__al:
            connection.pop(vertex)

    def connected(self, start: Vertex, end: Vertex) -> bool:
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        return bool(self.__al[start][end])

    def connect(self, start: Vertex, end: Vertex, weight: float = 1.0) -> None:
        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Add connections
        self.__al[start][end] = weight
        self.__al[end][start] = weight

        # If connected to itself
        if start == end and self.LOOP_WARN:
            warn(graph.exceptions.LoopWarning("Connecting vertex to itself"))

    def disconnect(self, start: Vertex, end: Vertex) -> None:
        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Remove connections
        self.__al[start][end] = 0.0
        self.__al[end][start] = 0.0

    def __iter__(self) -> Iterable[Vertex]:
        return iter([Vertex(vertex) for vertex in range(len(self.__am))])

    def __getitem__(self, vertex: Vertex) -> Generator[Vertex, None, None]:
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        for vertex, connected in enumerate(self.__am[vertex]):
            if connected:
                yield Vertex(vertex)

    def __contains__(self, vertex: Vertex) -> bool:
        return vertex < len(self.__am)
