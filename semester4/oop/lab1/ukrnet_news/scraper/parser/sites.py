# coding=utf-8

from typing import *
from lxml import html

from .base import BaseInfoParser


class BizuaInfoParser(BaseInfoParser):
    """
    BizuaInfoParser class. Parses news info from https://bizua.org/
    """

    url: str = "bizua.org"

    @staticmethod
    def parse(html_code: str, *args, **kwargs) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse https://bizua.org/ news and gets info

        Args:
            html_code (str): HTML page you want to parse

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]): News title, description and image URL
        """

        # Parse HTML to lxml tree
        html_tree = html.fromstring(html_code)

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="entry-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        # Get news description
        description = "\n\n".join(html_tree.xpath('//div[@class="entry-content"]/p/text()'))  # News description

        # Get news image
        image = list(
            html_tree.xpath('//div[@class="meta-image"]/img/@src') +  # News description
            [None],  # empty title
        )[0]

        return title, description, image


class UAMotorsInfoParser(BaseInfoParser):
    """
    UAMotorsInfoParser class. Parses news info from https://uamotors.com.ua/
    """

    url: str = "uamotors.com.ua"

    @staticmethod
    def parse(html_code: str, *args, **kwargs) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse https://uamotors.com.ua/ news and gets info

        Args:
            html_code (str): HTML page you want to parse

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]): News title, description and image URL
        """

        # Parse HTML to lxml tree
        html_tree = html.fromstring(html_code)

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="entry-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        # Get news description
        description = "\n \n".join(html_tree.xpath('//div[@class="post-fulltext"]/p/text()'))  # News description

        # Get news image
        image = list(
            html_tree.xpath('//meta[@property="og:image"]/@content') +  # Meta image
            [None],  # empty image
        )[0]

        return title, description, image


class AutoPoradyInfoParser(BaseInfoParser):
    """
    AutoPoradyInfoParser class. Parses news info from https://autoporady.com/
    """

    url: str = "autoporady.com"

    @staticmethod
    def parse(html_code: str, *args, **kwargs) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse https://autoporady.com/ news and gets info

        Args:
            html_code (str): HTML page you want to parse

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]): News title, description and image URL
        """

        # Parse HTML to lxml tree
        html_tree = html.fromstring(html_code)

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="entry-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        # Get news description
        description = "\n \n".join(html_tree.xpath('//div[@class="td-post-content tagdiv-type"]/*'
                                                   '[not(self::div)]/text()'))  # News description

        # Get news image
        image = list(
            html_tree.xpath('//meta[@property="og:image"]/@content') +  # Meta image
            [None],  # empty image
        )[0]

        return title, description, image


class USIOnlineInfoParser(BaseInfoParser):
    """
    AutoPoradyInfoParser class. Parses news info from https://usionline.com/
    """

    url: str = "usionline.com"

    @staticmethod
    def parse(html_code: str, *args, **kwargs) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse https://autoporady.com/ news and gets info

        Args:
            html_code (str): HTML page you want to parse

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]): News title, description and image URL
        """

        # Parse HTML to lxml tree
        html_tree = html.fromstring(html_code)

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="single-post_title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        # Get news description
        description = "\n \n".join(html_tree.xpath(
            '//div[@class="single-post__desc" or @class="single-post__content wysiwyg"]//text()'
        ))  # News description

        # Get news image
        image = list(
            html_tree.xpath('//meta[@property="og:image"]/@content') +  # Meta image
            [None],  # empty image
        )[0]

        return title, description, image
