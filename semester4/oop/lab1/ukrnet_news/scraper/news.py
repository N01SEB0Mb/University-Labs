# coding=utf-8

import logging
import requests
from typing import *

from .parser import PARSER_CLASSES
from ukrnet_news.config import CONFIG


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
        self.title:       str = title
        self.description: str = description
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
            ModuleNotFoundError: If no parsers found for specified URL (broken PARSER_CLASSES list)
            ValueError: If title or description are None
        """

        # Select matching parser
        for parser_class in PARSER_CLASSES:
            # Check if given 'url' contains parser's specified url

            if parser_class.url in url:
                # Found matching parser
                break
        else:
            # No parser found => exception
            raise ModuleNotFoundError("Parser not found for specified URL")

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

        if title is None or description is None:
            # No news info
            raise ValueError(f"Couldn't get news page info '{url}'")

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
