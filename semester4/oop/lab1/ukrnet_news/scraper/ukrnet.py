# coding=utf-8

import logging
import traceback
from typing import *

from .news import News
from .basescraper import BaseNewsScraper


class UkrnetNewsScraper(BaseNewsScraper):
    """
    UkrnetNewsScraper class. Used for scraping news from https://ukr.net/
    """

    class Links:
        """
        Storing Ukrnet links that are used for scraping
        """

        get_news = "https://www.ukr.net/news/dat/{}/"

    def get_news(self, category: str) -> Generator[Dict, None, None]:
        """
        Get latest news from specified category

        Attributes:
            category (str): Name of category

        Yields:
            News: Last news from specified category
        """

        # Request latest news
        logging.info(f"Getting latest news ({category})")
        news_request = self.get(
            self.Links.get_news.format(category),
            timeout=self.timeout
        )

        if news_request.status_code != 200:
            # News request failed
            return None

        logging.info(f"Found {len(news_request.json()['tops'])} news")

        # Iterate found news
        for number, news in enumerate(news_request.json()["tops"]):
            if "News" in news:
                # Get first news from list
                news = news["News"][0]

            # Yield found news
            yield {
                "id": news["NewsId"],
                "url": news["Url"],
                "dups": [] if "Dups" not in news else list(map(lambda dup: dup["NewsId"], news["Dups"]))
            }
