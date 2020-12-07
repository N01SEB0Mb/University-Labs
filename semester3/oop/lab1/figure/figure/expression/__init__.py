# coding=utf-8
"""
This package defines objects and other to work with math function expressions
"""

from .number import Number
from .node import ExpressionNode
from .function import Expression
from .exceptions import ExpressionError


__all__ = [
    "Number",
    "Expression",
    "ExpressionNode",
    "ExpressionError"
]


__author__ = "Tiron Mykhailo"
__maintainer__ = "Tiron Mykhailo"
__email__ = "noisebombch@gmail.com"

__license__ = "WTFPL"
__version__ = "1.0.0"
__status__ = "Alpha"
