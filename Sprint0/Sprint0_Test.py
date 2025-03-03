import unittest
from Sprint0_Game import Board, Game_GUI  
import tkinter as tk


class Testing(unittest.TestCase):
    def test_board(self):
        size = 5
        board = Board(size)
        self.assertEqual(len(board.board), size)  
        self.assertEqual(len(board.board[0]), size)  
        self.assertTrue(all(cell == '' for row in board.board for cell in row))  

    def test_player_name(self):
        game = Game_GUI()

        
        game.p1_input.insert(0, "")  
        game.p2_input.insert(0, "Abdul")  

        
        game.p1type.set("Human")
        game.p2type.set("Computer")

        
        game.gsize_input.insert(0, "5")  

        
        game.start_game()

        
        self.assertEqual(game.players[0][0], "Player 1")  
        self.assertEqual(game.players[1][0], "Computer")  

if __name__ == "__main__":
    unittest.main()
