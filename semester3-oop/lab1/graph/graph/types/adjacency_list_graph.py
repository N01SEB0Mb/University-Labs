# coding=utf-8

from collections.abc import Iterable

import graph.exceptions


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
                raise graph.exceptions.GraphTypeError("invalid index type '{}', use 'int' instead".format(
                    iterable.__class__.__name__
                ))

        def __init__(self, index: int):
            """
            Inits Vertex object

            Args:
                index (int): Graph vertex index
            """

            super(AdjacencyListGraph.Vertex, self).__init__()

        def __repr__(self):
            """
            Overwrites __repr__ method

            Returns:
                str: Representation of Vertex object
            """

            return "Vertex[{}]".format(self)

    class Edge(Vertex):
        """
        This is Edge class of AdjacencyListGraph to be used in edge list
        It consists of Vertex object and edge properties
        """

        # def __new__(cls, vertex, weight: float = 1.0):
        #     """
        #     Creates new Edge object
        #
        #     Args:
        #         vertices (Iterable): Any iterable object consists of two Vertex objects
        #         weight (float, optional): Weight of the edge. Defaults to 1.0
        #
        #     Raises:
        #         TypeError: If vertices argument is not iterable
        #         PairError: If number of vertices is not 2
        #     """
        #
        #     new_edge = super(EdgeListGraph.Edge, cls).__new__(cls, vertex)
        #     if len(new_edge) != 2:
        #         raise graph.exceptions.PairError("too {} vertices specified, there should be 2 vertices".format(
        #             "few" if len(new_edge) < 2 else "much"
        #         ))
        #     else:
        #         return new_edge

        def __init__(self, vertex, weight: float = 1.0):
            """
            Inits Edge object

            Args:
                vertices (Iterable): Any iterable object consists of two Vertex objects
                weight (float, optional): Weight of the edge. Defaults to 1.0

            Raises:
                GraphTypeError: If vertex argument is not instance of Vertex class
            """

            super(AdjacencyListGraph.Vertex, self).__init__()
            print(self)

            try:
                self.weight = float(weight)
            except (TypeError, ValueError):
                raise graph.exceptions.GraphTypeError("'' is not valid type for weight value".format(
                    weight.__class__.__name__
                ))

            if not isinstance(self[0], EdgeListGraph.Vertex) or not isinstance(self[1], EdgeListGraph.Vertex):
                raise graph.exceptions.GraphTypeError("invalid vertex type '{}', use 'Vertex' instead".format(
                    self[0].__class__.__name__ if not isinstance(self[0],
                                                                 EdgeListGraph.Vertex) else self[1].__class__.__name__
                ))

            if self[0] == self[1]:
                warnings.warn("Connecting vertex to itself", graph.exceptions.GraphWarning)

        def __hash__(self):
            """
            Overwrited __hash__ method
            Is used to comparison in set

            Returns:
                int: object hash
            """

            return hash((self[0], self[1]) if self.directed else (min(self), max(self)))

        def __eq__(self, other):
            """
            Overwrites __eq__ method
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
