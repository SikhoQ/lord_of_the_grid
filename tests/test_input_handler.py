import unittest
from src.input_handler import InputHandler


class TestInputHandler(unittest.TestCase):
    def test_valid_input_length(self):
        self.assertTrue(InputHandler.valid_input_length("A1-A2"))
        self.assertFalse(InputHandler.valid_input_length("A1A2"))

    def test_valid_input_format(self):
        self.assertTrue(InputHandler.valid_input_format("A1-A2", 3))
        self.assertFalse(InputHandler.valid_input_format("A2-A3", 2))
        self.assertFalse(InputHandler.valid_input_format("A1:A2", 3))


if __name__ == "__main__":
    unittest.main()
