#Creating the Logic for to move the letters on the grid 
class GLogic:    
    def __init__(self):
        self.mode= None 
        self.players={'Red': 'S', 'Blue':'S'} 
        self.turn='Blue'
        self.grid=None 
   
    def switch(self): 
        self.turn='Red' if self.turn =='Blue' else 'Blue'
        print(f"Current turn {self.turn}")
                
    def letter_placement(self, row, col, letter_choice):
        print(f"Attempting to place {letter_choice} at ({row}, {col})")
        print(f"Grid before move: {self.grid}")
        if self.grid is not None and self.grid[row][col]==" ":
            self.grid[row][col] = letter_choice
            self.switch()
            print(f"Grid after move: {self.grid}")

            return True 
        else:
            print("occupied")

            return False

    def g_verify(self,gsize_input):
        print(f"verity Size entered: {gsize_input}")
        try: 
            gsize=int(gsize_input)
            if gsize < 3 or gsize >10:
                raise ValueError("Grid too small")
            self.grid =[[" " for _ in range(gsize)] for _ in range(gsize)]
            return gsize 
        except ValueError:
            print(f"Invalid grid size input: {gsize_input}")  # Debugging print statement
            return "Invalid gird size!"
            