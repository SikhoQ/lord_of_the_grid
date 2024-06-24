import unittest
from src.game_grid import Grid
from src.player import Player
from src.utils import game_ended, scores


class TestUtils(unittest.TestCase):
    def test_game_ended(self):
        grid = Grid(2)
        self.assertFalse(game_ended(grid))
        for row in grid.grid:
            for i in range(len(row)):
                row[i] = "-"
        self.assertTrue(game_ended(grid))

    def test_scores(self):
        grid = Grid(3)
        player1 = Player("X")
        player2 = Player("O")
        grid.grid[1][1] = "X"
        grid.grid[1][3] = "O"
        result = scores(grid, player1, player2)
        self.assertEqual(result["X"], 1)
        self.assertEqual(result["O"], 1)


if __name__ == "__main__":
    unittest.main()
