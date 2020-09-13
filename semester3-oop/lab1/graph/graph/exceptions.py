# coding=utf-8
"""
This is exceptions used in graph package
"""


class GraphError(Exception):
    """
    This is base graph error
    """
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)


class GraphWarning(Warning):
    """
    This is base graph warning
    """
    def __init__(self, *args, **kwargs):
        super(Warning, self).__init__(*args, **kwargs)


class GraphTypeError(GraphError, TypeError):
    """
    This error occurs when there is a type mismatch in this package
    """


class PairError(GraphError):
    """
    This error occurs when an edge is attempted to initialize with wrong number of vertices
    """
    def __init__(self, message):
        super(GraphError, self).__init__(message)