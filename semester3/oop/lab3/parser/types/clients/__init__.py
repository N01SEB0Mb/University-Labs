# coding=utf-8

from .baseclient import BaseClient

from parser.types.clients.AsiaParts.client import AsiaParts
from parser.types.clients.AutoLider.client import AutoLider
from parser.types.clients.AutoTechnics.client import AutoTechnics
from parser.types.clients.Busmarket.client import Busmarket
from parser.types.clients.Direct24.client import Direct24
from parser.types.clients.FormParts.client import FormParts


CLIENT_CLASSES = {
    AsiaParts,
    AutoLider,
    AutoTechnics,
    Busmarket,
    Direct24,
    FormParts
}
