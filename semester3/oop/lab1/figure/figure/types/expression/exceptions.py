# coding=utf-8

from typing import Optional, Any


class ExpressionError(SyntaxError):
    """
    Raised if invalid function expression is given
    """

    def __init__(
            self,
            errmsg: Optional[str] = "",
            *args: Any,
            **kwargs: Any
    ) -> None:
        """
        __init__ method override. Initalizes ExpressionError object

        Args:
            errmsg (Optional[str]): Error description
            *args (Any): SyntaxError.__init__ *args
            **kwargs: SyntaxError.__init__ **kwargs
        """

        super(ExpressionError, self).__init__(
            errmsg if errmsg else "Invalid expression given",
            *args,
            **kwargs
        )
