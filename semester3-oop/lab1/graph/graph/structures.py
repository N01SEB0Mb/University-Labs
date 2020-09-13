# coding=utf-8

import sys
import warnings
from collections.abc import Iterable

import exceptions


class EdgeListGraph(set):
    class Vertex(int):
        """
        This is Vertex class of EdgeListGraph, base of Edge object
        """

        def __new__(cls, index: int):
            """
            Creates new Vertex object

            Args:
                index (int): Graph vertex index
            Raises:
                GraphTypeError: If number type is not int
            """

            if isinstance(index, int):
                return int.__new__(cls, index)
            else:
                raise exceptions.GraphTypeError("invalid index type '{}', use 'int' instead".format(
                    iterable.__class__.__name__
                ))

        def __init__(self, index: int):
            """
            Inits Vertex object

            Args:
                index: Graph vertex index
            """

            super(EdgeListGraph.Vertex, self).__init__()

        def __repr__(self):
            """
            Overwrites __repr__ method

            Returns:
                str: Representation of Vertex object
            """

            return "Vertex[{}]".format(self)

    class Edge(tuple):
        """
        This is Edge class of EdgeListGraph to be used in edge list
        It consists of two Vertex objects
        """

        def __new__(cls, vertices: Iterable, weight: float=1.0, directed: bool=False):
            """
            Creates new Edge object

            Args:
                vertices (Iterable): Any iterable object consists of two Vertex objects
                weight (float, optional): Weight of the edge. Defaults to 1.0
                directed(bool, optional): Is edge directed. Defaults to False

            Raises:
                TypeError: If vertices argument is not iterable
                PairError: If number of vertices is not 2
            """

            new_edge = super(EdgeListGraph.Edge, cls).__new__(cls, vertices)
            if len(new_edge) != 2:
                raise exceptions.PairError("too {} vertices specified, there should be 2 vertices".format(
                    "few" if len(new_edge) < 2 else "much"
                ))
            else:
                return new_edge

        def __init__(self, verices: Iterable, weight: float=1.0, directed: bool=False):
            """
            Inits Edge object

            Args:
                vertices (Iterable): Any iterable object consists of two Vertex objects
                weight (float, optional): Weight of the edge. Defaults to 1.0
                directed(bool, optional): Is edge directed. Defaults to False

            Raises:
                GraphTypeError: If vertices argument does not consists only of Vertex objects

            Warnings:
                GraphWarning: If connecting vertex to itself
            """

            try:
                self.weight = float(weight)
            except (TypeError, ValueError):
                raise exceptions.GraphTypeError("'' is not valid type for weight value".format(
                    weight.__class__.__name__
                ))

            self.directed = bool(directed)

            if not isinstance(self[0], EdgeListGraph.Vertex) or not isinstance(self[1], EdgeListGraph.Vertex):
                raise exceptions.GraphTypeError("invalid vertex type '{}', use 'Vertex' instead".format(
                    self[0].__class__.__name__ if not isinstance(self[0],
                                                                 EdgeListGraph.Vertex) else self[1].__class__.__name__
                ))

            if self[0] == self[1]:
                warnings.warn("Connecting vertex to itself", exceptions.GraphWarning)

        def __hash__(self):
            """
            Overwrited __hash__ method
            Is used to comparison in set

            Returns:
                int: object hash
            """

            return hash((self[0], self[1]) if self.directed else (min(self), max(self)))

        def __str__(self):
            """
            Overwrites __str__ method

            Returns:
                str: Edge object converted to string
            """
            return str(self[0]) + "--(" + str(self.weight) + (")--" if not self.directed else ")->") + str(self[1])

        def __repr__(self):
            """
            Overwrites __repr__ method

            Returns:
                str: Representation of Edge object
            """
            return repr(self[0]) + "--(" + str(self.weight) + (")--" if not self.directed else ")->") + repr(self[1])

    """
    This is Graph class implemented with edge list
    """

    def __init__(self, edge_list=None):
        """
        Inits Graph object

        Args:
            edge_list (Iterable): Any iterable object that consists of Edge objects

        Raises:
            TypeError: If edge_list is not iterable
            GraphTypeError: If edge_list does not consists only of Edge objects
        """

        super(set, self).__init__()

        if isinstance(edge_list, Iterable):
            for edge in edge_list:
                if isinstance(edge, EdgeListGraph.Edge):
                    self.add(edge)
                else:
                    raise exceptions.GraphTypeError("edge list should consists only of 'Edge' objects, not '{}'".format(
                        edge.__class__.__name__
                    ))
        else:
            raise exceptions.TypeError("'{}' object is not iterable".format(edge_list.__class__.__name__))

    def __str__(self):
        """
        Overwrites __str__ method

        Returns:
            str: Graph object converted to string
        """
        return "; ".join([str(edge) for edge in self])

    def __repr__(self):
        """
        Overwrites __repr__ method

        Returns:
            str: Representation of Graph object
        """
        return ", ".join([repr(edge) for edge in self])
