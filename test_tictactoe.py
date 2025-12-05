import unittest
import tkinter as tk

from main import TicTacToeApp, BOARD_SIZE


class TestTicTacToeLogic(unittest.TestCase):
    def setUp(self):
        # создаём "невидимое" окно Tk, чтобы не вылезало окно при тестах
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = TicTacToeApp(self.root)

    def tearDown(self):
        # закрываем Tk после каждого теста
        self.root.destroy()

    def test_empty_board_has_no_winner_and_not_draw(self):
        """Пустое поле: нет победителя и не ничья."""
        winner, cells = self.app.check_winner()
        self.assertIsNone(winner)
        self.assertEqual(cells, [])
        self.assertFalse(self.app.is_draw())

    def test_row_win_for_x(self):
        """X выигрывает по первой строке."""
        self.app.board = [
            ["X", "X", "X"],
            [None, None, None],
            [None, None, None],
        ]
        winner, cells = self.app.check_winner()
        self.assertEqual(winner, "X")
        self.assertEqual(cells, [(0, 0), (0, 1), (0, 2)])

    def test_draw_full_board(self):
        """Поле полностью заполнено, победителя нет → ничья."""
        self.app.board = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"],
        ]
        winner, _ = self.app.check_winner()
        self.assertIsNone(winner)
        self.assertTrue(self.app.is_draw())


if __name__ == "__main__":
    unittest.main()
