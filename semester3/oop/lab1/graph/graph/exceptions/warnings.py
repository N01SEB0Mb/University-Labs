# coding=utf-8
"""
This is warnings used in graph package
"""


class GraphWarning(Warning):
    """
    This is base graph warning
    """

    pass


class LoopWarning(GraphWarning):
    """
    This warning appears when you connect vertex to itself
    """

    pass
