# coding=utf-8
"""
This subpackage stores project configurations
"""

from .load import load_json


CONFIG:    dict = load_json("config.json")  # Package config
TELEGRAM:  dict = load_json("telegram.json")  # Bot config
BLACKLIST: frozenset = frozenset(load_json("blacklist.json"))  # Blacklisted sites (not supported)

__all__ = (
    "CONFIG",
    "TELEGRAM",
    "BLACKLIST"
)
