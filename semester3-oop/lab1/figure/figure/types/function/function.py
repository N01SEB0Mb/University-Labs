# coding=utf-8

import math
from typing import Callable, Optional, Union, Any

from .decorator import staticmethod


Number = Union[int, float]


class Function:
    """
    Function class, used to store and evaluate the result of an expression
    """

    class Operation:
        """
        Function.Operation class used to store math operations and info about it
        """

        @staticmethod("+")
        def addition(
                *summands: Number
        ) -> Number:
            """
            Summand numbers

            Args:
                *summands (Number): Numbers you want to summand

            Returns:
                Number: Result
            """

            result = 0

            for summand in summands:
                result += summand

            return result

        @staticmethod("-")
        def subtract(
                minuend: Number,
                *subtrahends: Number
        ) -> Number:
            """
            Substract numbers

            Args:
                minuend (Number): Minuend numbers
                *subtrahends (Number): Number you want to substract

            Returns:
                Number: result
            """

            result = minuend

            for subtrahend in subtrahends:
                result -= subtrahend

            return result

        @staticmethod("*")
        def multiply(
                *multipliers: Number
        ) -> Number:
            """
            Multiply numbers

            Args:
                *multipliers (Number): Numbers you want to multiply

            Returns:
                Number: Result
            """

            result = 1

            for multiplier in multipliers:
                result *= multiplier

            return result

        @staticmethod("/")
        def division(
                dividend: Number,
                *divisors: Number
        ) -> Number:
            """
            Divide numbers

            Args:
                dividend (Number): Divident number
                *divisors (Number): Divisor numbers

            Returns:
                Number: Result
            """

            result = dividend

            for divisor in divisors:
                result /= divisor

            return result

        @staticmethod("^")
        def power(
                base: Number,
                power: Number
        ) -> Number:
            """
            Raise number to power

            Args:
                base (Number): Base
                power (Number): Power

            Returns:
                Number: Power result
            """

            return base ** power

        def __class_getitem__(
                cls,
                operator: str
        ) -> Callable:
            """
            __class_getitem__ method override.
            Used to get operation method for specified operator char

            Args:
                operator (str): Operator

            Returns:
                Callable: Operation method

            Raises:
                ValueError: If specified operation not found
            """

            operations = dict(
                filter(
                    lambda key: "_" not in key[0],
                    cls.__dict__.items()
                )
            )

            for operation in operations.values():
                if operator in operation.__dir__:
                    return operation

            raise ValueError(f"Operation '{operator}' not found.")

    def __init__(
            self,
            expression: str,
            argument: Optional[str] = "x"
    ) -> None:
        """
        Inits function

        Args:
            expression (str): Function expression
            argument (Optional[str]): The function argument specified in the expression. Default is "x"

        Raises:
            ExpressionError: if expression is invalid
        """

        pass
