# coding=utf-8
"""
This is exceptions used in graph package
"""


class GraphError(Exception):
    """
    This is base graph error
    """

    pass


class GraphTypeError(GraphError, TypeError):
    """
    This error occurs when there is a type mismatch in this package
    """

    pass

