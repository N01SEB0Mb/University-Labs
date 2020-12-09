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
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Vertices type must be 'Vertex', not {vertex.__class__.__name__}"
            )

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
                try:
                    weight = float(weight)
                except ValueError:
                    # float(weight) error
                    raise graph.exceptions.GraphTypeError(
                        f"Connections weight type must be 'float', not {weight.__class__.__name__}"
                    )

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
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Vertices type must be 'Vertex', not {vertex.__class__.__name__}"
            )

        # Check existence
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        # Delete vertex
        self.__am.pop(vertex)

        # Delete connections
        for connection in self.__am:
            connection.pop(vertex)

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

        return bool(self.__am[start][end])

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
            self.__am[start][end] = float(weight)
            self.__am[end][start] = float(weight)
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
        self.__am[start][end] = 0.0
        self.__am[end][start] = 0.0

    def __iter__(self) -> Iterable[Vertex]:
        return iter([Vertex(vertex) for vertex in range(len(self.__am))])

    def __getitem__(self, vertex: Vertex) -> Dict[Vertex, float]:
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Key type must be 'Vertex', not {start__class__.__name__}"
            )

        # Check existence
        if vertex not in self:
            raise graph.exceptions.GraphExistenceError("Vertex does not exists")

        return {Vertex(connection): weight for connection, weight in enumerate(self.__am[vertex]) if weight}

    def __contains__(self, vertex: Vertex) -> bool:
        # Check type
        if not isinstance(vertex, Vertex):
            raise graph.exceptions.GraphTypeError(
                f"Vertex type must be 'Vertex', not {start__class__.__name__}"
            )

        return vertex < len(self.__am)
