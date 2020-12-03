# coding=utf-8

from random import choice, uniform, randint

from .coordinates import LawCoordinates


class Law:
    MIN_COMPLEXITY = 1
    MAX_COMPLEXITY = 99

    def __init__(self, complexity: int) -> None:
        self.complexity = complexity


class IdeologyLaw(LawCoordinates, Law):
    def __init__(self, value: float, direction: str, complexity: int) -> None:
        super(IdeologyLaw, self).__init__(value, direction)

        self.complexity = complexity

    @classmethod
    def random(cls, direction: str = None):
        direction = direction if direction in (self.SOCIAL, self.ECONOMIC) else choice(self.SOCIAL, self.ECONOMIC)
        value = round(uniform(-1.0, 1.0), 3)

        return cls(value, direction, randint(cls.MIN_COMPLEXITY, cls.MAX_COMPLEXITY))


class ParlamentaryLaw(Law):
    SEATS_LAW = 0
    TIME_LAW = 1
    VOTES_LAW = 2

    MIN_SEATS_LAW = 50
    MAX_SEATS_LAW = 300

    MIN_TIME_LAW = 10
    MAX_TIME_LAW = 99

    MIN_VOTES_LAW = 0.33
    MAX_VOTES_LAW = 0.66

    def __init__(self,  lawtype: int, value: int, complexity: int) -> None:
        super(ParlamentaryLaw, self).__init__(complexity)

        self.lawtype = lawtype
        self.value = value

    @classmethod
    def random(cls, lawtype: int = None):
        lawtype = lawtype if lawtype in (
            cls.SEATS_LAW,
            cls.TIME_LAW,
            cls.VOTES_LAW
        ) else choice(
            cls.SEATS_LAW,
            cls.TIME_LAW,
            cls.VOTES_LAW
        )
        if lawtype == cls.SEATS_LAW:
            value = randint(cls.MIN_SEATS_LAW, cls.MAX_SEATS_LAW)
        elif lawtype == cls.TIME_LAW:
            value = randint(cls.MIN_TIME_LAW, cls.MAX_TIME_LAW)
        else:
            value = uniform(cls.MIN_VOTES_LAW, cls.MAX_VOTES_LAW)

        return cls(lawtype, value, randint(cls.MIN_COMPLEXITY, cls.MAX_COMPLEXITY))


class ElectoralLaw(Law):
    FREQUENCY_LAW = 0
    MAX_SEATS_LAW = 1
    MIN_SEATS_LAW = 2
    TIME_LAW = 3

    MIN_FREQUENCY_LAW = 100
    MAX_FREQUENCY_LAW = 1000

    MIN_MAX_SEATS_LAW = 50
    MAX_MAX_SEATS_LAW = 300

    MIN_MIN_SEATS_LAW = 2
    MAX_MIN_SEATS_LAW = 20

    MIN_TIME_LAW = 10
    MAX_TIME_LAW = 100

    def __init__(self, lawtype: int, value: int, complexity: int) -> None:
        super(ElectoralLaw, self).__init__(complexity)

        self.lawtype = lawtype
        self.value = value

    @classmethod
    def random(cls, lawtype: int = None):
        lawtype = lawtype if lawtype in (
            cls.FREQUENCY_LAW,
            cls.MAX_SEATS_LAW,
            cls.MIN_SEATS_LAW,
            cls.TIME_LAW
        ) else choice(
            cls.FREQUENCY_LAW,
            cls.MAX_SEATS_LAW,
            cls.MIN_SEATS_LAW,
            cls.TIME_LAW
        )

        if lawtype == cls.FREQUENCY_LAW:
            value = randint(cls.MIN_FREQUENCY_LAW, cls.MAX_FREQUENCY_LAW)
        elif lawtype == cls.MAX_SEATS_LAW:
            value = randint(cls.MIN_MAX_SEATS_LAW, cls.MAX_MAX_SEATS_LAW)
        elif lawtype == cls.MIN_SEATS_LAW:
            value = randint(cls.MIN_MIN_SEATS_LAW, cls.MAX_MIN_SEATS_LAW)
        elif lawtype == cls.TIME_LAW:
            value = randint(cls.MIN_TIME_LAW, cls.MAX_TIME_LAW)

        return cls(lawtype, value, randint(cls.MIN_COMPLEXITY, cls.MAX_COMPLEXITY))
