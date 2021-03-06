import unittest

from VampireDiceRoller.DiceRoller import roll, RollCount
from VampireDiceRoller.Stringifier import stringify


class DiceRollerTestCase(unittest.TestCase):

    def test_always_success_randomizer(self):
        result = RollCount(3, 5, always_success_fake_randomize)
        self.assertEqual([9] * 8, result.rolls)
        self.assertEqual(result.successes, 8)
        self.assertEqual(result.failures, 0)
        self.assertEqual(result.critical_successes, 0)
        self.assertEqual(result.bestial_failures, 0)

    def test_no_hunger_dices(self):
        result = RollCount(12, 0, randomize=always_success_fake_randomize)
        self.assertEqual([9] * 12, result.rolls)
        self.assertEqual(12, result.successes, 12)
        self.assertEqual(0, result.failures)

    def test_no_successes_randomizer(self):
        result = RollCount(13, 15, always_fail_fake_randomize)
        self.assertEqual([2] * 28, result.rolls)
        self.assertEqual(0, result.successes)
        self.assertEqual(28, result.failures)

    def test_ascending_randomize(self):
        result = RollCount(10, 10, AscendingFakeRandomize().randomize)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2, result.rolls)
        self.assertEqual(4 + 4, result.successes)
        self.assertEqual(5 + 5, result.failures)
        self.assertEqual(1, result.critical_successes)
        self.assertEqual(1, result.messy_criticals)
        self.assertEqual(1, result.bestial_failures)

    def test_roll_result_successes_and_criticals(self):
        result = roll(4, 1, always_critical_fake_randomize)
        self.assertEqual(9, result.successes)
        self.assertEqual(0, result.failures)
        self.assertEqual([10] * 5, result.rolls)
        self.assertTrue(result.is_messy_critical)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_bestial_failure)
        result = roll(8, 2, always_critical_fake_randomize)
        self.assertEqual(20, result.successes)
        self.assertEqual(0, result.failures)
        self.assertEqual([10] * 10, result.rolls)
        self.assertTrue(result.is_messy_critical)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_bestial_failure)

    def test_roll_result_failures_and_successes(self):
        result = roll(5, 4, AscendingFakeRandomize().randomize)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], result.rolls)
        self.assertEqual(4, result.successes)
        self.assertEqual(5, result.failures)
        self.assertFalse(result.is_messy_critical)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_bestial_failure)

    def test_roll_result_is_critical(self):
        result = roll(2, 0, always_critical_fake_randomize)
        self.assertEqual([10, 10], result.rolls)
        self.assertTrue(result.is_critical)
        self.assertFalse(result.is_messy_critical)
        self.assertFalse(result.is_bestial_failure)
        result = roll(1, 1, always_critical_fake_randomize)
        self.assertEqual([10, 10], result.rolls)
        self.assertFalse(result.is_critical)
        self.assertTrue(result.is_messy_critical)
        self.assertFalse(result.is_bestial_failure)
        result = roll(1, 0, always_critical_fake_randomize)
        self.assertEqual([10], result.rolls)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_messy_critical)
        self.assertFalse(result.is_bestial_failure)
        result = roll(0, 1, always_critical_fake_randomize)
        self.assertEqual([10], result.rolls)
        self.assertEqual(1, result.successes)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_messy_critical)
        self.assertFalse(result.is_bestial_failure)

    def test_roll_bestial_failure(self):
        result = roll(1, 1, always_one_fake_randomize)
        self.assertEqual(0, result.successes)
        self.assertEqual(2, result.failures)
        self.assertEqual([1, 1], result.rolls)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_messy_critical)
        self.assertTrue(result.is_bestial_failure)

    def test_stringify_no_notes(self):
        result = stringify(roll(3, 5, always_success_fake_randomize))
        self.assertEqual("- **Successes**: 8\n- **Failures**: 0", result)
        result = stringify(roll(17, 4, always_success_fake_randomize))
        self.assertEqual("- **Successes**: 21\n- **Failures**: 0", result)
        result = stringify(roll(1, 0, always_critical_fake_randomize))
        self.assertEqual("- **Successes**: 1\n- **Failures**: 0", result)


def always_success_fake_randomize(ignored1, ignored2) -> int:
    return 9


def always_critical_fake_randomize(ignored1, ignored2) -> int:
    return 10


def always_fail_fake_randomize(ignored1, ignored2) -> int:
    return 2


def always_one_fake_randomize(ignored1, ignored2) -> int:
    return 1


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
