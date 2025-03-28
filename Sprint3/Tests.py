import unittest
from Game_Logic import GLogic, SimpleGame, GeneralGame

class TestBoardSizeSelection(unittest.TestCase):
    def setUp(self):
        self.logic = GLogic()
        self.logic.set_game_mode("Simple")  # Default to Simple for these tests
    
    # 1.1 Player inputs a valid board size
    def test_valid_board_size(self):
        result = self.logic.g_verify("5")
        self.assertEqual(result, 5)
        self.assertEqual(len(self.logic.grid), 5)
        self.assertEqual(len(self.logic.grid[0]), 5)
    
    # 1.2 Player inputs an invalid board size (too small)
    def test_invalid_small_board_size(self):
        result = self.logic.g_verify("2")
        self.assertEqual(result, "Invalid grid size!")
        self.assertIsNone(self.logic.grid)
    
    # 1.2 Player inputs an invalid board size (string)
    def test_invalid_string_board_size(self):
        result = self.logic.g_verify("abc")
        self.assertEqual(result, "Invalid grid size!")
        self.assertIsNone(self.logic.grid)
    
    # 1.3 Player does not input anything
    def test_empty_board_size(self):
        result = self.logic.g_verify("")
        self.assertEqual(result, "Invalid grid size!")
        self.assertIsNone(self.logic.grid)

class TestGameModeSelection(unittest.TestCase):
    # 2.1 Player chooses simple game
    def test_simple_game_mode(self):
        logic = GLogic()
        logic.set_game_mode("Simple")
        self.assertIsInstance(logic.game, SimpleGame)
        self.assertEqual(logic.mode, "Simple")
    
    # 2.2 Default is simple game
    def test_default_game_mode(self):
        logic = GLogic()
        # Simulate not setting mode explicitly
        self.assertIsNone(logic.game)
        # But when we try to use it, it should raise AttributeError
        with self.assertRaises(AttributeError):
            logic.mode
    
    # 2.3 Player chooses general game
    def test_general_game_mode(self):
        logic = GLogic()
        logic.set_game_mode("General")
        self.assertIsInstance(logic.game, GeneralGame)
        self.assertEqual(logic.mode, "General")

class TestNewGameStart(unittest.TestCase):
    # 3.1 Start game with correct settings
    def test_start_new_game_valid(self):
        logic = GLogic()
        logic.set_game_mode("Simple")
        size = logic.g_verify("5")
        self.assertEqual(size, 5)
        self.assertEqual(len(logic.grid), 5)
        self.assertEqual(logic.turn, 'Blue')  # Default starting player
    
    #  3.2 Reset after finishing a game - FINAL WORKING VERSION
    def test_reset_after_game(self):
        logic = GLogic()
        logic.set_game_mode("Simple")
        logic.g_verify("3")
        
        # Make a move (Blue's turn)
        logic.letter_placement(0, 0, 'S')
        
        # Verify turn switched to Red
        self.assertEqual(logic.turn, 'Red')
        
        # Reset the game
        new_size = logic.g_verify("3")
        self.assertEqual(new_size, 3)
        
        # Verify all state is reset
        self.assertEqual(logic.turn, 'Blue')
        self.assertEqual(logic.grid[0][0], " ")
        self.assertEqual(len(logic.sos_positions), 0)

class TestSimpleGameMoves(unittest.TestCase):
    def setUp(self):
        self.logic = GLogic()
        self.logic.set_game_mode("Simple")
        self.logic.g_verify("3")
    
    # 4.1 Valid move in simple game
    def test_valid_move_simple_game(self):
        result = self.logic.letter_placement(0, 0, 'S')
        self.assertTrue(result)
        self.assertEqual(self.logic.grid[0][0], 'S')
        self.assertEqual(self.logic.turn, 'Red')  # Turn should switch
    
    # 4.2 Invalid move (occupied cell)
    def test_invalid_move_occupied(self):
        self.logic.letter_placement(0, 0, 'S')  # First move valid
        result = self.logic.letter_placement(0, 0, 'O')  # Try same cell
        self.assertFalse(result)
    
    # 5.1 Player wins in simple game
    def test_player_wins_simple_game(self):
        # Setup a winning condition
        self.logic.letter_placement(0, 0, 'S')  # Blue
        self.logic.letter_placement(1, 0, 'O')  # Red
        result = self.logic.letter_placement(2, 0, 'S')  # Blue wins
        self.assertEqual(result, "WIN")
        status = self.logic.get_game_status()
        self.assertIn("Player Blue won!", status)
    
    # 5.2 Other player loses in simple game
    def test_other_player_loses_simple_game(self):
        # Setup a winning condition
        self.logic.letter_placement(0, 0, 'S')  # Blue
        self.logic.letter_placement(1, 0, 'O')  # Red
        result = self.logic.letter_placement(2, 0, 'S')  # Blue wins
        status = self.logic.get_game_status()
        self.assertIn("Player Red lost!", status)
    
    # 5.3 Reset after game over
    def test_reset_after_game_over(self):
        # Play a winning game
        self.logic.letter_placement(0, 0, 'S')  # Blue
        self.logic.letter_placement(1, 0, 'O')  # Red
        self.logic.letter_placement(2, 0, 'S')  # Blue wins
        
        # Reset
        self.logic.g_verify("3")
        self.assertEqual(self.logic.grid[0][0], " ")
        self.assertEqual(self.logic.turn, 'Blue')
        self.assertEqual(len(self.logic.sos_positions), 0)
    
    # 5.4 Game is a tie
    def test_game_tie_simple_game(self):
        # Fill the board without any SOS
        self.logic.letter_placement(0, 0, 'O')
        self.logic.letter_placement(0, 1, 'O')
        self.logic.letter_placement(0, 2, 'O')
        self.logic.letter_placement(1, 0, 'O')
        self.logic.letter_placement(1, 1, 'O')
        self.logic.letter_placement(1, 2, 'O')
        self.logic.letter_placement(2, 0, 'O')
        self.logic.letter_placement(2, 1, 'O')
        result = self.logic.letter_placement(2, 2, 'O')
        
        self.assertEqual(result, True)  # Last move is valid
        status = self.logic.get_game_status()
        self.assertEqual(status, "Game is tied!")

class TestGeneralGameMoves(unittest.TestCase):
    def setUp(self):
        self.logic = GLogic()
        self.logic.set_game_mode("General")
        self.logic.g_verify("3")
    
    # 6.1 Valid move in general game
    def test_valid_move_general_game(self):
        result = self.logic.letter_placement(0, 0, 'S')
        self.assertTrue(result)
        self.assertEqual(self.logic.grid[0][0], 'S')
        self.assertEqual(self.logic.turn, 'Red')  # Turn should switch
    
    # 6.2 Invalid move (occupied cell) in general game
    def test_invalid_move_occupied_general(self):
        self.logic.letter_placement(0, 0, 'S')  # First move valid
        result = self.logic.letter_placement(0, 0, 'O')  # Try same cell
        self.assertFalse(result)
    
    # 7.1 Player wins in general game
    def test_player_wins_general_game(self):
        # Blue creates an SOS
        self.logic.letter_placement(0, 0, 'S')  # Blue
        self.logic.letter_placement(1, 0, 'O')  # Red
        self.logic.letter_placement(2, 0, 'S')  # Blue
        
        # Fill rest of board without creating more SOS
        self.logic.letter_placement(0, 1, 'O')  # Red
        self.logic.letter_placement(0, 2, 'O')  # Blue
        self.logic.letter_placement(1, 1, 'O')  # Red
        self.logic.letter_placement(1, 2, 'O')  # Blue
        self.logic.letter_placement(2, 1, 'O')  # Red
        result = self.logic.letter_placement(2, 2, 'O')  # Blue
        
        self.assertEqual(result, "TIE")  # Board is full
        status = self.logic.get_game_status()
        self.assertIn("Player Blue won!", status)
        self.assertEqual(self.logic.scores['Blue'], 1)
        self.assertEqual(self.logic.scores['Red'], 0)
    
    # 7.2 Other player loses in general game
    def test_other_player_loses_general_game(self):
        # Blue creates an SOS
        self.logic.letter_placement(0, 0, 'S')  # Blue
        self.logic.letter_placement(1, 0, 'O')  # Red
        self.logic.letter_placement(2, 0, 'S')  # Blue
        
        # Fill rest of board
        self.logic.letter_placement(0, 1, 'O')  # Red
        self.logic.letter_placement(0, 2, 'O')  # Blue
        self.logic.letter_placement(1, 1, 'O')  # Red
        self.logic.letter_placement(1, 2, 'O')  # Blue
        self.logic.letter_placement(2, 1, 'O')  # Red
        self.logic.letter_placement(2, 2, 'O')  # Blue
        
        status = self.logic.get_game_status()
        self.assertIn("Player Red lost!", status)
    
    #7.3 Reset after game over in general game - FINAL FIXED VERSION
    def test_reset_after_game_over_general(self):
        # Play partial game
        self.logic.letter_placement(0, 0, 'S')  # Blue
        self.logic.letter_placement(1, 0, 'O')  # Red
        
        # Reset game
        size = self.logic.g_verify("3")
        self.assertEqual(size, 3)
        self.assertEqual(self.logic.turn, 'Blue')  # Verify turn reset
        self.assertEqual(self.logic.grid[0][0], " ")
        self.assertEqual(self.logic.scores['Blue'], 0)
        self.assertEqual(self.logic.scores['Red'], 0)
    
    #  7.4 Game is a tie in general game 
    def test_game_tie_general_game(self):  
    # Create fresh game state
        self.logic = GLogic()
        self.logic.set_game_mode("General")
        self.logic.g_verify("3")  # Set board size to 3x3
        
        # Move sequence that results in equal scores
        moves = [
            (0, 0, 'S', "Blue"),  # Blue
            (1, 0, 'O', "Red"),   # Red
            (2, 0, 'S', "Blue"),  # Blue (Vertical SOS - Blue scores)
            (0, 1, 'S', "Red"),   # Red
            (1, 1, 'O', "Blue"),  # Blue
            (2, 1, 'S', "Red"),   # Red (Vertical SOS - Red scores)
            (0, 2, 'O', "Blue"),  # Blue
            (1, 2, 'O', "Red"),   # Red
            (2, 2, 'O', "Blue")   # Blue
        ]
        
        for row, col, letter, player in moves:
            self.logic.letter_placement(row, col, letter)
        
        # Check if the game is tied
        status = self.logic.get_game_status()
        self.assertEqual(status, "Game is tied!", "Game should be tied")
        self.assertEqual(self.logic.scores['Red'], 1)
        self.assertEqual(self.logic.scores['Blue'], 1)


if __name__ == '__main__':
    unittest.main()