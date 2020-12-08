# coding=utf-8
"""
This file defines ResponseStatus class that is used in response.
Response status configuration could be found in "~/topauto_parser/config/data/status.json"

Examples:
    Successful response status example::
        status = ResponseStatus(ResponseStatus.SUCCESS)
"""

from typing import Optional

from topauto_parser.config import STATUS


class ResponseStatus(dict):
    """
    This class used to make response statuses. Inherits dict

    Attributes:
        ResponseStatus.SUCCESS (str): Success code

        ResponseStatus.EMPTY (str): Empty response
        ResponseStatus.NOT_DEFINED (str): Method is not defined

        ResponseStatus.NOT_FOUND (str): Item not found
        ResponseStatus.NO_ARTICLE (str): Article not found
        ResponseStatus.NO_BRAND (str): Brand not found

        ResponseStatus.NO_CONNECTION (str): Connection error
        ResponseStatus.TIMEOUT_EXPIRED (str): Connection timeout expired
        ResponseStatus.NOT_AUTHORIZED (str): Authorization failed

        ResponseStatus.INTERNAL_ERROR (str): Python error code
        ResponseStatus.NO_MEMORY (str): No memory to save file

        code (int): Status code
        message (str): Status message
    """

    SUCCESS = "success"

    EMPTY = "empty"
    NOT_DEFINED = "notDefined"

    NOT_FOUND = "itemNotFound"
    NO_ARTICLE = "articleNotFound"
    NO_BRAND = "brandNotFound"

    NO_CONNECTION = "noConnection"
    TIMEOUT_EXPIRED = "timeoutExpired"
    NOT_AUTHORIZED = "authorizationFailed"

    INTERNAL_ERROR = "internalError"
    NO_MEMORY = "noMemory"

    def __init__(
            self,
            status: str,
            description: Optional[str] = "",
            language: Optional[str] = "ua"
    ) -> None:
        """
        Initializes response status item

        Args:
            status (str): Response status (use ResponseStatus class attributes)
            description (Optional[str]): Response status description. Empty by default
            language (Optional[str]): Response status message language. Defaults by "ua"

        Raises:
            KeyError: If there is no such response with given status
            TypeError: If any of args is not "str" type
        """

        # Initializing dict

        super(ResponseStatus, self).__init__()

        # Saving status info to attributes

        self.code = STATUS[status]["code"]
        self.message = STATUS[status]["message"][language]

        if description:
            self.message += f" ({description})"

        # Saving status info to dict

        self["code"] = self.code
        self["message"] = self.message
