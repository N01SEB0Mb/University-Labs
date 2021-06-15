# coding=utf-8
"""
This subpackage defines news scraper classes
"""

from .basescraper import BaseNewsScraper
from .ukrnet import UkrnetNewsScraper


__all__ = (
    "UkrnetNewsScraper",
)
