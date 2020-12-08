# coding=utf-8

import time
from flask import Flask
from typing import Any, Set, Type, Optional

from topauto_parser.funcs import login
from topauto_parser.config import SERVER
from topauto_parser.types.clients import CLIENT_CLASSES, BaseClient


class ParserServer(Flask):
    """
    Parser server that contains clients. Inherits Flask

    Attributes:
        host (str): Server host
        port (str): Server port
        threading (bool): Is server threading enabled

        autoAuth (bool): Is auto-authorization enabled
        autoAuthHour (int): Auto-authorization hour
        autoAuthMinute (int): Auto-authorization minute

        clients (List[BaseClient]): List of clients
    """

    host = SERVER["host"]
    port = SERVER["port"]
    threaded = SERVER["threaded"]

    autoAuth = SERVER["autoAuth"]["enabled"]
    autoAuthHour = SERVER["autoAuth"]["hour"]
    autoAuthMinute = SERVER["autoAuth"]["minute"]

    def __init__(
            self,
            *args: Any,
            clientClasses: Optional[Set[Type[BaseClient]]] = CLIENT_CLASSES,
            **kwargs: Any
    ):
        """
        Flask __init__ method override. Initializes Flask app and clients list

        Args:
            *args (Any): Flask.__init__() *args
            **kwargs (Any): Flask.__init__() **kwargs
        """

        self.clients = login(clientClasses)

        super(ParserServer, self).__init__(
            *args,
            **kwargs
        )

    def run(
            self,
            *args: Any,
            **kwargs: Any
    ) -> None:
        kwargs = {
            "host": self.host,
            "port": self.port,
            "threaded": self.threaded,
            **kwargs
        }

        super(ParserServer, self).run(
            *args,
            **kwargs
        )

    @property
    def day(self):
        return int(time.strftime("%j"))

    @property
    def hour(self):
        return int(time.strftime("%H"))

    @property
    def minute(self):
        return int(time.strftime("%M"))
