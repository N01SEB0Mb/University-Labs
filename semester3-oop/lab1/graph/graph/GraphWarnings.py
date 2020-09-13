# coding=utf-8
"""
This is warnings used in graph package
"""


class GraphWarning(Warning):
    """
    This is base graph warning
    """
    def __init__(self, *args, **kwargs):
        super(Warning, self).__init__(*args, **kwargs)


class LoopWarning(GraphWarning):
    """
    This warning appears when you connect vertex to itself
    """
    def __init__(self, *args, **kwargs):
        super(GraphWarning, self).__init__(*args, **kwargs)
