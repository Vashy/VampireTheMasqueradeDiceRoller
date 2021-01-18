import unittest

from VampireDiceRoller.DiceRoller import roll


class MyTestCase(unittest.TestCase):

    def test_always_success_randomizer(self):
        result = roll(3, 5, always_success)
        self.assertEqual(result.successes, 3)
        self.assertEqual(result.failures, 0)

    def test_no_hunger_dices(self):
        result = roll(12, randomize=always_success)
        self.assertEqual(result.successes, 12)
        self.assertEqual(result.failures, 0)

    def test_no_successes_randomizer(self):
        result = roll(13, 15, no_successes)
        self.assertEqual(result.successes, 0)
        self.assertEqual(result.failures, 13)


def always_success(ignored1, ignored2) -> int:
    return 9


def no_successes(ignored1, ignored2) -> int:
    return 1


if __name__ == '__main__':
    unittest.main()
