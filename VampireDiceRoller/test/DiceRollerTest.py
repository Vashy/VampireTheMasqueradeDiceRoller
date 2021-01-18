import unittest

from VampireDiceRoller.DiceRoller import roll, RollResult


class MyTestCase(unittest.TestCase):

    def test_always_success_randomizer(self):
        result = roll(3, 5, always_success_fake_randomize)
        self.assertEqual(result.successes, 8)
        self.assertEqual(result.failures, 0)
        self.assertEqual(result.critical_successes, 0)
        self.assertEqual(result.bestial_failures, 0)

    def test_no_hunger_dices(self):
        result = roll(12, randomize=always_success_fake_randomize)
        self.assertEqual(12, result.successes, 12)
        self.assertEqual(0, result.failures)

    def test_no_successes_randomizer(self):
        result = roll(13, 15, no_successes_fake_randomize)
        self.assertEqual(0, result.successes)
        self.assertEqual(28, result.failures)

    def test_ascending_randomize(self):
        result = roll(10, 10, AscendingFakeRandomize().randomize)
        self.assertEqual(4 + 4, result.successes)
        self.assertEqual(5 + 4, result.failures)
        self.assertEqual(1, result.critical_successes)
        self.assertEqual(1, result.messy_criticals)
        self.assertEqual(1, result.bestial_failures)

    def test_roll_result_successes_and_criticals(self):
        result = RollResult(roll(4, 1, always_critical_fake_randomize))
        self.assertEqual(9, result.successes)
        self.assertEqual(True, result.is_messy_critical)
        result = RollResult(roll(8, 2, always_critical_fake_randomize))
        self.assertEqual(20, result.successes)
        self.assertEqual(True, result.is_messy_critical)

    def test_roll_result_failures_and_successes(self):
        result = RollResult(roll(5, 4, AscendingFakeRandomize().randomize))
        self.assertEqual(4, result.successes)
        self.assertEqual(False, result.is_messy_critical)


def always_success_fake_randomize(ignored1, ignored2) -> int:
    return 9


def always_critical_fake_randomize(ignored1, ignored2) -> int:
    return 10


def no_successes_fake_randomize(ignored1, ignored2) -> int:
    return 2


class AscendingFakeRandomize:
    def __init__(self):
        self.value = 0

    def randomize(self, ignored1, ignored2) -> int:
        if self.value == 10:
            self.value = 0
        self.value += 1
        return self.value


if __name__ == '__main__':
    unittest.main()
