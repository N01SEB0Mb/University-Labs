# coding=utf-8

from typing import Union, List

from .law import *
from .party import Party
from .elector import Elector


class Parlament:
    PARLAMENT_SEATS = 200
    LAW_APPLY_TIME = 10
    MIN_VOTES_TO_APPLY = 0.5

    ELECTIONS_FREQUENCY = 500
    ELECTIONS_TIME = 50
    MAX_PARTY_SEATS = 50
    MIN_PARTY_SEATS = 5

    def __init__(self):
        self.time = 0

        self.__laws = list()
        self.__parties = dict()

    def __getitem__(self, item):
        print(item)

    @property
    def laws(self) -> list:
        return self.__laws

    def voteLaw(self, law: Union[IdeologyLaw, ParlamentaryLaw, ElectoralLaw]) -> bool:
        self.time += law.complexity

        votes = sum(party.addLaw(law) * seats for party, seats in self.__parties)

        if self.MIN_VOTES_TO_APPLY <= votes / self.PARLAMENT_SEATS:
            self.__laws.append(law)
            self.__applyLaw(law)
            return True

        return False

    def __applyLaw(self, law: Union[IdeologyLaw, ParlamentaryLaw, ElectoralLaw]) -> None:
        self.time += self.LAW_APPLY_TIME

        if isinstance(law, ParlamentaryLaw):
            if law.lawtype == ParlamentaryLaw.SEATS_LAW:
                self.PARLAMENT_SEATS = law.value
            elif law.lawtype == ParlamentaryLaw.TIME_LAW:
                self.LAW_APPLY_TIME = law.value
            elif law.lawtype == ParlamentaryLaw.VOTES_LAW:
                self.MIN_VOTES_TO_APPLY = law.value

        elif isinstance(law, ElectoralLaw):
            if law.lawtype == ElectoralLaw.FREQUENCY_LAW:
                self.ELECTIONS_FREQUENCY = law.value
            elif law.lawtype == ElectoralLaw.MAX_SEATS_LAW:
                self.MAX_PARTY_SEATS = law.value
            elif law.lawtype == ElectoralLaw.TIME_LAW:
                self.LAW_APPLY_TIME = law.value

    def voting(self, parties: List[Party], electors: List[Elector]):
        self.time += self.ELECTIONS_TIME

        partyVotes = {number: 0 for number in range(len(parties))}

        for elector in electors:
            partyVotes[elector.chooseParty(parties)] += 1

        topParties = {number: votes for number, votes in sorted(partyVotes.items(), key=lambda item: item[1])}

        for partyCount in range(1, len(parties)):
            votes = sum(vote for number, vote in topParties if number < partyCount)

            for partyNumber in range(partyCount):
                seats = int(topParties[partyNumber] / votes * self.PARLAMENT_SEATS)
                if self.MIN_PARTY_SEATS <= seats <= self.MAX_PARTY_SEATS:
                    self.__parties[parties[topParties[partyCount - 1]]] = seats
                else:
                    break
            else:
                break
