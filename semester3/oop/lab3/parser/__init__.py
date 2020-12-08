# coding=utf-8

import json
from pathlib import Path


with (Path(__file__).resolve().parent / "config.json").open("rt", encoding="utf-8") as configFile:
    CONFIG = json.load(configFile)

with (Path(__file__).resolve().parent / "brands.json").open("rt", encoding="cp1251") as brandsFile:
    BRANDS = json.load(brandsFile)
