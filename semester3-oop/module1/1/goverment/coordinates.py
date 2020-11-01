# coding=utf-8

import json
from math import floor
from pathlib import Path


with (Path(__file__).resolve().parent / "data" / "ideologies.json").open("rt") as ideologiesFile:
    IDEOLOGIES = json.load(ideologiesFile)


class Coordinates:
    def __init__(self, economic: float, social: float) -> None:
        """
        Coordinates __init__ method override

        Args:
            economic (float, optional): economic value in range from -1.0 to 1.0
            social (float, optional): social value in range from -1.0 to 1.0

        Raises:
            TypeError: if 'economic' or 'social' is not number
        """

        self._economic = -1.0 if economic < -1.0 else 1.0 if economic > 1.0 else economic
        self._social = -1.0 if social < -1 else 1.0 if social > 1.0 else social

    @property
    def economic(self):
        return self._economic

    @economic.setter
    def economic(self, value):
        self._economic = -1.0 if value < -1.0 else 1.0 if value > 1.0 else value

    @property
    def social(self):
        return self._social

    @social.setter
    def social(self, value):
        self._social = -1.0 if value < -1 else 1.0 if value > 1.0 else value

    @property
    def __ideologyX(self) -> int:
        x = (self.economic + 1.0) * 0.5
        return floor((0.999 if x == 1 else x) * len(IDEOLOGIES[0]))

    @property
    def __ideologyY(self) -> int:
        y = (self.social + 1.0) * 0.5
        return floor((0.999 if y == 1 else y) * len(IDEOLOGIES))

    def __str__(self) -> str:
        return IDEOLOGIES[self.__ideologyY][self.__ideologyY]

    def __repr__(self) -> str:
        return f"({self.economic}, {self.social})"


class LawCoordinates(Coordinates):
    def __init__(self, value: float, direction: str) -> None:
        if direction == "economic":
            super(LawCoordinates, self).__init__(value, 0.0)
        elif direction == "social":
            super(LawCoordinates, self).__init__(0.0, value)
        else:
            raise ValueError("'direction' value must be 'economic' or 'social'")

        self._direction = direction

    @property
    def direction(self) -> str:
        return self._direction

    @direction.setter
    def direction(self, value: str) -> None:
        if value in ("economic", "social"):
            self._direction = value
        else:
            raise ValueError("Direction must be 'economic' or 'social'")

    @property
    def economic(self) -> float:
        return self._economic

    @economic.setter
    def economic(self, value: float) -> None:
        if self._direction == "economic":
            self._economic = -1.0 if value < -1.0 else 1.0 if value > 1.0 else value
        else:
            raise ValueError("Law is 'social', you can't change 'economic' value")

    @property
    def social(self) -> float:
        return self._social

    @social.setter
    def social(self, value: float) -> None:
        if self._direction == "social":
            self._social = -1.0 if value < -1.0 else 1.0 if value > 1.0 else value
        else:
            raise ValueError("Law is 'economic', you can't change 'social' value")
