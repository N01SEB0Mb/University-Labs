# coding=utf-8
"""
This subpackage stores news pages parsers
"""

from typing import List, Type

from .base import BaseInfoParser, MetaInfoParser
from .sites import *


# Define list of available parser classes
PARSER_CLASSES: List[Type[BaseInfoParser]] = [
    BizuaInfoParser,
    UAMotorsInfoParser,
    AutoPoradyInfoParser,
    MetaInfoParser
]


# Define public attributes of the package
__all__ = (
    "BizuaInfoParser",
    "UAMotorsInfoParser",
    "AutoPoradyInfoParser",
    "MetaInfoParser",
    "PARSER_CLASSES"
)
