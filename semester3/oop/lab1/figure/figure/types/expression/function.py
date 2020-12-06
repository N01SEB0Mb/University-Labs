# coding=utf-8

import math
import functools
from typing import Callable, Optional, Union, Any
from types import FunctionType

from number import Number
from node import ExpressionNode
from operations import Operation
from exceptions import ExpressionError


class Expression:
    """
    Expression class, used to store and evaluate the result of an expression
    """

    def __init__(
            self,
            expressionString: str,
            argumentName: Optional[str] = "x"
    ) -> None:
        """
        Inits function

        Args:
            expressionString (str): Function expression
            argumentName (Optional[str]): The function argumentName specified in the expression. Default is "x"

        Raises:
            ExpressionError: If expression is invalid
        """

        self.__arg: str = argumentName
        self.__func: ExpressionNode = self.__parse(
            expressionString,
            argumentName=argumentName
        )

    def __call__(
            self,
            value: Number
    ):
        return self.__func(value)

    def __parse(
            self,
            expression: str,
            argumentName: Optional[str] = "x"
    ) -> ExpressionNode:
        """
        Parse expression string

        Args:
            expression (str): Function expression you want to parse
            argumentName (Optional[str]): The function argumentName specified in the expression. Default is "x"

        Returns:
            Callable: Given expression converted to callable object

        Raises:
            ExpressionError: If expression is invalid
        """

        def pairUp(
                operationsToPair: list,
                onlyPrior=False
        ) -> list:
            """
            Pair up operations

            Args:
                operationsToPair (list): Operations list to pair
                onlyPrior (bool): Pair up only prior operations

            Returns:
                list: Paired up operations
            """

            index = 1

            # Iterate through operations (every 2-nd element)
            while index < len(operationsToPair):
                if Operation.exists(operationsToPair[index], prior=onlyPrior):
                    # If this is suitable operation

                    # Create operation node
                    operationNode = ExpressionNode(Operation[operationsToPair[index]])

                    # Add operands
                    operationNode.left = operationsToPair[index - 1]
                    operationNode.right = operationsToPair[index + 1]

                    # Replace items by expression node
                    operationsToPair = operationsToPair[:index - 1] + [operationNode] + operationsToPair[index + 2:]
                else:
                    # If this is not suitable operation, check next
                    index += 2

            return operationsToPair

        # Remove spaces
        expression = expression.replace(" ", "")

        # Operation variables
        operations = list()
        current = ""
        signOk = True

        # Parentheses variables
        isParentheses = False
        parentFunction = None
        parenthesesNumber = 0

        # Iterate through expression
        for char in expression:
            if char == "(":  # Start of parentheses
                if parenthesesNumber:  # If parentheses already started
                    current += char

                else:  # If parentheses started
                    if current:
                        parentFunction = Operation[current]
                        current = ""

                    isParentheses = True

                parenthesesNumber += 1

            elif char == ")":  # End of parentheses
                if parenthesesNumber == 0:  # No parentheses to close
                    raise ExpressionError("Unexpected end of parentheses ')'")

                elif parenthesesNumber > 1:  # If parentheses already started
                    current += char

                parenthesesNumber -= 1

            else:  # Other symbol
                if (parenthesesNumber or not Operation.exists(
                        char
                )) or (signOk and not Operation.exists(
                    char, prior=True
                )):  # If parentheses active, char is not operator or this is number sign
                    current += char
                    signOk = False

                else:
                    if isParentheses:  # If parentheses ends
                        if parentFunction is not None:
                            # If there is parent function
                            functionNode = ExpressionNode(parentFunction)
                            functionNode.left = self.__parse(
                                current,
                                argumentName=argumentName
                            )
                            operations.append(functionNode)
                        else:
                            # If there is not parent function
                            operations.append(self.__parse(
                                current,
                                argumentName=argumentName
                            ))

                    else:  # If there was no parentheses
                        if current == f"+{argumentName}" or current == argumentName:  # Positive argumentName
                            operations.append(ExpressionNode(True))

                        elif current == f"-{argumentName}":  # Negative argumentName

                            operations.append(ExpressionNode(False))
                        else:  # Number
                            try:
                                operations.append(ExpressionNode(float(current)))
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
                if parentFunction is not None:
                    # If there is parent function
                    functionNode = ExpressionNode(parentFunction)
                    functionNode.left = self.__parse(
                        current,
                        argumentName=argumentName
                    )
                    operations.append(functionNode)
                else:
                    # If there is not parent function
                    operations.append(self.__parse(
                        current,
                        argumentName=argumentName
                    ))

            else:  # If there was no parentheses
                if current == f"+{argumentName}" or current == argumentName:  # Positive argumentName
                    operations.append(ExpressionNode(True))

                elif current == f"-{argumentName}":  # Negative argumentName
                    operations.append(ExpressionNode(False))
                else:  # Number
                    try:
                        operations.append(ExpressionNode(float(current)))
                    except BaseException:
                        raise ExpressionError(f"Unknown value '{current}'")

        return pairUp(  # Pairing up unprior operations (+, -)
            pairUp(  # Pairing up prior operations
                operations,
                onlyPrior=True
            ),
        )[0]
