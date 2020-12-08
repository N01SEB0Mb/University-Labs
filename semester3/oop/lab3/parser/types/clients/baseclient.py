# coding=utf-8
"""
This file defines BaseClient abc.
Used to store configuration and making basic functions

Also, imported all required packages for any of sites
"""

import json
import requests
import datetime
from lxml import html
from math import ceil
from hashlib import md5
from copy import deepcopy
from random import choice
from datetime import datetime
from time import strftime, time
from typing import Any, Optional, Tuple, Set, Generator
from requests.packages.urllib3 import disable_warnings


from topauto_parser.config import PARSER, BRANDS, Path
from topauto_parser.types.response import ResponseStatus, ResponseSearch, ResponseInfo, ResponseCurrency


disable_warnings()


class BaseClient(requests.Session):
    """
    BaseClient abc, inherits requests.Session
    Used to store configuration and making basic functions

    Attributes:
        name (str): Name of client
        onlyMatchingArt (bool): Option to search only matching item articles
        currencies (set): Set of required currencies. Other will be ignored

        pingConnection (bool): Option to ping connection every time instead of saving connection status
        pingAuthorization (bool): Option to ping authorization every time instead of saving authorization status

        connected (bool): Is client connected
        loggedIn (bool): Is client logged in
        loginTime (float): Time spent on authorization (seconds)
    """

    name: str
    onlyMatchingArt: bool = PARSER["onlyMatchingArticle"]
    currencies: set = set(PARSER["currencies"])

    # Connection verifying settings

    pingConnection = PARSER["connection"]["ping"]["connected"]
    pingAuthorization = PARSER["connection"]["ping"]["loggedIn"]

    def __init__(
            self,
            *args: Any,
            **kwargs: Any
    ) -> None:
        """
        Initializes BaseClient object

        Args:
            *args (Any): requests.Session args
            **kwargs (Any): requests.Session kwargs
        """

        super(BaseClient, self).__init__(*args, **kwargs)

        self.headers.update(PARSER["connection"]["headers"])
        self.timeout = PARSER["connection"]["timeout"]
        self.verify = False

        # Authorization

        startTime = time()

        self._connected: bool = False
        self._loggedIn: bool = False

        try:
            self._connected, self._loggedIn = self.signIn()
        except BaseException:
            pass

        self.loginTime = time() - startTime

    def getImage(
            self,
            imageLink: str,
            imageId: str
    ) -> str:
        """
        Downloads image and saves it to the file

        Args:
            imageLink (str): Image URL
            imageId (str): Image unique id

        Returns:
            str: Path to image if download was successful, otherwise - None
        """

        imageRequest = self.get(
            imageLink,
            timeout=self.timeout
        )

        if imageRequest.status_code == 200:

            imagePath = Path(".").resolve() / PARSER["picturesPath"].format(
                self.name,
                str(imageId)
            )

            with imagePath.open("wb") as imageFile:
                imageFile.write(imageRequest.content)

                return str(imagePath)

    @classmethod
    def compareArticles(
            cls,
            searchArticle: str,
            foundArticle: str
    ) -> bool:
        """
        Used to compare articles.
        Checks if every 'searchArticle' character is in 'foundArticle'

        Args:
            searchArticle (str): Searching article
            foundArticle (str): Article you want to compare

        Returns:
            bool: Is articles equal to each other

        Notes:
            Only letters and numbers are compared.
            If onlyMatchingArt attribute is False, always returns True

        Examples:
            >>> client = BaseClient()
            >>> client.onlyMatchingArt = True
            >>> client.compareArticles("115906", "115-906")
            True
            >>> client.compareArticles("115906", "115907")
            False
            >>> client.onlyMatchingArt = False
            >>> client.compareArticles("115906", "115907")
            True
        """

        searchChars = [char for char in searchArticle.lower() if char.isalnum()]

        for char in foundArticle.lower():
            try:
                if char == searchChars[0]:
                    searchChars.pop(0)
            except IndexError:
                break

        return not searchChars or not cls.onlyMatchingArt

    @classmethod
    def compareBrands(
            cls,
            searchBrand: str,
            foundBrand: str
    ) -> bool:
        """
        Used to compare brands.
        Checks if strings are equal or in same list of equal brands (topauto_parser.config.BRANDS)

        Args:
            searchBrand (str): Searching brand
            foundBrand (str): Brand you want to compare

        Returns:
            bool: Is brands equal
        """

        searchBrand = cls.clear(searchBrand).upper()
        foundBrand = cls.clear(foundBrand).upper()

        if searchBrand == foundBrand:
            return True

        for brandVariants in BRANDS:
            if (searchBrand in brandVariants) and (foundBrand in brandVariants):
                return True

        return False

    @staticmethod
    def clear(
            string: str,
            delchars: Optional[str] = ""
    ) -> str:
        """
        Clears string: removes unwanted spaces, html tags, specified and special characters

        Args:
            string (str): String you want to clear
            delchars (Optional[str]): Characters you want to remove from string

        Returns:
            str: Cleared string

        Raises:
            TypeError: if 'string' argument type is not 'str'
        """

        # Checking str type

        if string is None:
            return ""
        elif not isinstance(string, str):
            raise TypeError(f"'string' argument type must be 'str', not '{string.__class__.__name__}'")

        # Deleting unwanted symbols

        for delstring in ["\n", "\t", "<b>", "</b>"]:
            string = string.replace(delstring, "")

        string = string.translate(
            str.maketrans(
                dict.fromkeys(delchars)
            )
        )

        # Clearing extra spaces

        if string:
            index = 1

            try:
                # Clearing extra spaces at the beginning of string

                while string[0] == " ":
                    string = string[1:]

                # Clearing extra spaces between words

                while index < len(string) - 2:
                    if string[index] == string[index + 1] == " ":
                        string = string[:index] + string[index + 1:]
                    else:
                        index += 1

                # Clearing extra spaces at the end of string

                if string:
                    while string[-1] == " ":
                        string = string[:-1]
            except IndexError:
                pass

        return string

    @staticmethod
    def search(
            article: str
    ) -> ResponseSearch.List:
        """
        Abstract method of searching

        Args:
            article (str): Article of item you want to find

        Returns:
            ResponseSearch.List: Searching response

        Notes:
            It must be overridden by child.
            Otherwise, this method would be used,
            and it will return that this method is not defined
        """

        return ResponseSearch.List(
            status=ResponseStatus(
                ResponseStatus.NOT_DEFINED
            )
        )

    @staticmethod
    def info(
            article: str,
            brand: str
    ) -> ResponseInfo.Item:
        """
        Abstract method of getting item info

        Args:
            article (str): Article of item you want to find
            brand (str): Brand of item you want to find

        Returns:
            ResponseInfo.Item: Getting info response

        Notes:
            It must be overridden by child.
            Otherwise, this method would be used,
            and it will return that this method is not defined
        """

        return ResponseInfo.Item(
            status=ResponseStatus(
                ResponseStatus.NOT_DEFINED
            )
        )

    @staticmethod
    def currency() -> ResponseCurrency.List:
        """
        Abstract method of getting currency

        Returns:
            ResponseCurrency.Item: Getting currency response

        Notes:
            It must be overridden by child.
            Otherwise, this method would be used,
            and it will return that this method is not defined
        """

        return ResponseCurrency.List(
            status=ResponseStatus(
                ResponseStatus.NOT_DEFINED
            )
        )

    def signIn(self) -> Tuple[bool, bool]:
        """
        Client authorization.

        Returns:
            Tuple[bool, bool]: Is connected, is authorized

        Notes:
            It must be overridden by child (except cases when using API without authorization)
        """

        return True, True

    @property
    def connected(self) -> bool:
        """
        Verifying connection.
        If attribute pingConnection is True, then it pinging connection. Otherwise,
        it returns saved connection status

        Returns:
            bool: Is client connected

        Notes:
            Pinging connection is better than using saved status, but takes more time
        """

        if self.pingConnection:
            self._connected = self._pingConnection()

        return self._connected

    @property
    def loggedIn(self) -> bool:
        """
        Verifying authorization.
        If attribute pingAuthorization is True, then it pinging authorization. Otherwise,
        it returns saved authorization status

        Returns:
            bool: Is client authorized

        Notes:
            Pinging authorization is better than using saved status, but takes more time
        """

        if self.pingAuthorization:
            self._loggedIn = self._pingAuthorization()

        return self._loggedIn

    def _pingConnection(self) -> bool:
        """
        Virtual method of pinging client connection.

        Returns:
            bool: Is client connected

        Notes:
            It must be overridden by child.
            Otherwise, this method would be used,
            and it will return saved connection status
        """

        return self._connected

    def _pingAuthorization(self) -> bool:
        """
        Virtual method of pinging client authorization.

        Returns:
            bool: Is client authorized

        Notes:
            It must be overridden by child.
            Otherwise, this method would be used,
            and it will return saved authorization status
        """

        return self._loggedIn
