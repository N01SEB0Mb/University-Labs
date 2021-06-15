# coding=utf-8

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

    def get_news(self, category: str) -> Generator[News, None, None]:
        """
        Get latest news from specified category

        Attributes:
            category (str): Name of category

        Yields:
            News: Last news from specified category
        """

        # Request latest news
        news_request = self.get(
            self.Links.get_news.format(category),
            timeout=self.timeout
        )

        if news_request.status_code != 200:
            # News request failed
            return []

        # Iterate found news
        for news in news_request.json()["tops"]:
            try:
                # Try yielding news
                yield News.from_url(
                    news["Url"],
                    news_id=news["NewsId"],
                    dups=None if "Dups" not in news else list(map(lambda dup: dup["NewsId"], news["Dups"]))
                )

            except BaseException:
                # Some error occured
                pass
