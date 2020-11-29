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

        @staticmethod("+", prior=False)
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

        @staticmethod("-", prior=False)
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

            Examples:
                >>> Function.Operation["*"](2, 2)
                4
                >>> addFunc = Function.Operation["+"]
                >>> addFunc(3, 4)
                7

            Notes:
                It searches methods from Function.Operator.__dict__ (except method names containing "_")
                and checks if specified operator method is in method __dir__ attribute
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
                        return operation
                except AttributeError:
                    pass

            raise ValueError(f"Operation '{operator}' not found.")

        @classmethod
        def isOperator(
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
            ExpressionError: If expression is invalid
        """

        self.__arg = argument
        self.__func = self.__parse(
            expression,
            argument=argument
        )

    def __call__(
            self,
            value: Number
    ):
        return self.__func(value)

    def __parse(
            self,
            expression,
            argument: Optional[str] = "x"
    ) -> Callable:
        """
        Parse expression string

        Args:
            expression (str): Expression you want to parse
            argument (Optional[str]): The function argument specified in the expression. Default is "x"

        Returns:
            Callable: Expression converted to function

        Raises:
            ExpressionError: If expression is invalid

        """

        # Remove spaces
        expression = expression.replace(" ", "")

        # Operation variables
        operations = list()
        current = ""
        signOk = True

        # Parentheses variables
        isParentheses = False
        parenthesesNumber = 0

        # Iterate through expression
        for char in expression:
            if char == "(":  # Start of parentheses
                if parenthesesNumber:  # If parentheses already started
                    current += char

                else:  # If parentheses started
                    isParentheses = True

                parenthesesNumber += 1

            elif char == ")":  # End of parentheses
                if parenthesesNumber == 0:  # No parentheses to close
                    raise ExpressionError("Unexpected end of parentheses ')'")

                elif parenthesesNumber > 1:  # If parentheses already started
                    current += char

                parenthesesNumber -= 1

            else:  # Other symbol
                if (parenthesesNumber or not self.Operation.isOperator(
                        char
                )) or (signOk and not self.Operation.isOperator(
                    char, prior=True
                )):  # If parentheses active, char is not operator or this is number sign
                    current += char
                    signOk = False

                else:
                    if isParentheses:  # If parentheses ends
                        operations.append(self.__parse(
                            current,
                            argument=argument
                        ))

                    else:  # If there was no parentheses
                        if current == f"+{argument}" or current == argument:  # Positive argument
                            operations.append(lambda x: x)

                        elif current == f"-{argument}":  # Negative argument
                            operations.append(lambda x: -x)
                        else:  # Number
                            try:
                                operations.append(float(current))
                            except BaseException:
                                raise ExpressionError(f"Unknown value '{current}'")

                    # Add current operation
                    operations.append(char)

                    # Clear variables
                    current = ""
                    isParentheses = False
                    signOk = True

        if current:  # If last part not added
            if isParentheses:  # If parentheses ends
                operations.append(self.__parse(
                    current,
                    argument=argument
                ))

            else:  # If there was no parentheses
                if current == f"+{argument}" or current == argument:  # Positive argument
                    operations.append(lambda x: x)

                elif current == f"-{argument}":  # Negative argument
                    operations.append(lambda x: -x)
                else:  # Number
                    try:
                        operations.append(float(current))
                    except BaseException:
                        raise ExpressionError(f"Unknown value '{current}'")

        # Prioring operations variables
        prioredOperations = list()
        lastPrior = -1

        # Iterating through operations
        for number in range(1, len(operations), 2):
            if not Function.Operation.isOperator(operations[number], prior=True):
                if number - lastPrior > 2:  # If two or more operators since last prior
                    prioredOperations.append(
                        self.__toFunc(
                            operations[lastPrior + 1: number]
                        )
                    )
                else:  # If only one operator
                    prioredOperations.append(
                        operations[number - 1]
                    )

                prioredOperations.append(
                    operations[number]
                )
                lastPrior = number
        else:
            if prioredOperations:  # If there are unpriored operations
                number += 1

                if number - lastPrior >= 2:
                    prioredOperations.append(
                        self.__toFunc(
                            operations[lastPrior + 1: number + 1]
                        )
                    )
                else:
                    prioredOperations.append(
                        operations[number]
                    )
            else:  # If every operation is prior
                prioredOperations = operations[:]

        return self.__toFunc(prioredOperations)

    def __toFunc(
            self,
            operations: list
    ) -> Callable:
        leftarg = operations[0]

        for index in range(1, len(operations), 2):
            rightarg = operations[index + 1]
            opfunc = self.Operation[operations[index]]

            if isinstance(leftarg, float) and isinstance(rightarg, float):
                return self.__toFunc([lambda x: opfunc(leftarg, rightarg)] + operations[3:])
            elif isinstance(leftarg, float):
                return self.__toFunc([lambda x: opfunc(leftarg, rightarg(x))] + operations[3:])
            elif isinstance(rightarg, float):
                return self.__toFunc([lambda x: opfunc(leftarg(x), rightarg)] + operations[3:])
            else:
                return self.__toFunc([lambda x: opfunc(leftarg(x), rightarg(x))] + operations[3:])

        if isinstance(leftarg, float):
            return lambda x: leftarg
        else:
            return leftarg
