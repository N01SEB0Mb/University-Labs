# coding=utf-8

import abc
from typing import *
from lxml import html
from urllib.parse import urlparse


class BaseInfoParser(abc.ABC):
    """
    BaseInfoParser class

    Attributes:
        url (str): Parsed url
    """

    url: str

    @classmethod
    def parse(
            cls: Type["BaseInfoParser"],
            html_code: str,
            page_url: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse news HTML page and get info

        Args:
            html_code (str): HTML page you want to parse
            page_url (Optional[str]): Page URL, used for relative URLs. Defaults by None

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]): News title, description and image URL
        """

        # Parse HTML to lxml tree
        html_tree = html.fromstring(html_code)

        # Parse news info and return
        return (
            cls._title(html_tree),
            cls._description(html_tree),
            cls._image(html_tree, page_url=page_url)
        )

    @staticmethod
    @abc.abstractmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:
        """
        Parse news HTML page and get title

        Args:
            html_tree (str): HTML page you want to parse

        Returns:
            Optional[str]: News title
        """

        pass

    @staticmethod
    @abc.abstractmethod
    def _description(html_tree: html.HtmlElement) -> Optional[str]:
        """
        Parse news HTML page and get description

        Args:
            html_tree (str): HTML page you want to parse

        Returns:
            Optional[str]: News description
        """

        pass

    @staticmethod
    @abc.abstractmethod
    def _image(html_tree: html.HtmlElement, page_url: Optional[str] = None) -> Optional[str]:
        """
        Parse news HTML page and get image

        Args:
            html_tree (str): HTML page you want to parse
            page_url (str): Page URL, used for relative URLs. Defaults by None

        Returns:
            Optional[str]: News image
        """

        pass


class MetaInfoParser(BaseInfoParser):
    """
    MetaInfoParser class. Parses page meta-data.
    Used if there are no parser for given url

    Attributes:
        url (str): Empty, so it could be parser for any url
    """

    url: str = ""

    @staticmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:

        # Get best (longest) title or empty if there are none
        title = max(
            html_tree.xpath('//title/text()') +  # Page title
            html_tree.xpath('//meta[@property="og:title" or @name="og:title"]/@content') +  # og title
            html_tree.xpath('//meta[@property="twitter:title" or @name="twitter:title"]/@content') +  # twitter title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        return title

    @staticmethod
    def _description(html_tree: html.HtmlElement) -> Optional[str]:

        # Get best (longest) description or empty if there are none
        description = max(
            html_tree.xpath('//div[@class="article-body"]//strong/text()') +  # Article description
            html_tree.xpath('//meta[@property="og:description" or @name="og:description"]/@content') +  # og description
            html_tree.xpath('//meta[@property="description" or @name="description"]/@content') +  # Page description
            html_tree.xpath('//meta[@name="twitter:description" or @property="twitter:description"]/@content') +
            [None],  # empty description
            key=lambda value: 0 if value is None else len(value)
        )

        return description

    @staticmethod
    def _image(html_tree: html.HtmlElement, page_url: Optional[str] = None) -> Optional[str]:

        # Get first image or empty if there are none
        image = list(
            html_tree.xpath('//meta[@property="og:image" or @name="og:image"]/@content') +
            html_tree.xpath('//meta[@name="twitter:image" or @property="twitter:image"]/@content') +
            [None]
        )[0]

        if image and not urlparse(image).netloc:
            # Image url is relative

            if page_url:
                # Add page url to create absolute url
                image = urlparse(page_url).scheme + "://" + urlparse(page_url).netloc + image

            else:
                # Page url is not provided
                image = None

        return image
