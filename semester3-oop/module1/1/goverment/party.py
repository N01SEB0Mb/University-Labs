# coding=utf-8

from .position import Position


class Party(Position):
    def __init__(
            self,
            economic: float,
            social: float,
            title: str,
            members: int,
            strategy: int = 1
    ) -> None:
        super(Party, self).__init__(economic, social)

        self.title = title
        self.members = members
        self.strategy = strategy
