# coding=utf-8
"""
Package calculate provides 3 different solutions:
 - CalcFunc, function
 - CalcCall, callable object using __call__ method
 - CalcNew, class that simulates function using __new__ method
"""

from .func import CalcFunc
from .call import CalcCall
from .new import CalcNew

__author__ = "Tiron Mykhailo"
__version__ = "1.0.0"
__date__ = "31.10.2020"

__all__ = ["CalcFunc", "CalcCall", "CalcNew"]
