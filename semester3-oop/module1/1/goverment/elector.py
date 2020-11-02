# coding=utf-8

from random import randint
from typing import List

from .law import Law
from .party import Party
from .position import Position


class Elector(Position):
    IDEOLOGICAL = 0
    ACTIVE = 1
    RANDOM = 2

    def __init__(
            self,
            economic: float,
            social: float,
            name: str,
            age: int,
            strategy: int = IDEOLOGICAL
    ) -> None:
        super(Elector, self).__init__(economic, social)

        self.name = name
        self.age = age
        self.strategy = strategy

    def checkParty(self, party: Party) -> int:
        number = 0

        for law in self.good:
            if law in party.good:
                number += 1
            elif law in party.bad:
                number -= 1

        for law in self.bad:
            if law in party.bad:
                number += 1
            elif law in party.good:
                number -= 1

        return number

    def chooseParty(self, partyList: List[Party]) -> int:
        if self.strategy == self.IDEOLOGICAL:
            bestParty = 0

            for number, party in partyList:
                if self.checkParty(party) > self.checkParty(partyList[bestParty]):
                    bestParty = number

            return bestParty
        elif self.strategy == self.ACTIVE:
            for number, party in partyList:
                if party.active:
                    return number
            else:
                return 0
        elif self.strategy == self.RANDOM:
            return randint(0, len(partyList) - 1)
