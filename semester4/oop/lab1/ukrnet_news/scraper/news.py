# coding=utf-8

import logging
import requests
from typing import *
from urllib.parse import urlparse

from .parser import PARSER_CLASSES
from ukrnet_news.utils import clear
from ukrnet_news.config import CONFIG, BLACKLIST
from ukrnet_news.exceptions import ParserNotFoundError, EmptyNewsError, InBlacklistError


class News:
    """
    News class. Stores info about news
    """

    __slots__ = ("id", "url", "title", "description", "image_url", "dups")

    def __init__(
            self,
            news_id: int,
            url: str,
            title: str,
            description: str,
            image_url: Optional[str] = None,
            dups: Optional[List[int]] = None
    ) -> None:
        """
        News object initialization

        Args:
            news_id (int): News ID
            title (str): News title
            description (str): News description
            image_url (Optional[str]): News image URL
            dups (Optional[List[int]]): List of IDs of news dups (equal news)
        """

        self.id:  int = news_id
        self.url: str = url

        # Define news info
        self.title:       str = clear(title)
        self.description: str = clear(description)
        self.image_url:   str = image_url

        # Define news dups
        self.dups: List[int] = dups or []

    @classmethod
    def from_url(cls, url: str, *args: Any, **kwargs: Any) -> "News":
        """
        Get news from specified url

        Args:
            url (str): News URL

        Returns:
            News: News object

        Raises:
            InBlacklistError: If site is in the blacklist
            EmptyNewsError: If title or description are None
            ParserNotFoundError: If no parsers found for specified URL
        """

        # Parse URL
        parsed_url = urlparse(url)

        # Check blaclist
        if parsed_url.netloc in BLACKLIST:
            # Given URL is in the blacklist
            raise InBlacklistError(f"Specified URL is in the blacklist '{url}'")

        # Select matching parser
        for parser_class in PARSER_CLASSES:
            # Check if given URL contains parser's specified url

            if parser_class.url in parsed_url.netloc:
                # Found matching parser
                break
        else:
            # No parser found => exception
            raise ParserNotFoundError("Parser not found for specified URL")

        # Get news page
        page_request = requests.get(
            url,
            headers=CONFIG["connection"]["headers"],
            timeout=CONFIG["connection"]["timeout"]
        )

        if page_request.status_code != 200:
            # Failed to get news page
            raise requests.exceptions.RequestException(f"Failed to get '{url}'")

        # Get news info
        title, description, image_url = parser_class.parse(page_request.text, page_url=url)

        if not title or not description:
            # No news info
            raise EmptyNewsError(f"Couldn't get news page info '{url}'")

        return cls(
            url=url,
            title=title,
            description=description,
            image_url=image_url,
            *args, **kwargs
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "News":
        """
        Create News object from dict

        Args:
            data (Dict[str, Any]): News dict you want top convert

        Returns:
            News: Converted News object
        """

        return cls(
            news_id=data["id"],
            url=data["url"],
            title=data["title"],
            description=data["description"],
            image_url=data["image_url"],
            dups=data["dups"],
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converting News object to dictionary

        Returns:
            Dict[str, Any]: Converted News
        """

        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "dups": self.dups
        }
