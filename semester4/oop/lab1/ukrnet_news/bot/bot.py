# coding=utf-8

from typing import *
from aiogram import Bot

from ukrnet_news.scraper import BaseNewsScraper, UkrnetNewsScraper


class UkrnetNewsBot(Bot):
    """
    UkrnetNewsBot class
    """

    __slots__ = ("__scraper",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        UkrnetNewBot initializing

        Args:
            *args (Any): aiogram.Bot *args
            **kwargs (Any): aiogram.Bot **kwargs
        """

        super(UkrnetNewsBot, self).__init__(*args, **kwargs)

        # Initialize news scraper

        self.__scraper: BaseNewsScraper = UkrnetNewsScraper()
