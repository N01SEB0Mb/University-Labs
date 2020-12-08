# coding=utf-8
"""
This package used to store config files

Attributes:
    CONFIG (dict): Configuration
    SERVER (dict): Server settings
    PARSER (dict): Parser (client) settings
    BRANDS (dict): List of equal brands
    STATUS (dict): Response status config
"""

import json
from pathlib import Path
from typing import Optional


def loadJSON(
        filename: str,
        dirpath: Optional[Path] = Path(__file__).resolve().parent
) -> dict:
    """
    Used to load json file to dict from specified path

    Args:
        filename (str): Name of json file (without ".json")
        dirpath (Optional[Path]): Path to file. Default path is "data/"

    Returns:
        dict: Loaded json

    Raises:
        FileNotFoundError: If no such file or directory
    """

    with (dirpath / "{}.json".format(filename)).open("rt", encoding="utf-8") as jsonFile:
        return json.load(jsonFile)


CONFIG = loadJSON("data/config")
SERVER = loadJSON("data/server")
PARSER = loadJSON("data/parser")
BRANDS = loadJSON("data/brands")
STATUS = loadJSON("data/status")
