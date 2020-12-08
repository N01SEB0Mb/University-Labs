# coding=utf-8

from .Client import *
from .ResponseItem import *

from parser.client.AsiaParts.client import AsiaParts
from parser.client.AutoLider.client import AutoLider
from parser.client.AutoTechnics.client import AutoTechnics
from parser.client.Busmarket.client import Busmarket
from parser.client.Direct24.client import Direct24
from parser.client.FormParts.client import FormParts
from parser.client.InterCars.client import InterCars
from parser.client.Mahina.client import Mahina
from parser.client.MasterService.client import MasterService
from parser.client.MaxiElit.client import MaxiElit
from parser.client.OmegaAuto.client import OmegaAuto
from parser.client.XPertAuto.client import XPertAuto


disable_warnings()


CLIENT_CLASSES = {
    AsiaParts,
    AutoLider,
    AutoTechnics,
    Busmarket,
    Direct24,
    FormParts,
    InterCars,
    Mahina,
    MaxiElit,
    MasterService,
    OmegaAuto,
    XPertAuto
}
