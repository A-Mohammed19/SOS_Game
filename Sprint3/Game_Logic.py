class Base:
    def __init__(self):
        self.players = {'Red': 'S', 'Blue':'S'} 
        self.turn = 'Blue'
        self.grid = None 
        self.sos_positions = {}  
    
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
            # S at the front 
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
                            print(f"SOS found for {self.turn} at positions: {sos_pos}")

            # O in the middle
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
                            print(f"SOS found for {self.turn} at positions: {sos_pos}")

            # S at the end
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
                            print(f"SOS found for {self.turn} at positions: {sos_pos}")

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
            self.turn = 'Blue'  # Explicitly reset turn to Blue
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
            winner = self.turn  
            return f"Player {winner} won! Player {'Red' if winner == 'Blue' else 'Blue'} lost!"
        return None

# class for general game 
class GeneralGame(Base):
    def __init__(self):
        super().__init__()
        self.mode = "General"
        self.scores = {'Red': 0, 'Blue': 0}

    def letter_placement(self, row, col, letter_choice):
        print(f"\nAttempting to place {letter_choice} at ({row}, {col})")
        print(f"Current turn: {self.turn}")
        print(f"Current scores - Red: {self.scores['Red']}, Blue: {self.scores['Blue']}")
        print(f"Grid before move: {self.grid}")
        
        if self.grid is not None and self.grid[row][col]==" ":
            self.grid[row][col] = letter_choice
            sos_found = self.check_sos(row, col)
            if sos_found:
                self.scores[self.turn] += 1
                print(f"SOS found! {self.turn} scores: {self.scores[self.turn]}")
                # Switch turns even if SOS is found
                self.switch()
                print(f"Grid after move: {self.grid}")
                print(f"Updated scores - Red: {self.scores['Red']}, Blue: {self.scores['Blue']}")
                return True
            if self.is_board_full():
                print("Board is full!")
                return "TIE"
            # Switch turns if no SOS was found
            self.switch()
            print(f"Grid after move: {self.grid}")
            print(f"Updated scores - Red: {self.scores['Red']}, Blue: {self.scores['Blue']}")
            return True 
        else:
            print("occupied")
            return False

    def get_game_status(self):
        """Get the current game status"""
        if self.is_board_full():
            print("\nGame Over!")
            print(f"Final scores - Red: {self.scores['Red']}, Blue: {self.scores['Blue']}")
            print(f"Current turn: {self.turn}")
            # Compare scores to determine winner
            if self.scores['Red'] > self.scores['Blue']:
                return "Player Red won! Player Blue lost!"
            elif self.scores['Blue'] > self.scores['Red']:
                return "Player Blue won! Player Red lost!"
            else:
                return "Game is tied!"
        return None

    

# refactored to make it set thge game mode and call the required methods based on the game mode 
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
    def __getattr__(self, name):
        if self.game is None:
            raise AttributeError("Game mode not set")
        return getattr(self.game, name)
            