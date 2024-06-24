import unittest
from src.player import Player
from src.game_grid import Grid


class TestGameGrid(unittest.TestCase):
    def test_grid_creation(self):
        grid = Grid(3)
        expected_grid = [
            ["+", " ", "+", " ", "+"],
            [" ", " ", " ", " ", " "],
            ["+", " ", "+", " ", "+"],
            [" ", " ", " ", " ", " "],
            ["+", " ", "+", " ", "+"]
        ]
        self.assertEqual(grid.grid, expected_grid)

    def test_already_played(self):
        grid = Grid(3)
        play = "A1-A2"
        grid.update_grid(play)
        self.assertTrue(grid.already_played(play))
        self.assertFalse(grid.already_played("A2-A3"))

    def test_update_grid(self):
        grid = Grid(3)
        grid.update_grid("A1-A2")
        self.assertEqual(grid.grid[0][1], "-")
        grid.update_grid("A1-B1")
        self.assertEqual(grid.grid[1][0], "|")

    def test_update_grid_block_complete(self):
        grid = Grid(3)
        grid.update_grid("A1-A2")
        grid.update_grid("B1-B2")
        grid.update_grid("A1-B1")
        grid.update_grid("A2-B2")
        grid.update_grid("B1-B2")
        self.assertEqual(grid.grid[0][1], "-")
        self.assertEqual(grid.grid[2][1], "-")
        self.assertEqual(grid.grid[1][0], "|")
        self.assertEqual(grid.grid[1][2], "|")

    def test_check_block_completed(self):
        grid = Grid(3)
        grid.update_grid("A1-A2")
        grid.update_grid("B1-B2")
        grid.update_grid("A1-B1")
        grid.update_grid("A2-B2")
        self.assertTrue(grid.check_block_completed("A2-B2"))

    def test_get_coordinates(self):
        grid = Grid(3)
        coords = grid.get_coordinates("A1-B1")
        self.assertEqual(coords, (0, 0, 2, 0))

    def test_do_block_sign(self):
        grid = Grid(3)
        player = Player("X")
        grid.update_grid("A1-A2")
        grid.update_grid("B1-B2")
        grid.update_grid("A1-B1")
        grid.update_grid("A2-B2")
        grid.update_grid("B1-B2")
        grid.sign_block = [1, 1]
        grid.do_block_sign(player)
        self.assertEqual(grid.grid[1][1], "X")


if __name__ == "__main__":
    unittest.main()
