from random import randint
from typing import Callable, Final

Randomize: Final = Callable[[int, int], int]


def calculate_successes(n: int, randomize: Randomize = randint) -> int:
    successes = 0
    for _ in range(n):
        if randomize(1, 10) >= 6:
            successes += 1
    return successes


def roll(normal_dices: int, hunger_dices: int = 0, randomize=calculate_successes) -> (int, int):
    return [randomize(normal_dices), randomize(hunger_dices)]
