# coding=utf-8

from abc import ABC
from typing import Any


class BaseNewsException(Exception, ABC):
    """
    BaseNewsException class. Commonn class for all package exceptions
    """

    __msg: str

    def __init__(self, err_msg: str = "", *args: Any, **kwargs: Any) -> None:
        """
        ParserNotFoundError object initialization

        Args:
            err_msg (str): Error description
            *args (Any): BaseNewsException *args
            **kwargs (Any): BaseNewsException **kwargs
        """

        super(ExpressionError, self).__init__(err_msg or self.__msg, *args, **kwargs)


class ParserNotFoundError(BaseNewsException):
    """
    No parser found for given website
    """

    __msg = "No parser found for given website"


class EmptyNewsError(BaseNewsException):
    """
    No news info provided (title or description is empty)
    """

    __msg = "No news info provided"


class InBlacklistError(BaseNewsException):
    """
    Given website is in the blacklist
    """

    __msg = "Given website is in the blacklist"
