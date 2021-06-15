# coding=utf-8
"""
This subpackage stores project configurations
"""

from .load import load_json


CONFIG:   dict = load_json("config.json")
TELEGRAM: dict = load_json("telegram.json")


__all__ = (
    "CONFIG",
    "TELEGRAM",
)
