from enum import Enum
from random import randint
from typing import Callable, Final, List

Randomize: Final = Callable[[int, int], int]


class RollResult:
    def __init__(self, normal_dices: int, hunger_dices: int, randomize: Randomize):
        (normal_dices_results, hunger_dices_results) = RollResult.calculate_rolls(normal_dices, hunger_dices,
                                                                                  randomize)

        normal_dices_results = self._map_dices(normal_dices_results)
        hunger_dices_results = self._map_dices(hunger_dices_results)
        self.successes = self._count_successes(normal_dices_results + hunger_dices_results)
        self.critical_successes = self._count_critical_successes(normal_dices_results)
        self.messy_criticals = self._count_critical_successes(hunger_dices_results)
        self.bestial_failures = self._count_bestial_failures(hunger_dices_results)
        self.failures = (normal_dices + hunger_dices) - \
                        (self.successes + self.critical_successes + self.messy_criticals + self.bestial_failures)

    class ResultType(Enum):
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
    def _map_dices(numbers: List[int]) -> List[ResultType]:
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

    @staticmethod
    def _count_successes(roll_results: List[ResultType]) -> int:
        return RollResult._count(RollResult.ResultType.SUCCESS, roll_results)

    @staticmethod
    def _count_critical_successes(roll_results: List[ResultType]) -> int:
        return RollResult._count(RollResult.ResultType.CRITICAL_SUCCESS, roll_results)

    @staticmethod
    def _count_bestial_failures(hunger_dices_results):
        return RollResult._count(RollResult.ResultType.CRITICAL_FAILURE, hunger_dices_results)

    @staticmethod
    def _count(result_type: ResultType, roll_results: List[ResultType]) -> int:
        result = 0
        for roll_result in roll_results:
            if roll_result == result_type:
                result += 1
        return result


def roll(normal_dices: int, hunger_dices: int = 0, randomize: Randomize = RollResult.calculate_rolls) -> RollResult:
    return RollResult(normal_dices, hunger_dices, randomize)
