# coding=utf-8


class IndexCounter:
    def __init__(self, startValue: int = 1) -> None:
        self.__value = startValue - 1

    def __call__(self) -> int:
        self.__value += 1
        return self.__value


NCounter = IndexCounter()
S = 1
DELETED = set()


class Base1:
    def __init__(self, *args) -> None:
        self.N = NCounter()
        self.included = args

    def formula(self, s) -> int:
        return 3 * s + self.N + 41

    def __call__(self, s: int) -> int:
        if self.N in DELETED:
            return s

        for item in included:
            s = item(s)

        return self.formula(s)

    def __del__(self) -> None:
        global S

        DELETED.add(self.N)

        for item in self.included:
            item.__del__()

        S = self(S)

    def __str__(self) -> str:
        return f"{self.N}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(N={self.N})"


class Base2:
    def __init__(self, *args) -> None:
        self.N = NCounter()
        self.included = args

    def formula(self, s) -> int:
        return s // 2 - self.N

    def __call__(self, s: int) -> int:
        if self.N in DELETED:
            return s

        for item in included:
            s = item(s)

        return self.formula(s)

    def __del__(self) -> None:
        global S

        DELETED.add(self.N)

        for item in self.included:
            item.__del__()

        print(self.N, S)
        S = self(S)
        print(self.N, S)

    def __str__(self) -> str:
        return f"{self.N}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(N={self.N})"


class Alpha(Base1):
    def formula(self, s) -> int:
        return s - 2 * self.N + 14


class Beta(Base1):
    def formula(self, s) -> int:
        return s - self.N


class Gamma(Base2):
    def formula(self, s) -> int:
        return s - self.N


class Delta(Base2):
    def formula(self, s) -> int:
        return s + 3 * self.N - 41
