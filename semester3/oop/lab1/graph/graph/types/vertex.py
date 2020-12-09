# coding=utf-8

import graph.exceptions


class Vertex(int):
    """
    This is Vertex class, base of graph
    """

    __slots__ = []

    def __new__(cls, index: int) -> "Vertex":
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
                index.__class__.__name__
            ))

    def __init__(self, index: int) -> None:
        """
        Inits Vertex object

        Args:
            index (int): Graph vertex index
        """

        super(Vertex, self).__init__()
