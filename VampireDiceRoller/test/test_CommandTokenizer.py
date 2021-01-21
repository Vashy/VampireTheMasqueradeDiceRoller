import unittest
from VampireDiceRoller.CommandTokenizer import tokenize


class CommandTokenizerTestCase(unittest.TestCase):
    def test_simple_tokenize(self):
        (normal_dices, hunger_dices, comment) = tokenize('3+2')
        self.assertEqual(3, normal_dices)
        self.assertEqual(2, hunger_dices)
        self.assertIsNone(comment)

    def test_tokenize_without_hunger(self):
        (normal_dices, hunger_dices, comment) = tokenize('6')
        self.assertEqual(6, normal_dices)
        self.assertEqual(0, hunger_dices)
        self.assertIsNone(comment)

    def test_tokenize_with_comment(self):
        (normal_dices, hunger_dices, comment) = tokenize('7+3 nice comment!')
        self.assertEqual(7, normal_dices)
        self.assertEqual(3, hunger_dices)
        self.assertEqual('nice comment!', comment)

    def test_tokenize_with_comment_without_hunger(self):
        (normal_dices, hunger_dices, comment) = tokenize('7 another nice comment!')
        self.assertEqual(7, normal_dices)
        self.assertEqual(0, hunger_dices)
        self.assertEqual('another nice comment!', comment)


if __name__ == '__main__':
    unittest.main()
