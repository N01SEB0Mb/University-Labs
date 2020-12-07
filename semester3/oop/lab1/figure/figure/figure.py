# coding=utf-8

from expression import Expression
from .axisfigure import AxisFigure


class Figure(AxisFigure):
    """
    Figure class. Implements figure using 2 functions.
    Figure is a shape between functions
    """

    def __init__(
            self,
            first: Expression,
            second: Expression
    ) -> None:
        """
        Initializes Figure object using 2 functions

        Args:
            first (Expression): First function
            second (Expression): Second function

        Raises:
            TypeError: If 'first'/'second' argument type is not 'Expression'
        """

        super(Figure, self).__init__(first)

        # Check second type
        if isinstance(second, Expression):
            self.__func2 = second
        else:
            raise TypeError(
                f"'seconds' argument type must be 'Expression', not '{second.__class__.__name__}'"
            )

    @property
    def second(self) -> Expression:
        """
        Get Figure second function
        """

        return self.__func2

    @second.setter
    def second(self, expression: Expression) -> None:
        """
        Set Figure second function

        Args:
            expression (Expression): Function you want to set

        Raises:
            TypeError: If 'expression' argument type is not 'Expression'
        """

        if isinstance(expression, Expression):
            self.__func2 = expression
        else:
            raise TypeError(
                f"Figure second function type must be 'Expression', not '{expression.__class__.__name__}'"
            )

    @second.deleter
    def second(self) -> None:
        """
        Delete Figure second function
        """

        del self.__func2
