# coding=utf-8

from typing import *


def exception_handler(function: Callable) -> Callable:
    """
    Wrapping function in try-except expression

    Args:
        function (Callable): Function, you want to wrap

    Returns:
        Callable: Function wrapper
    """

    def try_except_wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
        """
        Running wrapped function with specified arguments

        Args:
            *args (Any): 'function' *args
            **kwargs (Any): 'function' **kwargs

        Returns:
            Optional[Any]: 'function' result
        """

        try:
            # Try executing function
            result: Any = function(*args, **kwargs)

        except BaseException:
            # Some exception raised
            return None

        else:
            # No exceptions
            return result

    return try_except_wrapper


def async_exception_handler(function: Callable) -> Callable:
    """
    Wrapping asynchronous function in try-except expression

    Args:
        function (Callable): Function, you want to wrap

    Returns:
        Callable: Function wrapper
    """

    async def async_try_except_wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
        """
        Running wrapped asynchronuous function with specified arguments

        Args:
            *args (Any): 'function' *args
            **kwargs (Any): 'function' **kwargs

        Returns:
            Optional[Any]: 'function' result
        """

        try:
            # Try executing function
            result: Any = await function(*args, **kwargs)

        except BaseException:
            # Some exception raised
            return None

        else:
            # No exceptions
            return result

    return async_try_except_wrapper
