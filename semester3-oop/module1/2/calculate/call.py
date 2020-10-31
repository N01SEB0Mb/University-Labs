# coding=utf-8
"""
Task solution using class with __call__ method
"""

from .basecalc import CalculatorABC, CalculatorTypeError
from typing import Union, Iterable, Any


class CalcCall(CalculatorABC):
    """
    CalcCall class using __call__ method:
    You need to create CalcCall object, after you can call it like function
    """

    def __call__(self, x: Union[int, float, str, tuple, list, Any]) -> int:
        """
        CalcCall __call__ method override, used when calling object

        Args:
            x (int/float/str/tuple/list): given value

        Returns:
            int: calculation result

        Raises:
            IndexError: if 'x' argument is pair(tuple) and does not consists of 2 elements
        """

        for func in self._getFuncs():
            try:
                return func(x)
            except CalculatorTypeError:
                pass

    def _getFuncs(self):
        """
        Method to get list of calculating methods

        Returns:
            list: list of methods

        Notes:
            Order of methods in list is important, changing it may cause problems
        """

        return [
            self._string,
            self._pair,
            self._list,
            self._natural,
            self._integer,
            self._decimal,
            lambda value: 8941
        ]

    def _pair(self, value: tuple) -> int:
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
            return self.__call__(value[0]) * (self.__call__(value[1]) + 1) % 541
        else:
            raise CalculatorTypeError("pair")

    def _list(self, value: list) -> int:
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
            return sum(map(self.__call__, value)) % 741
        else:
            raise CalculatorTypeError("list")
