# coding=utf-8
"""
This subpackage stores news pages parsers
"""

from typing import List, Type

from .base import BaseInfoParser, MetaInfoParser


# Define list of available parser classes
PARSER_CLASSES: List[Type[BaseInfoParser]] = [
    MetaInfoParser
]


# Define public attributes of the package
__all__ = (
    "MetaInfoParser",
    "PARSER_CLASSES"
)
