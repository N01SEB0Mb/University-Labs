# coding=utf-8

from math import nan, isnan

from .expression import Expression, Number


class AxisFigure(object):
    """
    AxisFigure class. Implements figure using 1 function.
    Figure is a shape between function and X-axis
    """

    __slots__ = ["__func1", "__func2"]

    def __init__(self, first: Expression) -> None:
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

    def area(
            self,
            start: Number,
            end: Number,
            parts: int = 1000
    ) -> Number:
        """
        Calculate shape area

        Args:
            start (Number): Start ordinate (x0)
            end (Number): End ordinate (x1)
            parts (int): Count of shape parts. Greater -> more accuracy

        Returns:
            Number: Shape area
        """

        getX = lambda index: start + (index / parts) * (end - start)

        result = 0

        for part in range(parts):
            x = getX(part + 0.5)

            try:
                height = self.height(x)
                assert not isnan(height)
            except BaseException:
                pass
            else:
                result += height

        return result * (end - start) / parts

    def height(self, x: Number):
        try:
            firstValue = self.__func1(x)
            secondValue = self.__func2(x)
        except BaseException:
            return nan
        else:
            return abs(firstValue - secondValue)


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
