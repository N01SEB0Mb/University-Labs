# coding=utf-8
"""
Task solution using function
"""

from math import factorial, sin
from typing import List, Tuple, Union, Any


def CalcFunc(x: Union[int, float, str, list, tuple, Any]) -> int:
    """
    Function f(x) from the task that calculates value depending on argument type

    Function using dict instead of if/else/elif construction,
    where key is a lambda with condition,
    and value is a lambda with result

    Args:
        x (int/float/str/List[float]/Tuple[float]/Any): given value

    Returns:
        int: result

    Raises:
        IndexError: if 'x' argument is pair(tuple) and not consists of 2 elements

    Notes:
        Funcs dict values is lambdas, so expressions calculates only when lambda is called
    """

    funcs = {
        lambda value: isinstance(value, str):  # Is string
            lambda: len([char for char in x if char.isalpha() and char.isupper()]),
        lambda value: isinstance(value, tuple):  # Is pair
            lambda: CalcFunc(x[0]) * (CalcFunc(x[1]) + 1) % 541,
        lambda value: isinstance(value, list):  # Is list
            lambda: sum(map(CalcFunc, x)) % 741,
        lambda value: (isinstance(value, int) or isinstance(value, float)) and abs(int(value)) == value:  # Is natural
            lambda: (factorial(x) + x - 1) % 141,
        lambda value: isinstance(value, int) or isinstance(value, float) and int(value) == value:  # Is integer
            lambda: x ** 3 % 241,
        lambda value: isinstance(value, float):  # Is decimal
            lambda: int(1 / sin(77 * x)) % 341,
        lambda value: True:  # Other values
            lambda: 8941
    }

    for key in funcs.keys():
        if key(x):
            return funcs[key]()
