# coding=utf-8

from random import choice, uniform, randint

from .coordinates import LawCoordinates


class Law(LawCoordinates):
    def __init__(self, value: float, direction: str, text: str, number: int) -> None:
        super(Law, self).__init__(value, direction)

        self.text = text
        self.number = number

    @classmethod
    def random(cls, direction: str = None) -> Law:
        value = round(uniform(-1.0, 1.0), 3)
        direction = direction if direction in ("social", "economic") else choice("social", "economic")

        return cls(value, direction, "some text", randint(1, 9999))
