# coding=utf-8
"""
This file defines ResponseItem (abc) and classes for each of 3 methods: search(), info(), currency()

search():
    ResponseSearch.Item: Used to store info about found item
    ResponseSearch.List: Used to store found items

info():
    ResponseInfo.Item: Used to store info about item
    ResponseInfo.Analog: Used to store info about analog of item

currency():
    ResponseCurrency.Item: Used to store info about currency item

Examples:
    info() method usage::
        >>> responseItem = ResponseInfo.Item(itemId=item["id"], article=item["article"])
        >>> responseItem["brand"] = item["brand"]
        >>> return responseItem
"""

from typing import Optional, Union, Any

from .status import ResponseStatus


class ResponseItem(dict):
    """
    This class used to contain parser response. Inherits dict

    Attributes:
        _TEMPLATE (dict): Response template
        id (int): Item unique id

    Notes:
        Keys must be from template, otherwise - they would be ignored.
    """

    _TEMPLATE = {
        "status": ResponseStatus(
            ResponseStatus.EMPTY
        )
    }

    def __init__(
            self,
            itemId: Optional[Union[str, int]] = 0,
            **kwargs: Any
    ) -> None:
        """
        Dict __init__ override. Initializes ResponseItem

        Args:
            itemId (Optional[int]): Item unique id
            **kwargs (Any): Item info

        Keyword Args:
            status (ResponseStatus)
        """

        super(ResponseItem, self).__init__()

        self.id = itemId

        # Saving keys

        for key, value in self._TEMPLATE.items():
            if key in kwargs:
                value = kwargs[key]

            self[key] = value

    def __setitem__(self, key: str, value: Any):
        """
        Dict __setitem__ override. Used to set a value for a specified key

        Args:
            key (str): Key you want to set
            value (Any): Value you want to set

        Notes:
            Keys must be from template, otherwise - they would be ignored.
        """

        if key in self._TEMPLATE:
            super(ResponseItem, self).__setitem__(key, value)


class ResponseSearch:
    """
    This class has Item and List classes, that used to contain search() method response.
    """

    class Item(ResponseItem):
        """
        This class used to contain search() method response for item. Inherits ResponseItem

        Attributes:
            _TEMPLATE (dict): Response template
        """

        _TEMPLATE = {
            "article": "",
            "brand": "",
            "name": "",
            "description": "",
            "price": "",
            "stocks": [],
            "image": None
        }

    class List(ResponseItem):
        """
        This class used to contain search() method response with found items. Inherits ResponseItem

        Attributes:
            _TEMPLATE (dict): Response template
        """

        _TEMPLATE = {
            "results": [],
            "status": ResponseStatus(ResponseStatus.EMPTY)
        }

        def append(
                self,
                item: dict
        ) -> None:
            """
            Appending found item to results

            Args:
                item (ResponseSearch.Item): Item you want to append
            """

            self["results"].append(item)

        def __bool__(self):
            """
            Override __bool__ method.

            Returns:
                bool: True if there are items in results, otherwise - False
            """

            return bool(self["results"])


class ResponseInfo:
    """
    This class has Item and Analog classes, that used to contain info() method response.
    """

    class Analog(ResponseItem):
        """
        This class used to contain info about item analog

        Attributes:
            _TEMPLATE (dict): Response template
        """

        _TEMPLATE = {
            "article": "",
            "brand": "",
            "name": "",
            "description": "",
            "price": "",
            "image": None,
            "stocks": [],
            "foreign": []
        }

    class Item(ResponseItem):
        """
        This class used to contain info() method response for item. Inherits ResponseItem

        Attributes:
            _TEMPLATE (dict): Response template
        """

        _TEMPLATE = {
            "article": "",
            "brand": "",
            "name": "",
            "description": "",
            "price": "",
            "image": None,
            "stocks": [],
            "foreign": [],
            "cross": {},
            "using": {},
            "analogs": [],
            "status": ResponseStatus(
                ResponseStatus.EMPTY
            )
        }

        def setAnalog(
                self,
                analog: dict
        ) -> None:
            self["analogs"].append(analog)


class ResponseCurrency:
    """
    This class has Item class, that used to contain currency() method response.
    """

    class List(ResponseItem):
        """
        This class used to contain currency() method response with found items. Inherits ResponseItem

        Attributes:
            _TEMPLATE (dict): Response template
        """

        _TEMPLATE = {
            "currencies": [],
            "status": ResponseStatus(ResponseStatus.EMPTY)
        }

        def append(
                self,
                currency: dict
        ) -> None:
            """
            Appending found item to results

            Args:
                currency (ResponseSearch.Item): Item you want to append
            """

            self["currencies"].append(currency)

        def __bool__(self):
            """
            Override __bool__ method.

            Returns:
                bool: True if there are any currencies, otherwise - False
            """

            return bool(self["currencies"])

    class Currency(ResponseItem):
        """
        This class used to contain currency() method response for item. Inherits ResponseItem

        Attributes:
            _TEMPLATE (dict): Response template
        """

        _TEMPLATE = {
            "name": "",
            "price": 0.00
        }
