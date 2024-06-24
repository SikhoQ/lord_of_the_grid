import unittest
from src.game_grid import Grid
from src.player import Player
from src.utils import game_ended, scores


class TestGameFunctions(unittest.TestCase):
    def test_scores(self):
        grid = Grid(3)
        player1 = Player('A')
        player2 = Player('B')
        grid.grid[0][0] = 'A'
        grid.grid[0][2] = 'B'
        score_dict = scores(grid, player1, player2)
        self.assertEqual(score_dict['A'], 1)
        self.assertEqual(score_dict['B'], 1)

    def test_game_ended(self):
        grid = Grid(3)
        self.assertFalse(game_ended(grid))
        for row in grid.grid:
            for i in range(len(row)):
                row[i] = 'X'
        self.assertTrue(game_ended(grid))


if __name__ == '__main__':
    unittest.main()
