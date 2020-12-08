# coding=utf-8

from .baseclient import BaseClient

from topauto_parser.types.clients.AsiaParts.client import AsiaParts
from topauto_parser.types.clients.AutoLider.client import AutoLider
from topauto_parser.types.clients.AutoTechnics.client import AutoTechnics
from topauto_parser.types.clients.Busmarket.client import Busmarket
from topauto_parser.types.clients.Direct24.client import Direct24
from topauto_parser.types.clients.FormParts.client import FormParts


CLIENT_CLASSES = {
    AsiaParts,
    AutoLider,
    AutoTechnics,
    Busmarket,
    Direct24,
    FormParts
}
