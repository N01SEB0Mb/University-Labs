# coding=utf-8

from typing import *


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
    def from_url(cls, url: str) -> "News":
        """
        Get news from specified url

        Args:
            url (str): News URL

        Returns:
            News: News object
        """

        pass
