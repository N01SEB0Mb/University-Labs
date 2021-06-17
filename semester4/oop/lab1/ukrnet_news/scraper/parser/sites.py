# coding=utf-8

from typing import *
from lxml import html

from .base import MetaInfoParser


class BizuaInfoParser(MetaInfoParser):
    """
    BizuaInfoParser class. Parses news info from https://bizua.org/
    """

    url: str = "bizua.org"

    @staticmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="entry-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        return title

    @staticmethod
    def _description(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news description
        description = "\n\n".join(html_tree.xpath('//div[@class="entry-content"]/p/text()'))  # News description

        return description

    @staticmethod
    def _image(html_tree: html.HtmlElement, page_url: Optional[str] = None) -> Optional[str]:

        # Get news image
        image = list(
            html_tree.xpath('//div[@class="meta-image"]/img/@src') +  # News description
            [None],  # empty title
        )[0]

        return image


class UAMotorsInfoParser(MetaInfoParser):
    """
    UAMotorsInfoParser class. Parses news info from https://uamotors.com.ua/
    """

    url: str = "uamotors.com.ua"

    @staticmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="entry-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        return title

    @staticmethod
    def _description(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news description
        description = "\n \n".join(html_tree.xpath('//div[@class="post-fulltext"]/p/text()'))  # News description

        return description


class AutoPoradyInfoParser(MetaInfoParser):
    """
    AutoPoradyInfoParser class. Parses news info from https://autoporady.com/
    """

    url: str = "autoporady.com"

    @staticmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="entry-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        return title

    @staticmethod
    def _description(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news description
        description = "\n \n".join(html_tree.xpath(
            '//div[@class="td-post-content tagdiv-type"]/*'
            '[not(self::div)]/text()')
        )

        return description


class USIOnlineInfoParser(MetaInfoParser):
    """
    USIOnlineInfoParser class. Parses news info from https://usionline.com/
    """

    url: str = "usionline.com"

    @staticmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news title
        title = max(
            html_tree.xpath('//h1[@class="single-post_title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        return title

    @staticmethod
    def _description(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news description
        description = "\n \n".join(html_tree.xpath(
            '//div[@class="single-post__desc" or @class="single-post__content wysiwyg"]//text()'
        ))

        return description


class AutoDreamInfoParser(MetaInfoParser):
    """
    AutoDreamInfoParser class. Parses news info from https://usionline.com/
    """

    url: str = "avtodream.org"

    @staticmethod
    def _title(html_tree: html.HtmlElement) -> Optional[str]:

        # Get news title
        title = max(
            html_tree.xpath('//h1[@id="news-title"]/text()') +  # News title
            [None],  # empty title
            key=lambda value: 0 if value is None else len(value)
        )

        return title
