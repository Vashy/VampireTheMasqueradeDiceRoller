import unittest

from VampireDiceRoller.DiceRoller import roll, RollCount


class MyTestCase(unittest.TestCase):

    def test_always_success_randomizer(self):
        result = RollCount(3, 5, always_success_fake_randomize)
        self.assertEqual(result.successes, 8)
        self.assertEqual(result.failures, 0)
        self.assertEqual(result.critical_successes, 0)
        self.assertEqual(result.bestial_failures, 0)

    def test_no_hunger_dices(self):
        result = RollCount(12, 0, randomize=always_success_fake_randomize)
        self.assertEqual(12, result.successes, 12)
        self.assertEqual(0, result.failures)

    def test_no_successes_randomizer(self):
        result = RollCount(13, 15, no_successes_fake_randomize)
        self.assertEqual(0, result.successes)
        self.assertEqual(28, result.failures)

    def test_ascending_randomize(self):
        result = RollCount(10, 10, AscendingFakeRandomize().randomize)
        self.assertEqual(4 + 4, result.successes)
        self.assertEqual(5 + 4, result.failures)
        self.assertEqual(1, result.critical_successes)
        self.assertEqual(1, result.messy_criticals)
        self.assertEqual(1, result.bestial_failures)

    def test_roll_result_successes_and_criticals(self):
        result = roll(4, 1, always_critical_fake_randomize)
        self.assertEqual(9, result.successes)
        self.assertEqual(0, result.failures)
        self.assertTrue(result.is_messy_critical)
        self.assertTrue(result.is_critical)
        result = roll(8, 2, always_critical_fake_randomize)
        self.assertEqual(20, result.successes)
        self.assertEqual(0, result.failures)
        self.assertTrue(result.is_messy_critical)
        self.assertTrue(result.is_critical)

    def test_roll_result_failures_and_successes(self):
        result = roll(5, 4, AscendingFakeRandomize().randomize)
        self.assertEqual(4, result.successes)
        self.assertEqual(5, result.failures)
        self.assertFalse(result.is_messy_critical)
        self.assertFalse(result.is_critical)

    def test_roll_result_is_critical(self):
        result = roll(2, 0, always_critical_fake_randomize)
        self.assertTrue(result.is_critical)
        self.assertFalse(result.is_messy_critical)
        result = roll(1, 1, always_critical_fake_randomize)
        self.assertTrue(result.is_critical)
        self.assertTrue(result.is_messy_critical)
        result = roll(1, 0, always_critical_fake_randomize)
        self.assertFalse(result.is_critical)
        self.assertFalse(result.is_messy_critical)

    def test_stringify(self):
        result = roll(3, 5, always_success_fake_randomize).stringify()
        self.assertEquals("8 successes\n0 failures", result)


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
