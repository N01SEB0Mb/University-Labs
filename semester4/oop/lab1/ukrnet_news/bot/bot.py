# coding=utf-8

import json
import time
import logging
import traceback
import requests.exceptions

from typing import *
from pathlib import Path
from aiogram import Bot
from aiogram.utils.markdown import bold, link
from aiogram.utils.exceptions import RetryAfter, WrongFileIdentifier, BadRequest

from ukrnet_news.config import CONFIG, TELEGRAM
from ukrnet_news.scraper import BaseNewsScraper, UkrnetNewsScraper, News
from ukrnet_news.exceptions import ParserNotFoundError, EmptyNewsError, InBlacklistError


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
        to_get = []

        # Filter only latest news
        for new in news:
            for existing_new in self.__news:
                # Check if news equal
                if new["id"] == existing_new["id"]:
                    break

                # Check if news are dups
                if new["id"] in existing_new["dups"] or existing_new["id"] in new["dups"]:
                    break
            else:
                # No equal news found
                to_get.append(new)

        # Update and save existing news
        self.__news = [{
            "id": new["id"],
            "dups": new["dups"]
        } for new in news]

        self.__save_news()

        # Get info about newly found news
        to_post = self.__get_news(to_get)

        # Post newly found news
        await self.__post(*to_post)

    def __get_news(self, news: List[Dict[str, Any]]) -> Generator[News, None, None]:
        """
        Get info about latest news

        Args:
            news (List[Dict[str, Any]]): News, info of which you want to get

        Yields:
            News: News object
        """

        # Log number of news
        logging.info(f"News to get: {len(news)}")

        # Iterating news
        for number, new in enumerate(news):
            # Trying to get info about news
            try:
                # Log current request
                logging.info(f"Get ({number + 1}/{len(news)}): <id={new['id']}> <url={new['url']}>")

                # Yield info about news
                yield News.from_url(
                    new["url"],
                    news_id=new["id"],
                    dups=new["dups"]
                )

            except InBlacklistError:
                # URL is blacklisted
                logging.warning("Given URL is in the blacklist")

            except ParserNotFoundError:
                # Could not find parser for given URL
                logging.error("Could not find parser for given URL")

            except EmptyNewsError:
                # Could not get news info (title or description)
                logging.error("Could not get info (title or description)")

            except requests.exceptions.Timeout:
                # Page request timeout expired
                logging.error(f"Connection timeout expired")

            except requests.exceptions.RequestException as request_error:
                # Could not get page
                logging.error(str(request_error))

            except BaseException:
                # Some error occured
                logging.error(traceback.format_exc())

    async def __post(self, *news: News) -> None:
        """
        Posting latest news

        Args:
            *news (News): News you want to post
        """

        # Log number of news
        logging.info(f"News to post: {len(news)}")

        # Iterate all news
        for number, new in enumerate(news):

            logging.info(f"Posting ({number + 1}/{len(news)}): <id={new.id}> <url={new.url}>")

            # Trying to post news
            try:

                # Check if image exists
                if new.image_url:
                    # Has image
                    await self.send_photo(
                        chat_id=TELEGRAM["channel"]["id"],
                        photo=str(new.image_url),
                        caption=self.__format_news(new),
                        parse_mode="Markdown"
                    )

                else:
                    # Has no image
                    logging.warning("No image")

                    if CONFIG["news"]["post_no_image"]:
                        # Posting is allowed
                        await self.send_message(
                            chat_id=TELEGRAM["channel"]["id"],
                            text=self.__format_news(new),
                            parse_mode="Markdown"
                        )
                    else:
                        continue

            except WrongFileIdentifier:
                # Invalid image URL
                logging.warning(f"Invalid image URL specified: '{new.image_url}'")

            except BadRequest:
                # Wrong image type
                logging.warning(f"Invalid image type provided: '{new.image_url}'")

            except RetryAfter:
                # Flood control (retry after 16 seconds)
                logging.info("Flood control: retry after 16 seconds")
                time.sleep(16)

            except BaseException:
                # Some exception occured
                logging.error(traceback.format_exc())

            else:
                # Sleep for configured interval
                time.sleep(CONFIG["news"]["posting_interval"])

    def __load_news(self, filepath: Path = news_path) -> None:
        """
        Load news from file

        Args:
            filepath (Path): News cache file path
        """

        logging.info(f"Loading recent news from '{filepath}'")

        if not filepath.exists():
            # News file not exists => return load empty list
            self.__news = []

        else:
            with filepath.open("rb") as news_file:
                # Load news
                self.__news = json.loads(news_file.read().decode("utf-8"))

    def __save_news(self, filepath: Path = news_path) -> None:
        """
        Save news to file

        Args:
            filepath (Path): News cache file path
        """

        logging.info(f"Saving recent news to '{filepath}'")

        if not filepath.exists():
            # Create directories if not exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

        with filepath.open("wb") as news_file:
            # Save news
            news_file.write(
                json.dumps(
                    self.__news,
                    indent=2,
                    ensure_ascii=False
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
