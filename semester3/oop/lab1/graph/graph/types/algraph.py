# coding=utf-8

from warnings import warn
from typing import *

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

        self.__al: Dict[Vertex, Dict[Vertex, float]] = {}

        super(ALGraph, self).__init__()

    def add(self, vertex: Vertex, connections: Iterable[Tuple[Vertex, float]]) -> None:
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Vertices type must be 'Vertex', not {vertex.__class__.__name__}"
            )

        # Check existence
        if vertex in self:
            raise graph.exceptions.GraphExistenceError("Vertex already exists")

        # Add vertex
        self.__al[vertex] = {}

        # Add connections
        for connection, weight in connections:
            # Check vertex type
            if not isinstance(connection, Vertex):
                raise graph.exceptions.GraphTypeError(
                    f"Vertices type must be 'Vertex', not {vertex.__class__.__name__}"
                )

            if connection in self:
                # If connected vertex exists
                try:
                    self.__al[vertex][connection] = float(weight)
                    self.__al[connection][vertex] = float(weight)
                except ValueError:
                    # float(weight) error
                    raise graph.exceptions.GraphTypeError(
                        f"Connections weight type must be 'float', not {weight.__class__.__name__}"
                    )

            if connection == vertex and self.LOOP_WARN:
                # Loop warning
                warn(graph.exceptions.LoopWarning("Connecting vertex to itself"))

    def remove(self, vertex: Vertex):
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Vertices type must be 'Vertex', not {vertex.__class__.__name__}"
            )

        # Check existence
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        # Delete vertex
        self.__al.pop(vertex)

        # Delete all connections
        for connections in self.__al.values():
            if vertex in connections:
                connections.pop(vertex)

    def connected(self, start: Vertex, end: Vertex) -> bool:
        # Check type
        if not isinstance(start, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"'start' type must be 'Vertex', not {start__class__.__name__}"
            )
        elif not isinstance(end, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"'end' type must be 'Vertex', not {end.__class__.__name__}"
            )

        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        return end in self.__al[start]

    def connect(self, start: Vertex, end: Vertex, weight: float = 1.0) -> None:
        # Check type
        if not isinstance(start, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"'start' type must be 'Vertex', not {start__class__.__name__}"
            )
        elif not isinstance(end, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"'end' type must be 'Vertex', not {end.__class__.__name__}"
            )

        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Add connections
        try:
            self.__al[start][end] = float(weight)
            self.__al[end][start] = float(weight)
        except ValueError:
            # float(weight) error
            raise graph.exceptions.GraphTypeError(
                f"Connections weight type must be 'float', not {weight.__class__.__name__}"
            )

        # If connected to itself
        if start == end and self.LOOP_WARN:
            warn(graph.exceptions.LoopWarning("Connecting vertex to itself"))

    def disconnect(self, start: Vertex, end: Vertex) -> None:
        # Check type
        if not isinstance(start, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"'start' type must be 'Vertex', not {start__class__.__name__}"
            )
        elif not isinstance(end, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"'end' type must be 'Vertex', not {end.__class__.__name__}"
            )

        # Check existence
        if start not in self or end not in self:
            raise graph.exceptions.GraphExistenceError("Given vertices does not exists")

        # Remove connections
        try:
            self.__al[start].pop(end)
            self.__al[end].pop(start)
        except KeyError:
            # If connections does not exist
            raise graph.exceptions.GraphExistenceError("Given vertices does not connected")

    def __iter__(self) -> Iterable[Vertex]:
        return iter(self.__al)

    def __getitem__(self, vertex: Vertex) -> Dict[Vertex, float]:
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Key type must be 'Vertex', not {vertex.__class__.__name__}"
            )

        # Check existence
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        return self.__al[vertex]

    def __contains__(self, vertex: Vertex) -> bool:
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Vertex type must be 'Vertex', not {start__class__.__name__}"
            )

        return vertex in self.__al
