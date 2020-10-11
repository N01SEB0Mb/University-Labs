# coding=utf-8
"""
AdjacencyListGraph type
"""

from collections.abc import Iterable

import graph.exceptions
from .vertex import Vertex


class AdjacencyListGraph(dict):
    class Edge:
        """
        This is Edge class of AdjacencyListGraph to be used in adjacency list
        It consists of 'Vertex' object, weight of edge and is the edge directed or not

        Notes:
            if edge is directed, then direction towards containing vertex
        """

        def __init__(self, vertex, weight: float=1.0, directed: bool=False):
            """
            Inits Edge object

            Args:
                vertices (Iterable): Any iterable object consists of two Vertex objects
                weight (float, optional): Weight of the edge. Defaults to 1.0
                directed (bool, optional): Is edge directed. Defaults to False

            Raises:
                GraphTypeError: If 'vertex' argument is not instance of Vertex class
                GraphTypeError: If 'weight' argument is not float/can`t be converted to float
            """

            if isinstance(vertex, AdjacencyListGraph.Vertex):
                self.vertex = vertex
            else:
                raise graph.exceptions.GraphTypeError("'' is not valid type for vertex, use 'Vertex' instead".format(
                    vertex.__class__.__name__
                ))

            try:
                self.weight = float(weight)
            except (TypeError, ValueError):
                raise graph.exceptions.GraphTypeError("'{}' is not valid type for weight value".format(
                    weight.__class__.__name__
                ))

            self.directed = bool(directed)

        def __str__(self):
            """
            Overloads __str__ method

            Returns:
                str: Edge object converted to string
            """

            return "({0})-{1}{2}".format(self.weight, ">" if self.directed else "-", self.vertex)

        def __repr__(self):
            """
            Overloads __repr__ method

            Returns:
                str: representation of Edge object
            """

            return "Edge[-{1}{0}, {2}]".format(repr(self.vertex), ">" if self.directed else "-", self.weight)

    """
    This is Graph class implemented with adjacency list
    """

    def __init__(self, adjacency_list=None):
        super(dict, self).__init__()

        if adjacency_list is None:
            adjacency_list = dict()

        if isinstance(adjacency_list, dict):
            for vertex, edges in adjacency_list:
                if isinstance(vertex, Vertex):
                    if isinstance(edges, Iterable):
                        for edge in edges:
                            if not isinstance(edge, edges):
                                raise graph.exceptions.GraphTypeError("adjacency_list should be dict with"
                                                                      "iterable values consists of 'Edge' objects,"
                                                                      "not '{}'".format(edge.__class__.__name__))
                        self[vertex] = edges
                    else:
                        raise graph.exceptions.GraphTypeError("adjacency_list should be dict with iterable values,"
                                                              "not '{}'".format(edges.__class__.__name__))
                else:
                    raise graph.exceptions.GraphTypeError("adjacency_list should be dict with keys only of"
                                                          "'Vertex' type, not {}".format(vertex.__class__.__name__))
        else:
            raise graph.exceptions.GraphTypeError("adjacency_list type should be 'dict',"
                                                  "not '{}'".format(adjacency_list.__class__.__name__))

    def __str__(self):
        """
        Overloads __str__ method

        Returns:
            str: Graph object converted to string
        """

        return ""

    def __repr__(self):
        return ""