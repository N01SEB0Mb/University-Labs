# coding=utf-8

from random import randint
from typing import List

from .law import Law
from .party import Party
from .position import Position


class Elector(Position):
    def __init__(
            self,
            economic: float,
            social: float,
            name: str,
            age: int,
            strategy: int = 1
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
        bestParty = 0

        for number, party in partyList:
            if self.checkParty(party) > self.checkParty(partyList[bestParty]):
                bestParty = number

        return bestParty
