# coding=utf-8
"""
Package goverment provides political object for simulating democracy system
"""

from .party import Party
from .elector import Elector
from .position import Position
from .parlament import Parlament
from .coordinates import Coordinates, LawCoordinates
from .law import Law, ElectoralLaw, IdeologyLaw, ParlamentaryLaw

__author__ = "Tiron Mykhailo"
__version__ = "1.0.0"
__date__ = "01.11.2020"

__all__ = [
    "Law",
    "Party",
    "Elector",
    "Position",
    "Parlament",
    "IdeologyLaw",
    "Coordinates",
    "ElectoralLaw",
    "LawCoordinates",
    "ParlamentaryLaw",
]
