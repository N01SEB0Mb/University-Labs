# coding=utf-8

from typing import Callable, Optional, Any


class staticmethod(object):
    """
    @staticmethod decorator redefinition.
    Used to store decorator arguments to args and prior attributes and function __doc__

    Attributes:
        args (list): Decorator parameters
    """

    def __init__(
            self,
            *args: Any,
            prior: Optional[bool] = True
    ) -> None:
        """
        __init__ method override. Used to store decorator arguments into args and prior attributes
        
        Args:
            *args (Any): Decorator arguments you want to store
            prior (Optional[bool]): Is method prior. Defaults by True

        Examples:
            >>> class A:
            ...    @staticmethod("+")
            ...    def add(a, b):
            ...        return a + b
            ...
            >>> A.add.args
            ["+"]
        """

        self.args = list(args)
        self.prior = prior

    def __call__(
            self,
            function: Callable
    ) -> Callable:
        """
        __call__ method override

        Args:
            function (Callable): Decorated function

        Returns:
            Callable: Wrapped function
        """

        def wrapper(
                *args: Any
        ) -> Any:
            """
            Wrapper function

            Args:
                *args (Any): Function arguments

            Returns:
                Any: Function result
            """

            return function(*args)

        wrapper.args = self.args
        wrapper.prior = self.prior
        wrapper.__doc__ = function.__doc__

        return wrapper
