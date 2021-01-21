import unittest

from VampireDiceRoller.DiceRoller import roll
from VampireDiceRoller.DiscordRunner import stringify
from VampireDiceRoller.test.test_DiceRoller import always_critical_fake_randomize, AscendingFakeRandomize


class DiscordClientTest(unittest.TestCase):
    def test_stringify_notes_critical_hit(self):
        result = stringify(roll(2, 0, always_critical_fake_randomize))
        self.assertEqual("- **Successes**: 4\n- **Failures**: 0\n- **Special**: *critical hit*", result)

    def test_stringify_notes_bestial_failure(self):
        result = stringify(roll(0, 10, AscendingFakeRandomize().randomize))
        self.assertEqual("- **Successes**: 5\n- **Failures**: 5\n- **Special**: *bestial failure*",
                         result)

    def test_stringify_notes_messy_critical(self):
        result = stringify(roll(0, 20, always_critical_fake_randomize))
        self.assertEqual("- **Successes**: 40\n- **Failures**: 0\n- **Special**: *messy critical*",
                         result)

    def test_stringify_notes_messy_critical_and_bestial_failure(self):
        result = stringify(roll(20, 20, AscendingFakeRandomize().randomize))
        self.assertEqual(
            "- **Successes**: 24\n- **Failures**: 20\n"
            "- **Special**: *messy critical*, *bestial failure*",
            result)

    def test_stringify_critical_hit_and_bestial_failure(self):
        result = stringify(roll(20, 1, AscendingFakeRandomize().randomize))
        self.assertEqual(
            "- **Successes**: 12\n- **Failures**: 11\n"
            "- **Special**: *critical hit*, *bestial failure*",
            result)


if __name__ == '__main__':
    unittest.main()
