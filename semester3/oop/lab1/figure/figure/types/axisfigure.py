# coding=utf-8

from expression import Expression


class AxisFigure(object):
    """
    AxisFigure class. Implements figure using 1 function.
    Figure is a shape between function and X-axis
    """

    __slots__ = ["__func1", "__func2"]

    def __init__(
            self,
            first: Expression
    ) -> None:
        """
        Initializes Figure object using function

        Args:
            first (Expression): First function

        Raises:
            TypeError: If 'first' argument type is not 'Expression'
        """

        # Check first type
        if isinstance(first, Expression):
            self.__func1 = first
        else:
            raise TypeError(
                f"'first' argument type must be 'Expression', not '{first.__class__.__name__}'"
            )

        self.__func2 = Expression("0")

    @property
    def first(self) -> Expression:
        """
        Get Figure first function
        """

        return self.__func1

    @first.setter
    def first(self, expression: Expression) -> None:
        """
        Set Figure first function

        Args:
            expression (Expression): Function you want to set

        Raises:
            TypeError: If 'expression' argument type is not 'Expression'
        """

        if isinstance(expression, Expression):
            self.__func1 = expression
        else:
            raise TypeError(
                f"Figure first function type must be 'Expression', not '{expression.__class__.__name__}'"
            )

    @first.deleter
    def first(self) -> None:
        """
        Delete Figure first function
        """

        del self.__func1
