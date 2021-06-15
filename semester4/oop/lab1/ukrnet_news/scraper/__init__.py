# coding=utf-8
"""
This subpackage defines news scraper classes
"""

from .basescraper import BaseNewsScraper
from .ukrnet import UkrnetNewsScraper
from .news import News


__all__ = (
    "News",
    "UkrnetNewsScraper",
)
