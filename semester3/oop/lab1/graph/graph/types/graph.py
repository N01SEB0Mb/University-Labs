# coding=utf-8

from abc import ABC, abstractmethod
from typing import Iterable, Dict, Tuple

import graph.exceptions
from .vertex import Vertex


class GraphABC(ABC):
    """
    Abstract base class of graph

    Attributes:
        LOOP_WARN (bool): Enable or disable LoopWarning
    """

    LOOP_WARN: bool = True

    __slots__ = []

    @abstractmethod
    def add(self, vertex: Vertex, connections: Iterable[Tuple[Vertex, float]]) -> None:
        """
        Adds vertex to graph.

        Args:
            vertex (Vertex): Vertex you want to add
            connections (Iterable[Vertex]): Vertex connections

        Raises:
            GraphTypeError: If there are type mismatch
            GraphExistenceError: If you trying to add vertex that already exists
            GraphExistenceError: If you trying to connect non-existent vertices

        Warnings:
            LoopWarning: If you trying to connect vertex to itself
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
    def connected(self, start: Vertex, end: Vertex) -> bool:
        """
        Checks if vertices are connected

        Args:
            start (Vertex): Start vertex
            end (Vertex): End vertex

        Returns:
            bool: Does vertices connected
        """

        pass

    @abstractmethod
    def connect(self, start: Vertex, end: Vertex, weight: float = 1.0) -> None:
        """
        Connects 2 vertices

        Args:
            start (Vertex): Start vertex
            end (Vertex): End vertex
            weight (Vertex): Edge weight

        Raises:
            GraphTypeError: If there are type mismatch
            GraphExistenceError: If vertex does not exists

        Warnings:
            LoopWarning: If you trying to connect vertex to itself
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
    def __iter__(self) -> Iterable[Vertex]:
        """
        Get iterator with vertices

        Returns:
            Iterable[Vertex]: Graph vertices
        """

        pass

    @abstractmethod
    def __getitem__(self, vertex: Vertex) -> Dict[Vertex, float]:
        """
        Get vertex connections

        Args:
            vertex (Vertex): Vertex, connections of which you want to get

        Returns:
            Dict[Vertex, float]: Connected vertices dict

        Raises:
            GraphExistenceError: If vertex does not exists
        """

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

    def __str__(self) -> str:
        """
        Convertion to str

        Returns:
            str: Graph converted to str (<vertex>: <connected vertices>)
        """

        return "\n".join(
            map(
                lambda vertex: f"{vertex}: " + " ".join(map(
                    str,
                    self.__getitem__(vertex))
                ),
                self.__iter__()
            )
        )
