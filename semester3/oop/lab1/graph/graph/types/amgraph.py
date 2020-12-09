# coding=utf-8

from typing import Generator, List, Set

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

        self.__am: List[List[bool]] = [[]]

        super(AMGraph, self).__init__()

    def add(self, vertex: Vertex, connections: Iterable[Vertex]) -> None:
        # Check existence
        if vertex in self:
            raise graph.exceptions.GraphExistenceError("Vertex already exists")
        elif vertex > len(self.__am):
            raise graph.exceptions.GraphExistenceError("Could not add unordered vertex")

        # Set connections
        self.__am.append([
            vertex in connections for vertex in range(len(self.__am))
        ])

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

        return self.__al[start][end]

    def connect(self, start: Vertex, end: Vertex) -> None:
        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Add connections
        self.__al[start][end] = True
        self.__al[end][start] = True

    def disconnect(self, start: Vertex, end: Vertex) -> None:
        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Remove connections
        self.__al[start][end] = False
        self.__al[end][start] = False

    def __getitem__(self, vertex: Vertex) -> Generator[Vertex, None, None]:
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        for vertex, connected in enumerate(self.__al[vertex]):
            if connected:
                yield Vertex(vertex)

    def __contains__(self, vertex: Vertex) -> bool:
        return vertex < len(self.__am)
