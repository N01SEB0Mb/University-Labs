# coding=utf-8

from typing import Any, Optional

from .number import Number


class ExpressionNode:
    """
    Operation class (binary tree node-like)

    Attributes:
        value (Any): Node value
    """

    __slots__ = ["value", "__left", "__right"]

    def __init__(self, value: Any) -> None:
        """
        Initializes Node

        Args:
            value (Any): Node value

        Notes:
            If ExpressionNode supposed to have any childs then 'value' must be callable
            If value is argumentName, then provide True if argumentName is positive, else - False
        """

        self.value: Any = value
        self.__left:  Optional["ExpressionNode"] = None
        self.__right: Optional["ExpressionNode"] = None

    def __call__(self, value: Number) -> Number:
        """
        __call__ method override. Used to get expression result for specified argumentName
        
        Args:
            value (Number): Expression argumentName

        Returns:
            Number: Expression result
        """

        if self.__left is not None or self.__right is not None:
            # Have childs -> value is function

            leftarg: Tuple = (self.__left(value),) if self.__left is not None else ()
            rightarg: Tuple = (self.__right(value),) if self.__right is not None else ()

            return self.value(
                *(leftarg + rightarg)
            )
        else:
            # Does not have childs -> value attribute is number / argumentName

            if self.value is True:
                # Value is argumentName
                return value
            elif self.value is False:
                # Value is argumentName (negative)
                return -value
            else:
                # Value is number
                return self.value

    def __bool__(self) -> bool:
        """
        __bool__ method override. Checks if value attribute is callable

        Returns:
            bool: Is value attribute callable
        """

        return callable(self.value)

    def __str__(self) -> str:
        """
        __str__ method override. Converts ExpressionNode to str

        Returns:
            str: ExpressionNode converted to str
        """

        return f"ExpressionNode({str(self.__left)},{str(self.value)},{str(self.__right)})"

    @property
    def left(self) -> Optional["ExpressionNode"]:
        """
        Get node left child

        Returns:
            ExpressionNode: Node left child
        """

        return self.__left

    @left.setter
    def left(self, node: Optional["ExpressionNode"]) -> None:
        """
        Node left child setter

        Args:
            node (ExpressionNode): Node you want to set

        Raises:
            TypeError: If 'node' argumentName type is not 'ExpressionNode' or None
        """

        if isinstance(node, ExpressionNode):
            self.__left = node
        else:
            raise TypeError(
                f"Node left child type must be 'ExpressionNode' or None, not '{node.__class__.__name__}'"
            )

    @left.deleter
    def left(self) -> None:
        """
        Delets node left child
        """

        del self.__left

    @property
    def right(self) -> Optional["ExpressionNode"]:
        """
        Get node right child

        Returns:
            ExpressionNode: Node right child
        """

        return self.__right

    @right.setter
    def right(self, node: Optional["ExpressionNode"]) -> None:
        """
        Node right child setter

        Args:
            node (ExpressionNode): Node you want to set

        Raises:
            TypeError: If 'node' argumentName type is not 'ExpressionNode' or None
        """

        if isinstance(node, ExpressionNode):
            self.__right = node
        else:
            raise TypeError(
                f"Node right child type must be 'ExpressionNode' or None, not '{node.__class__.__name__}'"
            )

    @right.deleter
    def right(self) -> None:
        """
        Delets node right child
        """

        del self.__right

