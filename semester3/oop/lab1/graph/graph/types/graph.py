# coding=utf-8

from typing import Iterable
from abc import ABC, abstractmethod

import graph.exceptions
from .vertex import Vertex


class GraphABC(ABC):
    """
    Abstract base class of graph
    """

    __slots__ = []

    @abstractmethod
    def add(self, vertex: Vertex, connections: Iterable[Vertex]) -> None:
        """
        Adds vertex to graph.

        Args:
            vertex (Vertex): Vertex you want to add
            connections (Iterable[Vertex]): Vertex connections

        Raises:
            GraphTypeError: If there are type mismatch
            GraphExistenceError: If you trying to add vertex that already exists
            GraphExistenceError: If you trying to connect non-existent vertices
        """

        pass

    @abstractmethod
    def remove(self, vertex: Vertex) -> None:
        """
        Remove vertex from graph.

        Args:
            vertex (Union[Vertex, int]): Vertex or index of vertex you want to remove

        Raises:
            GraphTypeError: If there are type mismatch
            GraphExistenceError: If vertex does not exists
        """

        pass

    @abstractmethod
    def connected(self, start: Vertex, end: Vertex) -> None:
        """
        Connects 2 vertices

        Args:
            start (Vertex): Start vertex
            end (Vertex): End vertex

        Raises:
            GraphTypeError: If there are type mismatch
            GraphExistenceError: If vertex does not exists
        """

        pass

    @abstractmethod
    def disconnect(self, start: Vertex, end: Vertex) -> None:
        """
        Disconnects 2 vertices

        Args:
            start (Vertex): Start vertex
            end (Vertex): End vertex

        Raises:
            GraphTypeError: If there are type mismatch
            GraphExistenceError: If vertex does not exists
        """

        pass

    @abstractmethod
    def __contains__(self, vertex: Vertex) -> bool:
        """
        Check if vertex exists

        Args:
            vertex (Vertex): Vertex you want to check

        Returns:
            bool: Does the vertex exists

        Raises:
            GraphTypeError: If vertex argument type is not 'Vertex'
        """

        pass
