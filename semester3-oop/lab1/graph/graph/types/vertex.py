# coding=utf-8

import graph.exceptions


class Vertex(int):
    """
    This is Vertex class, base of graph
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
                index.__class__.__name__
            ))

    def __init__(self, index: int):
        """
        Inits Vertex object

        Args:
            index (int): Graph vertex index
        """

        super(Vertex, self).__init__()

    def __repr__(self):
        """
        Overloads __repr__ method

        Returns:
            str: Representation of Vertex object
        """

        return "Vertex[{}]".format(self)
