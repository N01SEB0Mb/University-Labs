# coding=utf-8
"""
Demonstration of functions and classes defined in package "calculate"

Follow instructions in the console.
You should entering values following Python3 syntax
"""

from typing import Union, Any

from calculate import *


def inputValue() -> Union[int, float, str, list, tuple, Any]:
    """
    Function for reading values from console
    It using eval() to read values, so you must follow Python3 syntax

    Returns:
        int / float / str / list / tuple / Any: read value

    Notes:
        The function reads in the loop, so it will not end until you enter a valid value
    """

    while True:
        try:
            inputStr = input("Type value to calculate or <Enter> to exit: ")
            assert inputStr
            return eval(inputStr)
        except (SyntaxError, TypeError, ValueError):
            print("Wrong type, try again.")
        except AssertionError:
            return False


if __name__ == "__main__":
    calcCall = CalcCall()

    value = inputValue()

    while value:
        print(f'CalcFunc({value}) = {CalcFunc(value)}\n'
              f'CalcCall({value}) = {calcCall(value)}\n'
              f'CalcNew({value})  = {CalcNew(value)}\n')

        value = inputValue()
