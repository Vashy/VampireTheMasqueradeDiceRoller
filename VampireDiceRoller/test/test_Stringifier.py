import unittest

from VampireDiceRoller.DiceRoller import roll
from VampireDiceRoller.Stringifier import stringify
from VampireDiceRoller.test.test_DiceRoller import always_success_fake_randomize, always_critical_fake_randomize, \
    AscendingFakeRandomize


class MyTestCase(unittest.TestCase):
    def test_simple_stringify(self):
        self.assertEqual('- **Successes**: 3\n- **Failures**: 0', stringify(roll(2, 1, always_success_fake_randomize)))
        self.assertEqual('- !Successes!: 1\n- !Failures!: 0', stringify(roll(1, 0, always_success_fake_randomize), '!'))

    def test_stringify_list_prefix(self):
        self.assertEqual('!! **Successes**: 3\n!! **Failures**: 0',
                         stringify(roll(2, 1, always_success_fake_randomize), list_prefix='!!'))

    def test_criticals(self):
        result = roll(2, 0, always_critical_fake_randomize)
        self.assertEqual('- **Successes**: 4\n- **Failures**: 0\n- **Special**: *critical hit*', stringify(result))
        self.assertEqual('- **Successes**: 4\n- **Failures**: 0\n- **Special**: !!critical hit!!',
                         stringify(result, italic_delimiter='!!'))

    def test_messy_and_bestial_failure(self):
        result = roll(10, 10, AscendingFakeRandomize().randomize)
        self.assertEqual('- **Successes**: 12\n- **Failures**: 10\n- **Special**: *messy critical*, *bestial failure*',
                         stringify(result))
        self.assertEqual('- *Successes*: 12\n- *Failures*: 10\n- *Special*: !messy critical!, !bestial failure!',
                         stringify(result, bold_delimiter='*', italic_delimiter='!'))


if __name__ == '__main__':
    unittest.main()
