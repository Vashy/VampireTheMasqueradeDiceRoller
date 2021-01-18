import unittest

from VampireDiceRoller.DiceRoller import roll


class MyTestCase(unittest.TestCase):

    def test_always_success_randomizer(self):
        result = roll(1, 5, always_success)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 5)

    def test_no_hunger_dices(self):
        result = roll(12, randomize=always_success)
        self.assertEqual(result[0], 12)
        self.assertEqual(result[1], 0)

    def test_no_successes_randomizer(self):
        result = roll(13, 15, no_successes)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)


def always_success(n: int) -> int:
    return n


def no_successes(n) -> int:
    return 0


if __name__ == '__main__':
    unittest.main()
