import unittest
from unittest.mock import patch, MagicMock
from src.player import Player


class TestPlayer(unittest.TestCase):
    @patch('src.player.inquirer.select')
    def test_get_player_initials(self, mock_select):
        mock_select.return_value.execute = MagicMock(side_effect=['A', 'B'])
        player1, player2 = Player.get_player_initials()
        self.assertEqual(player1, 'A')
        self.assertEqual(player2, 'B')

    def test_player_initialization(self):
        player = Player("X")
        self.assertEqual(player.name, "X")
        self.assertEqual(player.score, 0)


if __name__ == "__main__":
    unittest.main()
