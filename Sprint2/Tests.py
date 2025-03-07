import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox
from Game_Logic import GLogic
from GUI import SoS_GUI

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game_logic = GLogic()
    
    def test_valid_board_sizes(self):
        for size in range(3, 11):
            with self.subTest(size=size):
                result = self.game_logic.g_verify(str(size))
                self.assertEqual(result, size)
                self.assertIsNotNone(self.game_logic.grid)
                self.assertEqual(len(self.game_logic.grid), size)
                for row in self.game_logic.grid:
                    self.assertEqual(len(row), size)
                    for cell in row:
                        self.assertEqual(cell, " ")
    
    def test_too_small_board_sizes(self):
        for size in [-1, 0, 1, 2]:
            with self.subTest(size=size):
                result = self.game_logic.g_verify(str(size))
                self.assertIsInstance(result, str)
                self.assertIn("Invalid", result)
    
    def test_too_large_board_sizes(self):
        for size in [11, 15, 100]:
            with self.subTest(size=size):
                result = self.game_logic.g_verify(str(size))
                self.assertIsInstance(result, str)
                self.assertIn("Invalid", result)
    
    def test_non_numeric_board_sizes(self):
        for size in ["abc", "3.5", "seven", "10a"]:
            with self.subTest(size=size):
                result = self.game_logic.g_verify(size)
                self.assertIsInstance(result, str)
                self.assertIn("Invalid", result)
    
    def test_empty_board_size(self):
        result = self.game_logic.g_verify("")
        self.assertIsInstance(result, str)
        self.assertIn("Invalid", result)
    
    def test_valid_letter_placement(self):
        self.game_logic.g_verify("5")
        original_turn = self.game_logic.turn
        result = self.game_logic.letter_placement(2, 3, "S")
        self.assertTrue(result)
        self.assertEqual(self.game_logic.grid[2][3], "S")
        self.assertNotEqual(self.game_logic.turn, original_turn)
    
    def test_invalid_letter_placement_occupied_cell(self):
        self.game_logic.g_verify("5")
        self.game_logic.letter_placement(2, 3, "S")
        original_turn = self.game_logic.turn
        result = self.game_logic.letter_placement(2, 3, "O")
        self.assertFalse(result)
        self.assertEqual(self.game_logic.grid[2][3], "S")
        self.assertEqual(self.game_logic.turn, original_turn)
    
    def test_switch_turn(self):
        self.game_logic.turn = "Red"
        self.game_logic.switch()
        self.assertEqual(self.game_logic.turn, "Blue")
        self.game_logic.switch()
        self.assertEqual(self.game_logic.turn, "Red")


class TestGameGUI(unittest.TestCase):
    @patch('tkinter.Tk')
    def setUp(self, mock_tk):
        self.gui = SoS_GUI()
        self.gui.root = MagicMock()
        self.gui.sos_logic = GLogic()
        self.mock_logic = MagicMock()
        self.mock_logic.players = {'Red': None, 'Blue': None}
    
    @patch('tkinter.messagebox.showerror')
    def test_simple_game_mode_selection(self, mock_showerror):
        self.gui.sos_logic = self.mock_logic
        self.gui.sos_logic.g_verify.return_value = 5
        self.gui.game_choice.set("Simple")
        self.gui.gsize_input = MagicMock()
        self.gui.gsize_input.get.return_value = "5"
        self.gui.display_board = MagicMock()
        self.gui.starting()
        self.assertEqual(self.gui.sos_logic.mode, "Simple")
        mock_showerror.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_default_game_mode(self, mock_showerror):
        self.assertEqual(self.gui.game_choice.get(), "Simple")
        self.gui.sos_logic = self.mock_logic
        self.gui.sos_logic.g_verify.return_value = 5
        self.gui.gsize_input = MagicMock()
        self.gui.gsize_input.get.return_value = "5"
        self.gui.display_board = MagicMock()
        self.gui.starting()
        self.assertEqual(self.gui.sos_logic.mode, "Simple")
        mock_showerror.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_general_game_mode_selection(self, mock_showerror):
        self.gui.sos_logic = self.mock_logic
        self.gui.sos_logic.g_verify.return_value = 5
        self.gui.game_choice.set("General")
        self.gui.gsize_input = MagicMock()
        self.gui.gsize_input.get.return_value = "5"
        self.gui.display_board = MagicMock()
        self.gui.starting()
        self.assertEqual(self.gui.sos_logic.mode, "General")
        mock_showerror.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_start_new_game_with_valid_settings(self, mock_showerror):
        self.gui.sos_logic = GLogic()
        self.gui.game_choice.set("General")
        self.gui.r_letter_choice.set("S")
        self.gui.b_letter_choice.set("O")
        self.gui.gsize_input = MagicMock()
        self.gui.gsize_input.get.return_value = "7"
        with patch.object(self.gui.sos_logic, 'g_verify', return_value=7):
            with patch.object(self.gui, 'display_board') as mock_display:
                self.gui.starting()
                self.assertEqual(self.gui.sos_logic.mode, "General")
                self.assertEqual(self.gui.sos_logic.players['Red'], "S")
                self.assertEqual(self.gui.sos_logic.players['Blue'], "O")
                mock_display.assert_called_once_with(7)
                mock_showerror.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_error_for_invalid_settings(self, mock_showerror):
        self.gui.sos_logic = self.mock_logic
        self.gui.sos_logic.g_verify.return_value = "Invalid gird size!"
        self.gui.gsize_input = MagicMock()
        self.gui.gsize_input.get.return_value = "abc"
        self.gui.display_board = MagicMock()
        self.gui.starting()
        mock_showerror.assert_called_once()
        self.gui.display_board.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_valid_move(self, mock_showerror):
        self.gui.sos_logic = self.mock_logic
        self.gui.sos_logic.turn = 'Red'
        self.gui.sos_logic.letter_placement.return_value = True
        self.gui.update_b = MagicMock()
        self.gui.update_turn = MagicMock()
        self.gui.move_letter(2, 3)
        self.gui.sos_logic.letter_placement.assert_called_once()
        self.gui.update_b.assert_called_once()
        self.gui.update_turn.assert_called_once()
        mock_showerror.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_invalid_move(self, mock_showerror):
        self.gui.sos_logic = self.mock_logic
        self.gui.sos_logic.turn = 'Blue'
        self.gui.sos_logic.letter_placement.return_value = False
        self.gui.update_b = MagicMock()
        self.gui.update_turn = MagicMock()
        self.gui.move_letter(2, 3)
        self.gui.sos_logic.letter_placement.assert_called_once()
        self.gui.update_b.assert_not_called()
        self.gui.update_turn.assert_not_called()
        mock_showerror.assert_called_once()


if __name__ == '__main__':
    unittest.main()
