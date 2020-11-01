# coding=utf-8
"""
Task solution using class with __new__ method
"""

from .basecalc import CalculatorABC, CalculatorTypeError
from typing import Union, Iterable, Any


class CalcNew(CalculatorABC):
    """
    CalcNew class that simulates function:
    when class is called __new__ method must return new CalcNew object,
    but it returning calculation answer.
    You can call this class like function
    """

    def __new__(cls, x: Union[int, float, str, tuple, list, Any]) -> int:
        """
        CalcNew __new__ method override, uset to create new objects

        Args:
            x (int/float/str/tuple/list): given value

        Returns:
            int: result

        Raises:
            IndexError: if 'x' is pair(tuple) and it does not consists of 2 elements
        """

        for func in cls._getFuncs():
            try:
                print(func)
                return func(x)
            except CalculatorTypeError:
                pass

    @classmethod
    def _getFuncs(cls) -> List[Callable[[Union[int, float, str, tuple, list, Any]], int]]:
        """
        Method to get list of calculating methods

        Returns:
            list: list of methods

        Notes:
            Order of methods in list is important, changing it may cause problems
        """

        return [
            cls._string,
            cls._pair,
            cls._list,
            cls._natural,
            cls._integer,
            cls._decimal,
            lambda value: 8941
        ]

    @classmethod
    def _pair(cls, value: tuple) -> int:
        """
        Method for calculating result for pairs (tuples with 2 elements*)

        Args:
            value (tuple): tuple with 2 values

        Returns:
            int: result of task function

        Raises:
            CalculatorTypeError: if 'value' argument is not tuple
            IndexError: if 'value' tuple does not consists of 2 elements*

        Notes:
            *Tuple could consists of 3+ elements, but only 1-st and 2-nd element would be used
        """

        if isinstance(value, tuple):
            return cls(value[0]) * (cls(value[1]) + 1) % 541
        else:
            raise CalculatorTypeError("pair")

    @classmethod
    def _list(cls, value: list) -> int:
        """
        Method for calculating result for lists

        Args:
            value (list): list argument

        Returns:
            int: result of task function

        Raises:
            CalculatorTypeError: if 'value' argument is not list
        """

        if isinstance(value, list):
            return sum(map(cls, value)) % 741
        else:
            raise CalculatorTypeError("list")
