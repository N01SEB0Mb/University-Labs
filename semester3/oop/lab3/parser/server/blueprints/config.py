# coding=utf-8

import time
from flask_api import status
from flask import Blueprint, request

from parser.server.funcs import *
from parser.funcs import *


configRoute = Blueprint(
    "configuration",
    __name__,
    url_prefix="/parser"
)
