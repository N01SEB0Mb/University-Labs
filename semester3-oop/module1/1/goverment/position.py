# coding=utf-8

from random import randint
from typing import Union

from .law import IdeologyLaw, ParlamentaryLaw, ElectoralLaw
from .coordinates import Coordinates


class Position(Coordinates):
    IDEOLOGY_DELTA = 0.3

    def __init__(self, economic: float, social: float) -> None:
        super(Position, self).__init__(economic, social)

        self.good = list()
        self.bad = list()

    def __contains__(self, law: Law) -> bool:
        if isinstance(law, Law):
            if law.direction == law.ECONOMIC:
                return abs(law.economic - self.economic) <= self.IDEOLOGY_DELTA
            else:
                return abs(law.social - self.social) <= self.IDEOLOGY_DELTA
        else:
            raise TypeError(f"'{self.__class__.__name__}' class does not support"
                            f"operator 'in' for '{law.__class__.__name__}'")

    def addLaw(self, law: Union[IdeologyLaw, ParlamentaryLaw, ElectoralLaw]) -> bool:
        if isinstance(law, IdeologyLaw):
            result = law in self
        else:
            result = not randint(0, 1)

        self.good.append(law) if result else self.bad.append(law)
        return result
