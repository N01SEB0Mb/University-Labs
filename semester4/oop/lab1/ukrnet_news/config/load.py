# coding=utf-8

import json
from typing import *
from pathlib import Path


def load_json(filename: str, dirpath: Path = Path(__file__).resolve().parent) -> Dict[str, Any]:
    """
    Used to load json file to dict from specified path

    Args:
        filename (str): Name of json file
        dirpath (Optional[Path]): Path to file. Default path is "config/"

    Returns:
        Dict[str, Any]: Loaded json

    Raises:
        FileNotFoundError: If no such file or directory
    """

    with (dirpath / filename).open("rt", encoding="utf-8") as json_file:
        return json.load(json_file)
