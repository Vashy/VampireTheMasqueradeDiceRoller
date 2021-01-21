from enum import Enum
from random import randint
from typing import Callable, Final, List

Randomize: Final = Callable[[int, int], int]


class RollCount:
    def __init__(self, normal_dices: int, hunger_dices: int, randomize: Randomize):
        (normal_dices_rolls, hunger_dices_rolls) = RollCount.calculate_rolls(normal_dices, hunger_dices,
                                                                                 randomize)

        self.rolls = normal_dices_rolls + hunger_dices_rolls

        normal_dices_results = self._map_dices(normal_dices_rolls)
        hunger_dices_results = self._map_dices(hunger_dices_rolls)
        self.successes = self._count_successes(normal_dices_results + hunger_dices_results)
        self.critical_successes = self._count_critical_successes(normal_dices_results)
        self.messy_criticals = self._count_critical_successes(hunger_dices_results)
        self.bestial_failures = self._count_bestial_failures(hunger_dices_results)
        self.failures = (normal_dices + hunger_dices) - \
                        (self.successes + self.critical_successes + self.messy_criticals)

    def __str__(self):
        return f"""RollCount(
        self.successes = {self.successes},
        self.critical_successes = {self.critical_successes},
        self.messy_criticals = {self.messy_criticals},
        self.bestial_failures = {self.bestial_failures},
        self.failures = {self.failures},
)"""

    class RollType(Enum):
        SUCCESS = 1
        CRITICAL_SUCCESS = 2
        FAILURE = 3
        CRITICAL_FAILURE = 4

    @staticmethod
    def calculate_rolls(normal_dices: int, hunger_dices: int, randomize: Randomize = randint) -> (int, int):
        normal_dices_results = []
        for _ in range(normal_dices):
            normal_dices_results.append(randomize(1, 10))
        hunger_dices_results = []
        for _ in range(hunger_dices):
            hunger_dices_results.append(randomize(1, 10))
        return normal_dices_results, hunger_dices_results

    @staticmethod
    def _map_dices(numbers: List[int]) -> List[RollType]:
        results = []
        for n in numbers:
            if n == 10:
                results.append(RollCount.RollType.CRITICAL_SUCCESS)
            elif n >= 6:
                results.append(RollCount.RollType.SUCCESS)
            elif n == 1:
                results.append(RollCount.RollType.CRITICAL_FAILURE)
            else:
                results.append(RollCount.RollType.FAILURE)

        return results

    @staticmethod
    def _count_successes(roll_results: List[RollType]) -> int:
        return RollCount._count(RollCount.RollType.SUCCESS, roll_results)

    @staticmethod
    def _count_critical_successes(roll_results: List[RollType]) -> int:
        return RollCount._count(RollCount.RollType.CRITICAL_SUCCESS, roll_results)

    @staticmethod
    def _count_bestial_failures(hunger_dices_results: List[RollType]) -> int:
        return RollCount._count(RollCount.RollType.CRITICAL_FAILURE, hunger_dices_results)

    @staticmethod
    def _count(result_type: RollType, roll_results: List[RollType]) -> int:
        result = 0
        for roll_result in roll_results:
            if roll_result == result_type:
                result += 1
        return result


def _to_successes(critical_successes: int) -> int:
    single_successes = critical_successes % 2
    return (critical_successes - single_successes) * 2 + single_successes


class RollResult:
    def __init__(self, roll_count: RollCount):
        self.successes = roll_count.successes \
                         + _to_successes(roll_count.critical_successes + roll_count.messy_criticals)
        self.failures = roll_count.failures
        self.is_messy_critical = roll_count.messy_criticals >= 1
        self.is_critical = roll_count.critical_successes + roll_count.messy_criticals >= 2
        self.is_bestial_failure = roll_count.bestial_failures >= 1
        self.rolls = roll_count.rolls

    def __str__(self) -> str:
        return f"""RollResult(
        self.successes = {self.successes},
        self.is_messy_critical = {self.is_messy_critical},
        self.is_critical = {self.is_critical},
        self.is_bestial_failure = {self.is_bestial_failure},
)"""


def roll(normal_dices: int, hunger_dices: int = 0, randomize: Randomize = randint) -> RollResult:
    return RollResult(RollCount(normal_dices, hunger_dices, randomize))


if __name__ == '__main__':
    def print_roll(normal_dices, hunger_dices=0):
        print(f"Rolling {normal_dices}+{hunger_dices}:")
        roll_count = roll(normal_dices, hunger_dices)
        print(roll_count)
        print()


    print_roll(3, 2)
    print_roll(1)
    print_roll(50, 51)
