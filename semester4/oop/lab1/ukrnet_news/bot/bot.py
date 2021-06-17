# coding=utf-8

import json
import time
import traceback
from typing import *
from pathlib import Path
from aiogram import Bot
from aiogram.utils.markdown import bold, link

from ukrnet_news.config import CONFIG, TELEGRAM
from ukrnet_news.scraper import BaseNewsScraper, UkrnetNewsScraper, News


class UkrnetNewsBot(Bot):
    """
    UkrnetNewsBot class

    Attributes:
        news_path (Path): News cache file path
    """

    news_path: Path = Path().resolve() / "cache" / "news.json"

    __slots__ = ("__scraper", "__news")

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

        # Load last news from file
        self.__news: List[News] = []
        self.__load_news()

    async def refresh_news(self) -> None:
        """
        Refreshing news stream (checking for new articles)
        """

        # Get news
        news = list(self.__scraper.get_news("auto"))

        # Define list of news to be posted
        to_post = []

        # Filter only latest news
        for new in news:
            for existing_new in self.__news:
                # Check if news equal
                if new.id == existing_new.id:
                    break
            else:
                # No equal news found
                to_post.append(new)

        # Update and save existing news
        self.__news = news
        self.__save_news()

        # Post newly found news
        await self.__post(*to_post)

    async def __post(self, *news: News) -> None:
        """
        Posting latest news

        Args:
            *news (News): News you want to post
        """

        # Iterate all news
        for new in news:
            # Check if image exists

            if new.image_url:
                # Has image

                await self.send_photo(
                    chat_id=TELEGRAM["channel"]["id"],
                    photo=str(new.image_url),
                    caption=self.__format_news(new),
                    parse_mode="Markdown"
                )

            elif CONFIG["news"]["post_no_image"]:
                # Has no image, but posting is allowed

                await self.send_message(
                    chat_id=TELEGRAM["channel"]["id"],
                    text=self.__format_news(new),
                    parse_mode="Markdown"
                )

            else:
                continue

            # Sleep for configured interval
            time.sleep(CONFIG["news"]["posting_interval"])

    def __load_news(self, filepath: Path = news_path) -> None:
        """
        Load news from file

        Args:
            filepath (Path): News cache file path
        """

        if not filepath.exists():
            # News file not exists => return load empty list
            self.__news = []

        else:
            with filepath.open("rb") as news_file:
                # Load news
                self.__news = [
                    News.from_dict(news) for news in json.loads(
                        news_file.read().decode("utf-8")
                    )
                ]

    def __save_news(self, filepath: Path = news_path) -> None:
        """
        Save news to file

        Args:
            filepath (Path): News cache file path
        """

        if not filepath.exists():
            # Create directories if not exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

        with filepath.open("wb") as news_file:
            # Save news
            news_file.write(
                json.dumps(
                    [news.to_dict() for news in self.__news],
                    indent=2,
                    ensure_ascii=True
                ).encode("utf-8")
            )

    @staticmethod
    def __format_news(news: News) -> str:
        """
        Format news into text message

        Args:
            news (News): News you want to format

        Returns:
            str: News text
        """

        return "\n\n".join([
            bold(news.title),
            news.description,
            link("Подробнее", news.url)
        ])
