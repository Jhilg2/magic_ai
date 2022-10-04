import unittest
from card import Player

from magic import attack

class TestAttack(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.player1 = Player
    
    def test_attack_no_attacks(self):
        """
        Test that it can sum a list of integers
        """
        pass
        # self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()