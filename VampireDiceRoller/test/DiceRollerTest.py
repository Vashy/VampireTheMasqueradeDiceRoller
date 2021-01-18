import unittest

from VampireDiceRoller.DiceRoller import roll


class MyTestCase(unittest.TestCase):

    def test_always_success_randomizer(self):
        result = roll(3, 5, always_success)
        self.assertEqual(result.successes, 8)
        self.assertEqual(result.failures, 0)
        self.assertEqual(result.critical_successes, 0)
        self.assertEqual(result.bestial_failures, 0)

    def test_no_hunger_dices(self):
        result = roll(12, randomize=always_success)
        self.assertEqual(result.successes, 12)
        self.assertEqual(result.failures, 0)

    def test_no_successes_randomizer(self):
        result = roll(13, 15, no_successes)
        self.assertEqual(result.successes, 0)
        self.assertEqual(result.failures, 28)

    def test_ascending_randomize(self):
        randomize = AscendingRandomize()
        result = roll(10, 10, randomize.ascending_randomize)
        self.assertEqual(result.successes, 4 + 4)
        self.assertEqual(result.failures, 5 + 5)
        self.assertEqual(result.critical_successes, 1)
        self.assertEqual(result.messy_criticals, 1)
        self.assertEqual(result.bestial_failures, 1)


def always_success(ignored1, ignored2) -> int:
    return 9


def no_successes(ignored1, ignored2) -> int:
    return 2


class AscendingRandomize:
    def __init__(self):
        self.value = 0

    def ascending_randomize(self, ignored1, ignored2) -> int:
        if self.value == 10:
            self.value = 0
        self.value += 1
        return self.value


if __name__ == '__main__':
    unittest.main()
