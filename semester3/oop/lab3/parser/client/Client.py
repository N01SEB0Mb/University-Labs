# coding=utf-8

import json
import requests
import datetime
from lxml import html
from math import ceil
from hashlib import md5
from pathlib import Path
from copy import deepcopy
from random import choice
from datetime import datetime
from time import strftime, time
from requests.packages.urllib3 import disable_warnings

from parser import CONFIG, BRANDS


class Client:
    name = "defaultclient"

    def __init__(self):

        self.codes = CONFIG["codes"]
        self.searchArt = CONFIG["parser"]["searchOnlyArticle"]
        self.timezone = "UTC" + strftime("%z")[:3] + ":" + strftime("%z")[3:]

        (Path(".") / CONFIG["parser"]["picturesPath"].format(self.name)).mkdir(exist_ok=True, parents=True)

        self.session = requests.session()
        self.session.headers.update(CONFIG["parser"]["headers"])
        self.session.verify = False
        self.timeout = CONFIG["parser"]["connectionTimeout"]

    def get_image(self, image_link, image_id):
        image = None
        image_request = self.session.get(image_link)
        if image_request.status_code == 200:
            with open(CONFIG["parser"]["picturesPath"].format(self.name) + "{0}.jpeg".format(image_id), "wb") as fp:
                fp.write(image_request.content)
                image = CONFIG["parser"]["picturesPath"].format(self.name) + "{0}.jpeg".format(image_id)
        return image

    def response_article(self, status, message, item=None):
        codes = [self.codes[codeType] for codeType in ["successful",
                                                       "notFound",
                                                       "connectionError",
                                                       "authorizationError"]]
        if item is None:
            item = []

        return {"code": codes[status], "result": item, "message": message}

    def response_brand(self, status, message, item=None):
        codes = [self.codes[codeType] for codeType in ["successful",
                                                       "notFound",
                                                       "connectionError",
                                                       "authorizationError"]]
        if item is None:
            item = dict()

        return {"code": codes[status], **item, "message": message}

    def response_currency(self, status, message, response=None):
        codes = [self.codes[codeType] for codeType in ["successful",
                                                       "notFound",
                                                       "connectionError",
                                                       "authorizationError"]]
        if response is None:
            response = dict()

        return {"code": codes[status], "response": response, "message": message}

    @classmethod
    def compare(cls, brand0, brand1):
        brand0, brand1 = cls.clear(brand0).upper(), cls.clear(brand1).upper()

        for brandVariants in BRANDS:
            if brand0 == brand1 or (brand0 in brandVariants and brand1 in brandVariants):
                return True
        else:
            return False

    @classmethod
    def compare_art(cls, search_article, item_article):
        check_article = [char for char in search_article.lower() if char.isalnum()]
        for char in item_article.lower():
            try:
                if char == check_article[0]:
                    check_article.pop(0)
            except IndexError:
                break
        return not bool(check_article)

    def get_currency(self):
        return self.response_currency(0, "Отримання курсу для сайта не реалізовано")

    @staticmethod
    def clear(string: str, delchars: str = "") -> str:
        """
        Clears string: removes unwanted spaces, html tags, specified and special characters

        Args:
            string (str): String you want to clear
            delchars (str): Characters you want to remove from string

        Returns:
            str: Cleared string

        Raises:
            TypeError: if 'string' argument type is not 'str'
        """

        if string is None:
            return ""
        elif not isinstance(string, str):
            raise TypeError(f"'string' argument type must be 'str', not '{string.__class__.__name__}'")

        for delstring in ["\n", "\t", "<b>", "</b>"]:
            string = string.replace(delstring, "")

        string = string.translate(
            str.maketrans(
                dict.fromkeys(delchars)
            )
        )

        if string:
            index = 1
            try:
                while string[0] == " ":
                    string = string[1:]
                while index < len(string) - 2:
                    if string[index] == string[index + 1] == " ":
                        string = string[:index] + string[index + 1:]
                    else:
                        index += 1
                if string:
                    while string[-1] == " ":
                        string = string[:-1]
            except IndexError:
                pass

        return string

    def search(self, article):
        if self.connected and self.logged:
            return self.response_article(0, "ОК")
        elif self.connected:
            return self.response_article(3, "Помилка авторизації")
        else:
            return self.response_article(2, "Помилка з'єднання")

    def get_info(self, article, brand):
        if self.connected and self.logged:
            return self.response_brand(0, "OK")
        elif self.connected:
            return self.response_brand(3, "Помилка авторизації")
        else:
            return self.response_brand(2, "Помилка з'єднання")

    @staticmethod
    def sign_in():
        return 1, 1
