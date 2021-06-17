# coding=utf-8

import logging
import traceback
import requests.exceptions
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
        logging.info(f"Getting latest news ({category})")
        news_request = self.get(
            self.Links.get_news.format(category),
            timeout=self.timeout
        )

        if news_request.status_code != 200:
            # News request failed
            return None

        # Iterate found news
        for number, news in enumerate(news_request.json()["tops"]):
            try:
                if "News" in news:
                    # Get first news from list
                    news = news["News"][0]

                # Log current request
                logging.info(f"Get ({number + 1}/{len(news_request.json()['tops'])}): "
                             f"<id={news['NewsId']}> <url={news['Url']}>")

                # Try yielding news
                yield News.from_url(
                    news["Url"],
                    news_id=news["NewsId"],
                    dups=None if "Dups" not in news else list(map(lambda dup: dup["NewsId"], news["Dups"]))
                )

            except KeyError:
                # URL is blacklisted
                logging.warning("Given URL is in the blacklist")

            except ModuleNotFoundError:
                # Could not find parser for given URL
                logging.error("Could not find parser for given URL")

            except ValueError:
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
