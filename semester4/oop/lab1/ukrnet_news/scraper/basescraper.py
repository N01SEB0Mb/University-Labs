# coding=utf-8

import abc
import requests
from typing import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from ukrnet_news.config import CONFIG


# Disable InsecureRequestWarning (Unverified HTTPS)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BaseNewsScraper(requests.Session, abc.ABC):
    """
    BaseNewsScraper class

    Attributes:
        timeout (int): Connection timeout
    """

    timeout: int = CONFIG["connection"]["timeout"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        BaseNewsScraper initializing

        Args:
            *args (Any): requests.Session *args
            **kwargs (Any): requests.Session **kwargs
        """

        super(BaseNewsScraper, self).__init__(*args, **kwargs)

        # Add configured headers
        self.headers.update(CONFIG["connection"]["headers"])

        # Disable SSL verify
        self.verify = False

    @abc.abstractmethod
    def get_news(self, category: str) -> Generator[Dict, None, None]:
        """
        Get last news from specified category

        Attributes:
            category (str): Name of category

        Yields:
            Dict: Last news from specified category
        """

        pass
