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
    def __init__(self, successes: int, failures: int, critical_successes: int, messy_criticals: int,
                 bestial_failures: int):
        self.successes = successes
        self.failures = failures
        self.critical_successes = critical_successes
        self.messy_criticals = messy_criticals
        self.bestial_failures = bestial_failures

    class ResultType(Enum):
        SUCCESS = 1
        CRITICAL_SUCCESS = 2
        FAILURE = 3
        CRITICAL_FAILURE = 4


def map_dices(numbers: List[int]) -> List[RollResult.ResultType]:
    results = []
    for n in numbers:
        if n == 10:
            results.append(RollResult.ResultType.CRITICAL_SUCCESS)
        elif n >= 6:
            results.append(RollResult.ResultType.SUCCESS)
        elif n == 1:
            results.append(RollResult.ResultType.CRITICAL_FAILURE)
        else:
            results.append(RollResult.ResultType.FAILURE)

    return results


def count_successes(roll_results: List[RollResult.ResultType]) -> int:
    return count(RollResult.ResultType.SUCCESS, roll_results)


def count_critical_successes(roll_results: List[RollResult.ResultType]) -> int:
    return count(RollResult.ResultType.CRITICAL_SUCCESS, roll_results)


def count(result_type: RollResult.ResultType, roll_results: List[RollResult.ResultType]) -> int:
    result = 0
    for roll_result in roll_results:
        if roll_result == result_type:
            result += 1
    return result


def count_bestial_failures(hunger_dices_results):
    return count(RollResult.ResultType.CRITICAL_FAILURE, hunger_dices_results)


def roll(normal_dices: int, hunger_dices: int = 0, randomize: Randomize = calculate_rolls) -> RollResult:
    (normal_dices_results, hunger_dices_results) = calculate_rolls(normal_dices, hunger_dices, randomize)

    normal_dices_results = map_dices(normal_dices_results)
    hunger_dices_results = map_dices(hunger_dices_results)
    successes = count_successes(normal_dices_results + hunger_dices_results)
    critical_successes = count_critical_successes(normal_dices_results)
    messy_criticals = count_critical_successes(hunger_dices_results)
    bestial_failures = count_bestial_failures(hunger_dices_results)
    failures = (normal_dices + hunger_dices) - (successes + critical_successes + messy_criticals + bestial_failures)

    return RollResult(successes, failures, critical_successes, messy_criticals, bestial_failures)
