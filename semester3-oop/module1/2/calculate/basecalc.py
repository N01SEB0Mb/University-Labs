# coding=utf-8
"""
Abstract class for CalcCall and CalcNew solutions
"""

from math import sin, factorial
from typing import Tuple, List, Optional, Callable, Union, Any


class CalculatorTypeError(TypeError):
    """
    Calculator type error, used in CalculatorABC calculation methods
    """

    def __init__(self, argtype: str, msg: Optional[str] = "'value' argument must be {}") -> None:
        """
        CalculatorTypeError __init__ method override
        Initializes CalculatorTypeError object

        Args:
            argtype (str): correct type of argument
            msg (Optional[str]): error message
        """

        super(CalculatorTypeError, self).__init__(msg.format(argtype))


class CalculatorABC:
    """
    Calculator abstract base class, inherits in CalcCall and CalcNew colution
    Contains methods for every type calculation

    Notes:
        Does not have calculation for pairs and lists because of recursion
        that is different in CalcCall and CalcNew classes, so they define it by self
    """

    @classmethod
    def _getFuncs(cls) -> List[Callable[[Union[int, float, str, tuple, list, Any]], int]]:
        """
        Method to get list of calculating methods.

        Overriden in both CalcCall and CalcNew classes,
        because CalcNew has no object instance but CalcCall has,
        so it cause problems.

        Returns:
            list: list of methods

        Notes:
            Order of methods in list is important, changing it may cause problems
        """

        return [
            cls._string,
            cls._natural,
            cls._integer,
            cls._decimal,
            lambda value: 8941
        ]

    @classmethod
    def _natural(cls, value: int) -> int:
        """
        Method calculating result for natural numbers

        Args:
            value (int): natural number

        Returns:
            int: result of task function

        Raises:
            CalculatorTypeError: if 'value' argument is not natural number
        """

        if (isinstance(value, int) or isinstance(value, float)) and abs(int(value)) == value:
            return (factorial(value) + value - 1) % 141
        else:
            raise CalculatorTypeError("natural")

    @classmethod
    def _integer(cls, value: int) -> int:
        """
        Method calculating result for integers

        Args:
            value (int): integer argument

        Returns:
            int: result of task function

        Raises:
            CalculatorTypeError: if 'value' argument is not integer
        """

        if isinstance(value, int) or isinstance(value, float) and int(value) == value:
            return value ** 3 % 241
        else:
            raise CalculatorTypeError("integer")

    @classmethod
    def _decimal(cls, value: float) -> int:
        """
        Method for calculating result for decimal numbers

        Args:
            value (float): decimal number

        Returns:
            int: result of task function

        Raises:
            CalculatorTypeError: if 'value' argument is not decimal number
        """

        if isinstance(value, float):
            return int(1 / sin(77 * value)) % 341
        else:
            raise CalculatorTypeError("decimal")

    @classmethod
    def _string(cls, value: str) -> int:
        """
        Method calculating result for string

        Args:
            value (str): string argument

        Returns:
            int: result of task function

        Raises:
            CalculatorTypeError: if 'value' argument is not string
        """

        if isinstance(value, str):
            return len([char for char in value if char.isalpha() and char.isupper()])
        else:
            raise CalculatorTypeError("string")
