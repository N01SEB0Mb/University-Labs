# coding=utf-8

from collections.abc import Iterable

import GraphExceptions


class AdjacencyListGraph(dict):
    class Vertex(int):
        """
        This is Vertex class of AdjacencyListGraph, base of Edge object
        """

        def __new__(cls, index: int):
            """
            Creates new Vertex object

            Args:
                index (int): Graph vertex index
            Raises:
                GraphTypeError: If index type is not int
            """

            if isinstance(index, int):
                return int.__new__(cls, index)
            else:
                raise GraphExceptions.GraphTypeError("invalid index type '{}', use 'int' instead".format(
                    iterable.__class__.__name__
                ))

        def __init__(self, index: int):
            """
            Inits Vertex object

            Args:
                index: Graph vertex index
            """

            super(AdjacencyListGraph.Vertex, self).__init__()

        def __repr__(self):
            """
            Overwrites __repr__ method

            Returns:
                str: Representation of Vertex object
            """

            return "Vertex[{}]".format(self)
