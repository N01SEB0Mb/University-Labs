# coding=utf-8
"""
Operation class definition. Used to get specified operations
"""

import math
from typing import Callable

from .number import Number
from .decorator import staticmethod


class Operation:
    """
    Expression.Operation class used to store math operations and info about it
    """

    @staticmethod("+", prior=False)
    def addition(*summands: Number) -> Number:
        """
        Summand numbers

        Args:
            *summands (Number): Numbers you want to summand

        Returns:
            Number: Result
        """

        result: Number = 0

        for summand in summands:
            result += summand

        return result

    @staticmethod("-", prior=False)
    def subtract(minuend: Number, *subtrahends: Number) -> Number:
        """
        Substract numbers

        Args:
            minuend (Number): Minuend numbers
            *subtrahends (Number): Number you want to substract

        Returns:
            Number: result
        """

        result: Number = minuend

        for subtrahend in subtrahends:
            result -= subtrahend

        return result

    @staticmethod("*")
    def multiply(*multipliers: Number) -> Number:
        """
        Multiply numbers

        Args:
            *multipliers (Number): Numbers you want to multiply

        Returns:
            Number: Result
        """

        result: Number = 1

        for multiplier in multipliers:
            result *= multiplier

        return result

    @staticmethod("/")
    def division(dividend: Number, *divisors: Number) -> Number:
        """
        Divide numbers

        Args:
            dividend (Number): Divident number
            *divisors (Number): Divisor numbers

        Returns:
            Number: Result
        """

        result: Number = dividend

        for divisor in divisors:
            result /= divisor

        return result

    @staticmethod("%")
    def mod(dividend: Number, *divisors: Number) -> Number:
        """
        Remainder of division

        Args:
            dividend (Number): Divident number
            *divisors (Number): Divisor numbers

        Returns:
            Number: Result
        """

        result: Number = dividend

        for divisor in divisors:
            result %= divisor

        return result

    @staticmethod("^")
    def power(base: Number, *powers: Number) -> Number:
        """
        Raise number to power

        Args:
            base (Number): Base
            *powers (Number): Powers

        Returns:
            Number: Power result
        """

        result: Number = base

        for power in powers:
            result **= power

        return result

    @staticmethod("abs")
    def abs(number: Number) -> Number:
        """
        Get absolute value

        Args:
            number (Number): number

        Returns:
            Number: Absolute value of number
        """

        if number < 0:
            return -number
        else:
            return number

    @staticmethod("sin")
    def sin(angle: Number) -> Number:
        """
        Angle sinus

        Args:
            angle (Number): Angle

        Returns:
            Number: Sinus of given angle
        """

        return math.sin(angle)

    @staticmethod("cos")
    def cos(angle: Number) -> Number:
        """
        Angle cosinus

        Args:
            angle (Number): Angle

        Returns:
            Number: Cosinus of given angle
        """

        return math.cos(angle)

    @staticmethod("tan")
    def tan(angle: Number) -> Number:
        """
        Angle tangens

        Args:
            angle (Number): Angle

        Returns:
            Number: Tangens of given angle
        """

        return math.tan(angle)

    @staticmethod("cotan")
    def cotan(angle: Number) -> Number:
        """
        Angle cotangens

        Args:
            angle (Number): Angle

        Returns:
            Number: Cotangens of given angle
        """

        return 1.0 / math.tan(angle)

    @staticmethod("asin")
    def asin(value: Number) -> Number:
        """
        Value arcsinus

        Args:
            value (Number): Value

        Returns:
            Number: Angle
        """

        return math.asin(value)

    @staticmethod("acos")
    def acos(value: Number) -> Number:
        """
        Value arccosinus

        Args:
            value (Number): Value

        Returns:
            Number: Angle
        """

        return math.acos(value)

    @staticmethod("sqrt")
    def sqrt(square: Number) -> Number:
        """
        Get square root

        Args:
            square (Number): Given number

        Returns:
            Number: Square root of given number
        """

        return math.sqrt(square)

    @staticmethod("ceil")
    def ceil(number: Number) -> Number:
        """
        Ceiling of number

        Args:
            number (Number): Number

        Returns:
            Number: Ceiling of given number
        """

        return math.ceil(number)

    @staticmethod("floor")
    def floor(number: Number) -> Number:
        """
        Floor of number

        Args:
            number (Number): Number

        Returns:
            Number: Floor of number
        """

        return math.floor(number)

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

        Examples:
            >>> Expression.Operation["*"](2, 2)
            4
            >>> addFunc = Expression.Operation["+"]
            >>> addFunc(3, 4)
            7

        Notes:
            It searches methods from Expression.Operator.__dict__ (except method names containing "_")
            and checks if specified operator method is in method __dir__ attribute.
            If there is no such method, then searches math package functions
        """

        operations = dict(
            filter(
                lambda key: "_" not in key[0],
                cls.__dict__.items()
            )
        )

        for operation, function in operations.items():
            try:
                # If requested operator specified in decorator
                if operator in function.args:
                    return function
            except AttributeError:
                # If decorator not used (math package functions)
                # Checks if requested operator is name of function
                if operator == operation:
                    return function

        raise ValueError(f"Operation '{operator}' not found.")

    @classmethod
    def exists(
            cls,
            operator: str,
            prior=False
    ) -> bool:
        """
        Checks if there are given operator method

        Args:
            operator (str): Operator you want to check
            prior (bool): True if operator must be prior (like multiply). Defaults by False

        Returns:
            bool: Is there given operator method
        """

        operations = dict(
            filter(
                lambda key: "_" not in key[0],
                cls.__dict__.items()
            )
        )

        for operation in operations.values():
            try:
                if operator in operation.args:
                    if not prior or operation.prior:
                        return True
            except AttributeError:
                pass

        return False
