# coding=utf-8

from warnings import warn
from typing import Generator, Iterable, Dict, Set

import graph.exceptions
from .vertex import Vertex
from .graph import GraphABC


class ALGraph(GraphABC):
    """
    Graph represented with adjacency list
    """

    __slots__ = ["__al"]

    def __init__(self) -> None:
        """
        Inits ALGraph
        """

        self.__al: Dict[Vertex, Set[Vertex]] = {}

        super(ALGraph, self).__init__()

    def add(self, vertex: Vertex, connections: Iterable[Vertex]) -> None:
        # Check existence
        if vertex in self:
            raise graph.exceptions.GraphExistenceError("Vertex already exists")

        # Add vertex
        self.__al[vertex] = set()

        # Add connections
        for connection in connections:
            if connection in self:
                # If connected vertex exists
                self.__al[vertex].add(connection)
                self.__al[connection].add(vertex)

            if connection == vertex and self.LOOP_WARN:
                # Loop warning
                warn(graph.exceptions.LoopWarning("Connecting vertex to itself"))

    def remove(self, vertex: Vertex):
        # Check existence
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        # Delete vertex
        self.__al.pop(vertex)

        # Delete all connections
        for connections in self.__al.values():
            if vertex in connections:
                try:
                    connections.remove(vertex)
                except KeyError:
                    # If connection does not exists
                    pass

    def connected(self, start: Vertex, end: Vertex) -> bool:
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        return end in self.__al[start]

    def connect(self, start: Vertex, end: Vertex) -> None:
        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Add connections
        self.__al[start].add(end)
        self.__al[end].add(start)

        # If connected to itself
        if start == end and self.LOOP_WARN:
            warn(graph.exceptions.LoopWarning("Connecting vertex to itself"))

    def disconnect(self, start: Vertex, end: Vertex) -> None:
        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Remove connections
        try:
            self.__al[start].remove(end)
            self.__al[end].remove(start)
        except KeyError:
            # If connections does not exist
            raise graph.exceptions.GraphExistenceError("Given vertices does not connected")

    def __iter__(self) -> Iterable[Vertex]:
        return iter(self.__al)

    def __getitem__(self, vertex: Vertex) -> Generator[Vertex, None, None]:
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        for connection in self.__al[vertex]:
            yield connection

    def __contains__(self, vertex: Vertex) -> bool:
        return vertex in self.__al
