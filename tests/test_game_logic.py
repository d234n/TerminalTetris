import tempfile
import unittest
from pathlib import Path

import game_logic
from config import height, width


class GameLogicTests(unittest.TestCase):
    def test_rotate_moves_each_coordinate(self):
        shape = [(0, 1), (1, 1), (2, 1), (3, 1)]
        expected = [(2, 0), (2, 1), (2, 2), (2, 3)]

        self.assertEqual(game_logic.rotate(shape), expected)

    def test_can_move_rejects_left_wall(self):
        board = [[""] * width for _ in range(height)]
        shape = [(0, 0), (1, 0), (2, 0), (3, 0)]

        self.assertFalse(game_logic.can_move(board, shape, -1, 0))

    def test_can_move_rejects_filled_cell(self):
        board = [[""] * width for _ in range(height)]
        board[5][3] = "[]"

        self.assertFalse(game_logic.can_move(board, [(0, 0)], 3, 5))

    def test_clear_lines_removes_full_row(self):
        board = [[""] * width for _ in range(height)]
        board[-1] = ["[]"] * width
        board[-2][0] = "55"

        cleared = game_logic.clear_lines(board)

        self.assertEqual(cleared, 1)
        self.assertEqual(board[-1][0], "55")
        self.assertTrue(all(cell == "" for cell in board[0]))

    def test_high_score_file_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            score_path = Path(directory) / "high_score.txt"
            original_path = game_logic.HIGH_SCORE_FILE
            game_logic.HIGH_SCORE_FILE = str(score_path)
            try:
                self.assertEqual(game_logic.load_high_score(), 0)
                game_logic.save_high_score(1250)
                self.assertEqual(game_logic.load_high_score(), 1250)
                self.assertEqual(game_logic.update_high_score(1300, 1250), 1300)
            finally:
                game_logic.HIGH_SCORE_FILE = original_path


if __name__ == "__main__":
    unittest.main()