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

        self.__active = False

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool) -> None:
        self.__active = value

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other) -> bool:
        if isinstance(other, Party):
            return self.title == other.title
        else:
            return False
