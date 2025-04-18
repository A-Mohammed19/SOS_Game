import random
from Game_Logic import GeneralGame

class ComputerPlayer:
    def __init__(self, game_logic):
        self.game_logic = game_logic
    
    def make_move(self):
        """Make a move for the computer player"""
        # First try to find a move that completes an SOS
        winning_move = self.find_winning_move()
        if winning_move:
            return winning_move
        
        # If no winning move, choose a random empty cell and random letter
        empty_cells = [
            (i, j) 
            for i in range(len(self.game_logic.grid)) 
            for j in range(len(self.game_logic.grid)) 
            if self.game_logic.grid[i][j] == ' '
        ]
        
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        letter = random.choice(['S', 'O'])
        return row, col, letter
    
    def find_winning_move(self):
        """Look for existing patterns where adding a letter would complete SOS"""
        grid = self.game_logic.grid
        size = len(grid)
        directions = [(0,1),(1,0),(1,1),(1,-1)]
        
        for i in range(size):
            for j in range(size):
                if grid[i][j] != ' ':
                    continue
                
                # Check all directions for potential SOS completion
                for dr, dc in directions:
                    # Check S-O-_ pattern (needs S at end)
                    if (0 <= i+dr < size and 0 <= j+dc < size and
                        0 <= i+2*dr < size and 0 <= j+2*dc < size):
                        if (grid[i+dr][j+dc] == 'O' and 
                            grid[i+2*dr][j+2*dc] == 'S'):
                            return (i, j, 'S')
                    
                    # Check _-O-S pattern (needs S at start)
                    if (0 <= i-dr < size and 0 <= j-dc < size and
                        0 <= i-2*dr < size and 0 <= j-2*dc < size):
                        if (grid[i-dr][j-dc] == 'O' and 
                            grid[i-2*dr][j-2*dc] == 'S'):
                            return (i, j, 'S')
                    
                    # Check S-_ -S pattern (needs O in middle)
                    if (0 <= i-dr < size and 0 <= j-dc < size and
                        0 <= i+dr < size and 0 <= j+dc < size):
                        if (grid[i-dr][j-dc] == 'S' and 
                            grid[i+dr][j+dc] == 'S'):
                            return (i, j, 'O')
        
        return None