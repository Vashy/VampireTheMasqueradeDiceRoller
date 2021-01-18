from enum import Enum
from random import randint
from typing import Callable, Final, List

Randomize: Final = Callable[[int, int], int]


def calculate_rolls(normal_dices: int, hunger_dices: int, randomize: Randomize = randint) -> (int, int):
    normal_dices_results = []
    for _ in range(normal_dices):
        normal_dices_results.append(randomize(1, 10))
    hunger_dices_results = []
    for _ in range(hunger_dices):
        hunger_dices_results.append(randomize(1, 10))
    return normal_dices_results, hunger_dices_results


class RollResult:
    def __init__(self, successes, failures, critical_successes, bestial_criticals):
        self._successes = successes
        self._failures = failures
        self._critical_successes = critical_successes
        self._bestial_criticals = bestial_criticals

    @property
    def successes(self):
        return self._successes

    @property
    def failures(self):
        return self._failures

    @property
    def critical_successes(self):
        return self._critical_successes

    @property
    def bestial_criticals(self):
        return self._bestial_criticals

    class ResultType(Enum):
        SUCCESS = 1
        CRITICAL_SUCCESS = 2
        FAILURE = 3
        BESTIAL_FAILURE = 4
        BESTIAL_CRITICAL = 5


def map_dices(numbers: List[int]) -> List[RollResult.ResultType]:
    results = []
    for n in numbers:
        if n == 10:
            results.append(RollResult.ResultType.CRITICAL_SUCCESS)
        elif n > 6:
            results.append(RollResult.ResultType.SUCCESS)
        else:
            results.append(RollResult.ResultType.FAILURE)

    return results


def count_successes(roll_results: List[RollResult.ResultType]) -> int:
    result = 0
    for roll_result in roll_results:
        if roll_result == RollResult.ResultType.SUCCESS:
            result += 1
    return result


def roll(normal_dices: int, hunger_dices: int = 0, randomize: Randomize = calculate_rolls) -> RollResult:
    (normal_dices_results, hunger_dices_results) = calculate_rolls(normal_dices, hunger_dices, randomize)

    normal_dices_results = map_dices(normal_dices_results)
    successes = count_successes(normal_dices_results)
    # bestial_successes = count_successes(hunger_dices_results)

    return RollResult(successes, normal_dices - successes, 0, 0)
