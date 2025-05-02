#refactored to add components for the computer player 
class Base:
    def __init__(self):
        self.players = {'Red': 'S', 'Blue':'S'} 
        self.player_types = {'Red': 'Human', 'Blue': 'Human'}  #track player types
        self.turn = 'Blue' #
        self.grid = None 
        self.sos_positions = {}  
        self.last_starting_player = 'Red'  # Track last starting player
    
    def switch(self): 
        self.turn = 'Red' if self.turn == 'Blue' else 'Blue'
        print(f"Current turn {self.turn}")

    def check_sos(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  
                    (1, 1), (-1, -1), (1, -1), (-1, 1)]  
        
        sos_found = False
        current_letter = self.grid[row][col]
        
        if self.turn not in self.sos_positions:
            self.sos_positions[self.turn] = []

        for dr, dc in directions:
            # Only check valid SOS patterns (S-O-S)
            # Pattern 1: S at start (S-O-_ needs S at end)
            if current_letter == 'S':
                if (0 <= row + dr < len(self.grid) and 
                    0 <= col + dc < len(self.grid) and
                    0 <= row + 2*dr < len(self.grid) and 
                    0 <= col + 2*dc < len(self.grid)):
                    
                    if (self.grid[row + dr][col + dc] == 'O' and 
                        self.grid[row + 2*dr][col + 2*dc] == 'S'):
                        sos_pos = [
                            (row, col),
                            (row + dr, col + dc),
                            (row + 2*dr, col + 2*dc)
                        ]
                        if sos_pos not in self.sos_positions[self.turn]:
                            self.sos_positions[self.turn].append(sos_pos)
                            sos_found = True
                            print(f"Valid SOS found for {self.turn} at positions: {sos_pos}")

            # Pattern 2: O in middle (S-O-S)
            if current_letter == 'O':
                if (0 <= row - dr < len(self.grid) and 
                    0 <= col - dc < len(self.grid) and
                    0 <= row + dr < len(self.grid) and 
                    0 <= col + dc < len(self.grid)):
                    
                    if (self.grid[row - dr][col - dc] == 'S' and 
                        self.grid[row + dr][col + dc] == 'S'):
                        sos_pos = [
                            (row - dr, col - dc),
                            (row, col),
                            (row + dr, col + dc)
                        ]
                        if sos_pos not in self.sos_positions[self.turn]:
                            self.sos_positions[self.turn].append(sos_pos)
                            sos_found = True
                            print(f"Valid SOS found for {self.turn} at positions: {sos_pos}")

            # Pattern 3: S at end (_O-S needs S at start)
            if current_letter == 'S':
                if (0 <= row - 2*dr < len(self.grid) and
                    0 <= col - 2*dc < len(self.grid) and
                    0 <= row - dr < len(self.grid) and 
                    0 <= col - dc < len(self.grid)):
                    
                    if (self.grid[row - 2*dr][col - 2*dc] == 'S' and 
                        self.grid[row - dr][col - dc] == 'O'):
                        sos_pos = [
                            (row - 2*dr, col - 2*dc),
                            (row - dr, col - dc),
                            (row, col)
                        ]
                        if sos_pos not in self.sos_positions[self.turn]:
                            self.sos_positions[self.turn].append(sos_pos)
                            sos_found = True
                            print(f"Valid SOS found for {self.turn} at positions: {sos_pos}")

        return sos_found

    def is_board_full(self):
        return all(cell != " " for row in self.grid for cell in row)

    
    def g_verify(self, gsize_input):
        try:
            gsize = int(gsize_input)
            if gsize < 3 or gsize > 10:
                raise ValueError("Grid too small")
            self.grid = [[" " for _ in range(gsize)] for _ in range(gsize)]
            self.sos_positions = {}
            # Force reset to Blue player
            self.turn = 'Blue'
            self.last_starting_player = 'Red'  # Next game will start with Red
            return gsize
        except ValueError:
            return "Invalid grid size!"

# Class for simple game 
class SimpleGame(Base):
    def __init__(self):
        super().__init__()
        self.mode = "Simple"

    def letter_placement(self, row, col, letter_choice):
        print(f"Attempting to place {letter_choice} at ({row}, {col})")
        print(f"Grid before move: {self.grid}")
        if self.grid is not None and self.grid[row][col]==" ":
            self.grid[row][col] = letter_choice
            print(f"Grid after move: {self.grid}")
        
            sos_found = self.check_sos(row, col)
            if sos_found:
                return "WIN"
            self.switch()
            print(f"Grid after move: {self.grid}")
            return True 
        else:
            print("occupied")
            return False

    def get_game_status(self):
        if self.is_board_full():
            if not any(self.sos_positions.values()):
                return "Game is tied!"
        if any(self.sos_positions.values()):
            # Find the player who has SOS sequences
            for player, positions in self.sos_positions.items():
                if positions:  # If this player has any SOS sequences
                    return f"Player {player} won! Player {'Red' if player == 'Blue' else 'Blue'} lost!"
        return None

# class for general game 
class GeneralGame(Base):
    def __init__(self):
        super().__init__()
        self.mode = "General"
        self.scores = {'Red': 0, 'Blue': 0}

    def letter_placement(self, row, col, letter_choice):
        if self.grid is not None and self.grid[row][col] == " ":
            self.grid[row][col] = letter_choice
            sos_found = self.check_sos(row, col)
            if sos_found:
                self.scores[self.turn] += 1
                return "AGAIN"  # Stay on the same player's turn

            if self.is_board_full():
                return "TIE"

            self.switch()
            return True
        return False
    def get_game_status(self):
        if self.is_board_full():
            if self.scores['Red'] == self.scores['Blue']:
                return "Game is tied!"
            winner = 'Red' if self.scores['Red'] > self.scores['Blue'] else 'Blue'
            return f"Player {winner} won! Player {'Red' if winner == 'Blue' else 'Blue'} lost!"
        return None

    

class GLogic:
    def __init__(self):
        self.game = None
        
    def set_game_mode(self, mode):
        if mode == "Simple":
            self.game = SimpleGame()
        elif mode == "General":
            self.game = GeneralGame()
        else:
            raise ValueError("Invalid game mode")
            
    def set_player_type(self, color, player_type):
        if self.game:
            self.game.player_types[color] = player_type
            print(f"Set {color} player to {player_type}")
            
    def get_player_type(self, color):
        if self.game:
            return self.game.player_types[color]
        return "Human" 
            
    def __getattr__(self, name):
        if self.game is None:
            raise AttributeError("Game mode not set")
        return getattr(self.game, name)