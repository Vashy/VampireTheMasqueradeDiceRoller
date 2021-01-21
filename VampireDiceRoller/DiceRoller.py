from enum import Enum
from random import randint
from typing import Callable, Final, List

Randomize: Final = Callable[[int, int], int]


class RollCount:
    def __init__(self, normal_dices: int, hunger_dices: int, randomize: Randomize):
        (normal_dices_rolls, hunger_dices_rolls) = calculate_rolls(normal_dices, hunger_dices, randomize)

        self.rolls = normal_dices_rolls + hunger_dices_rolls

        normal_dices_results = _map_dices(normal_dices_rolls)
        hunger_dices_results = _map_dices(hunger_dices_rolls)
        self.successes = _count_successes(normal_dices_results + hunger_dices_results)
        self.critical_successes = _count_critical_successes(normal_dices_results)
        self.messy_criticals = _count_critical_successes(hunger_dices_results)
        self.bestial_failures = _count_bestial_failures(hunger_dices_results)
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


class RollResultType(Enum):
    SUCCESS = 1
    CRITICAL_SUCCESS = 2
    FAILURE = 3
    CRITICAL_FAILURE = 4

    @staticmethod
    def from_int(n: int):
        if n == 10:
            return RollResultType.CRITICAL_SUCCESS
        elif n >= 6:
            return RollResultType.SUCCESS
        elif n == 1:
            return RollResultType.CRITICAL_FAILURE
        else:
            return RollResultType.FAILURE


def calculate_rolls(normal_dices: int, hunger_dices: int, randomize: Randomize = randint) -> (int, int):
    normal_dices_results = [randomize(1, 10) for _ in range(normal_dices)]
    hunger_dices_results = [randomize(1, 10) for _ in range(hunger_dices)]
    return normal_dices_results, hunger_dices_results


def _map_dices(numbers: List[int]) -> List[RollResultType]:
    return [RollResultType.from_int(n) for n in numbers]


def _count_successes(result_types: List[RollResultType]) -> int:
    return _count(RollResultType.SUCCESS, result_types)


def _count_critical_successes(result_types: List[RollResultType]) -> int:
    return _count(RollResultType.CRITICAL_SUCCESS, result_types)


def _count_bestial_failures(hunger_dices_results: List[RollResultType]) -> int:
    return _count(RollResultType.CRITICAL_FAILURE, hunger_dices_results)


def _count(result_type: RollResultType, roll_results: List[RollResultType]) -> int:
    return len([roll_result for roll_result in roll_results if roll_result == result_type])


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
