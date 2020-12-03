# coding=utf-8

from abc import ABC, abstractmethod


class IndexCounter(object):
    """
    IndexCounter class. Used for count N (number) value.
    Just call IndexCounter item to get current number.
    Index increments after every call.

    Examples:
        >>> counter = IndexCounter()
        >>> counter()
        1
        >>> counter()
        2
    """

    def __init__(self, startValue: int = 1) -> None:
        """
        Initialize counter.

        Args:
            startValue (int, optional): start index. Defaults by 1
        """

        self.__value = startValue - 1

    def __call__(self) -> int:
        """
        Call method. Used to get index

        Returns:
            int: current index
        """

        self.__value += 1
        return self.__value


class BaseABC(ABC):
    """
    Abstract base class BaseABC.
    Inherited by Base1 and Base2.
    Defines all used methods.
    """

    def __init__(self, *args) -> None:
        """
        Initialize object, set N attribute and include some items

        Args:
            *args: items you want to include

        Attributes:
            N (int): object number
            included (tuple): included items
        """

        self.N = NCounter()
        self.included = args

    def __call__(self, s: int) -> int:
        """
        Used to get S value after deleting.
        First it calculated for each child, after for itself

        Args:
            s (int): S value before deleting

        Returns:
            int: S value after deleting
        """

        for item in self.included:
            s = item(s)

        return self.formula(s)

    @abstractmethod
    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return s

    def __del__(self) -> None:
        """
        Deletes item and it childs. Updates S value
        """

        global S

        for item in self.included:
            item.__del__()

        S = self(S)

    def __str__(self) -> str:
        """
        Converting item to string. Uses only N value

        Returns:
            str: converted item

        Examples:
            >>> a = BaseABC()
            >>> str(a)
            "1"
        """

        return f"{self.N}"

    def __repr__(self) -> str:
        """
        Representation of item. Shows N value and class name

        Returns:
            str: representation of item.

        Examples:
            >>> a = BaseABC()
            >>> repr(a)
            "BaseABC(N=1)"
        """

        return f"{self.__class__.__name__}(N={self.N})"


class Base1(BaseABC):
    """
    Base1 class. Inherits BaseABC and inherited by Alpha and Beta classes
    """

    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return 3 * s + self.N + 41


class Base2(BaseABC):
    """
    Base2 class. Inherits BaseABC and inherited by Gamma and Delta classes
    """

    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return s // 2 - self.N


class Alpha(Base1):
    """
    Alpha class. Inherits Base1
    """

    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return s - 2 * self.N + 14


class Beta(Base1):
    """
    Beta class. Inherits Base1
    """

    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return s - self.N


class Gamma(Base2):
    """
    Gamma class. Inherits Base2
    """

    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return s - self.N


class Delta(Base2):
    """
    Delta class. Inherits Base2
    """

    def formula(self, s: int) -> int:
        """
        Formula, used to calculate S value after deleting item (not counting included items)

        Args:
            s (int): S value

        Returns:
            int: S value after calculating
        """

        return s + 3 * self.N - 41


NCounter = IndexCounter()
S = 1
