# coding=utf-8

from typing import Callable, Any


class staticmethod(object):
    """
    @staticmethod decorator redefinition.
    Used to store decorator arguments to __dir__ attribute and function __doc__

    Attributes:
        args (list): Decorator parameters
    """

    def __init__(self, *args: Any) -> None:
        """
        __init__ method override. Used to store decorator arguments into __dir__ attribute
        
        Args:
            *args (Any): Decorator arguments you want to store

        Examples:
            >>> class A:
            ...    @staticmethod("+")
            ...    def add(a, b):
            ...        return a + b
            ...
            >>> A.add.__dir__
            ["+"]
        """

        self.args = list(args)

    def __call__(self, function: Callable) -> Callable:
        """
        __call__ method override

        Args:
            function (Callable): Decorated function

        Returns:
            Callable: Wrapped function
        """

        def wrapper(*args: Any) -> Any:
            """
            Wrapper function

            Args:
                *args (Any): Function arguments

            Returns:
                Any: Function result
            """

            return function(*args)

        wrapper.__dir__ = self.args
        wrapper.__doc__ = function.__doc__

        return wrapper
