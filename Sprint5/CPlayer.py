import random
from Game_Logic import Base

class Player(Base):
    def __init__(self, game_logic, player_color=None):
        super().__init__()
        self.game_logic = game_logic
        self.player_color = player_color
        self.score = 0
        self.moves_made = 0
    
    def make_move(self):
        raise NotImplementedError("Subclasses must implement make_move method")
    
    def get_empty_cells(self):
        return [
            (i, j) 
            for i in range(len(self.game_logic.grid)) 
            for j in range(len(self.game_logic.grid)) 
            if self.game_logic.grid[i][j] == ' '
        ]
    
    def is_valid_move(self, row, col):
        grid_size = len(self.game_logic.grid)
        return (0 <= row < grid_size and 
                0 <= col < grid_size and 
                self.game_logic.grid[row][col] == ' ')
    
    def increment_score(self, points=1):
        self.score += points
        
    def reset_stats(self):
        self.score = 0
        self.moves_made = 0
    
    def record_move(self):
        self.moves_made += 1


class ComputerPlayer(Player):
    def __init__(self, game_logic, difficulty='normal', player_color=None):
        super().__init__(game_logic, player_color)
        self.difficulty = difficulty
    
    def make_move(self):
        if self.difficulty == 'easy':
            return self._make_random_move()
            
        winning_move = self.find_winning_move()
        if winning_move:
            self.record_move()
            return winning_move
        
        if self.difficulty == 'hard':
            blocking_move = self._find_blocking_move()
            if blocking_move:
                self.record_move()
                return blocking_move
        
        return self._make_random_move()
    
    def _make_random_move(self):
        """Make a random move in an empty cell"""
        empty_cells = self.get_empty_cells()
        
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        letter = random.choice(['S', 'O'])
        self.record_move()
        return row, col, letter
    
    def find_winning_move(self):
        grid = self.game_logic.grid
        size = len(grid)
        directions = [(0,1),(1,0),(1,1),(1,-1)]
        
        for i in range(size):
            for j in range(size):
                if grid[i][j] != ' ':
                    continue
                
                for dr, dc in directions:
                    # Check S-O-
                    if (0 <= i+dr < size and 0 <= j+dc < size and
                        0 <= i+2*dr < size and 0 <= j+2*dc < size):
                        if (grid[i+dr][j+dc] == 'O' and 
                            grid[i+2*dr][j+2*dc] == 'S'):
                            return (i, j, 'S')
                    
                    # Check _-O-S
                    if (0 <= i-dr < size and 0 <= j-dc < size and
                        0 <= i-2*dr < size and 0 <= j-2*dc < size):
                        if (grid[i-dr][j-dc] == 'O' and 
                            grid[i-2*dr][j-2*dc] == 'S'):
                            return (i, j, 'S')
                    
                    # Check S-_-S 
                    if (0 <= i-dr < size and 0 <= j-dc < size and
                        0 <= i+dr < size and 0 <= j+dc < size):
                        if (grid[i-dr][j-dc] == 'S' and 
                            grid[i+dr][j+dc] == 'S'):
                            return (i, j, 'O')
        
        return None
        
    def _find_blocking_move(self):
        return self.find_winning_move()


class HumanPlayer(Player):
    def __init__(self, game_logic, player_color=None):
        super().__init__(game_logic, player_color)
    
    def make_move(self, row, col, letter):
        if not self.is_valid_move(row, col):
            return None
            
        if letter not in ['S', 'O']:
            return None
            
        self.record_move()
        return row, col, letter