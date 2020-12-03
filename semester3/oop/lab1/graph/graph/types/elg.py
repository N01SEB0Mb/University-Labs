# coding=utf-8
"""
EdgeListGraph and EdgeListGraph.Edge types
"""

import warnings
from collections.abc import Iterable

import graph.exceptions
from .vertex import Vertex


class EdgeListGraph(set):

    class Edge(tuple):
        """
        This is 'Edge' class of 'EdgeListGraph' to be used in edge list
        It consists of two 'Vertex' objects, weight of edge and is the edge directed or not

        Notes:
            if edge is directed, then direction is from the first vertex to second
        """

        def __new__(cls, vertex_from: Vertex, vertex_to: Vertex, weight: float=1.0, directed: bool=False):
            """
            Creates new Edge object

            Args:
                vertex_from (Vertex): Start vertex of edge
                vertex_to (Vertex): End vertex of edge
                weight (float, optional): Weight of the edge. Defaults to 1.0
                directed(bool, optional): Is edge directed. Defaults to False

            Raises:
                GraphTypeError: If vertices args is not 'Vertex' type
            """

            if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
                return super(EdgeListGraph.Edge, cls).__new__(cls, (vertex_from, vertex_to))
            else:
                vertex_type = vertex_to.__class__.__name__ if isinstance(vertex_from,
                                                                         Vertex) else vertex_from.__class__.__name__
                error_message = "'vertex_from' and 'vertex_to' must be 'Vertex' object, not {}"
                raise graph.exceptions.GraphTypeError(error_message.format(error_message.format(vertex_type)))

        def __init__(self, vertex_from: Vertex, vertex_to: Vertex, weight: float=1.0, directed: bool=False):
            """
            Inits Edge object

            Args:
                vertex_from (Vertex): Start vertex of edge
                vertex_to (Vertex): End vertex of edge
                weight (float, optional): Weight of the edge. Defaults to 1.0
                directed(bool, optional): Is edge directed. Defaults to False

            Raises:
                GraphTypeError: If 'weight' argument is not float/can`t be converted to float

            Warnings:
                LoopWarning: If connecting vertex to itself
            """

            try:
                self.weight = float(weight)
            except (TypeError, ValueError):
                raise graph.exceptions.GraphTypeError("'{}' is not valid type for weight value".format(
                    weight.__class__.__name__
                ))

            self.directed = bool(directed)

            if self[0] == self[1]:
                warnings.warn("Connecting vertex to itself", graph.exceptions.LoopWarning)

        def __hash__(self):
            """
            Overloads __hash__ method
            Is used to comparison in set

            Returns:
                int: object hash
            """

            return hash((self[0], self[1]) if self.directed else (min(self), max(self)))

        def __eq__(self, other):
            """
            Overloads __eq__ method
            Can be equal only to object of the same class

            Args:
                other (EdgeListGraph.Edge): object to compare with

            Returns:
                bool: is object equal to other
            """

            if not isinstance(other, EdgeListGraph.Edge):
                return False
            if self.directed:
                return self[0] == other[0] and self[1] == other[1]
            else:
                return (self[0] == other[0] and self[1] == other[1]) or (self[0] == other[1] and self[1] == other[0])

        def __str__(self):
            """
            Overloads __str__ method

            Returns:
                str: Edge object converted to string
            """

            return str(self[0]) + "--(" + str(self.weight) + (")--" if not self.directed else ")->") + str(self[1])

        def __repr__(self):
            """
            Overloads __repr__ method

            Returns:
                str: Representation of Edge object

            """

            return "Edge[{0}-{2}{1}, {3}]".format(repr(self[0]), repr(self[1]), ">" if self.directed else "-", self.weight)

    """
    This is Graph class implemented with edge list
    """

    def __init__(self, edge_list=None):
        """
        Inits Graph object

        Args:
            edge_list (Iterable): Any iterable object that consists of Edge objects

        Raises:
            GraphTypeError: If edge_list is not iterable
            GraphTypeError: If edge_list does not consists only of Edge objects
        """

        super(set, self).__init__()

        if edge_list is None:
            edge_list = []

        if isinstance(edge_list, Iterable):
            for edge in edge_list:
                if isinstance(edge, EdgeListGraph.Edge):
                    self.add(edge)
                else:
                    error_message = "edge list should consists only of 'Edge' objects, not '{}'"
                    raise graph.exceptions.GraphTypeError(error_message.format(edge.__class__.__name__))
        else:
            raise graph.exceptions.GraphTypeError("'{}' object is not iterable".format(edge_list.__class__.__name__))

    def __str__(self):
        """
        Overloads __str__ method

        Returns:
            str: Graph object converted to string
        """

        return ", ".join([str(edge) for edge in self])

    def __repr__(self):
        """
        Overloads __repr__ method

        Returns:
            str: Representation of Graph object
        """

        return "EdgeListGraph[{}]".format(", ".join([repr(edge) for edge in self]))
