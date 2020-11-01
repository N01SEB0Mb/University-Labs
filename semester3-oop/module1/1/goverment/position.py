# coding=utf-8

from .law import Law
from .coordinates import Coordinates


class Position(Coordinates):
    IDEOLOGY_DELTA = 0.3

    def __init__(self, economic: float, social: float) -> None:
        super(Position, self).__init__(economic, social)

        self.__good = list()
        self.__bad = list()

    def __contains__(self, law: Law) -> bool:
        if isinstance(law, Law):
            if law.direction == "economic":
                return abs(law.economic - self.economic) <= self.IDEOLOGY_DELTA
            else:
                return abs(law.social - self.social) <= self.IDEOLOGY_DELTA
        else:
            raise TypeError(f"'{self.__class__.__name__}' class does not support"
                            f"operator 'in' for '{law.__class__.__name__}'")
