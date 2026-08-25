from abc import ABC, abstractmethod

import roman


class NumberingStrategy:
    @abstractmethod
    def get(self, n: int) -> str:
        pass


class IntNumberingStragegy:
    def get(self, n: int) -> str:
        return str(n)


class Base26NumberingStragegy:
    def get(self, n: int) -> str:
        value = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            value = chr(65 + remainder) + value
        return value.lower()


class RomanNumberingStrategy:
    def get(self, n: int) -> str:
        return roman.toRoman(n)


class NumberingFactory:
    def __init__(self, strategies: list[NumberingStrategy]):
        self._strategies: list[NumberingStrategy] = strategies

    def get_next(self, current_strategy: NumberingStrategy | None = None) -> NumberingStrategy:
        if not self._strategies:
            raise RuntimeError("No numbering strategies registered")

        if current_strategy is None:
            return self._strategies[0]

        if current_strategy not in self._strategies:
            return self._strategies[0]

        current_index: int = self._strategies.index(current_strategy)
        next_index: int = (current_index + 1) % len(self._strategies)
        new_strategy: NumberingStrategy = self._strategies[next_index]
        return new_strategy


numbering_factory: NumberingFactory = NumberingFactory(
    [
        IntNumberingStragegy(),
        Base26NumberingStragegy(),
        RomanNumberingStrategy(),
    ]
)


class LijstType(ABC):
    def has_number(self) -> bool:
        return False

    def get_number(self, n: int) -> str:
        return ""

    def get_numbering_strategy(self) -> NumberingStrategy | None:
        return None

    @abstractmethod
    def get_type(self) -> str:
        pass


class LijstTypeUnordered(LijstType):
    def get_type(self) -> str:
        return "ongemarkeerd"


class LijstTypeOrdered(LijstType):
    def __init__(self, numbering_strategy: NumberingStrategy):
        self._numbering_strategy: NumberingStrategy = numbering_strategy

    def has_number(self) -> bool:
        return True

    def get_number(self, n: int) -> str:
        number: str = self._numbering_strategy.get(n)
        return f"{number}."

    def get_numbering_strategy(self) -> NumberingStrategy | None:
        return self._numbering_strategy

    def get_type(self) -> str:
        return "expliciet"
