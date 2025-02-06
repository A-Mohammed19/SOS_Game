import tkinter as tk

# Related to the board and its creation
class Board:
    # Setting up the board to be gsize squared
    def __init__(self, gsize):
        self.gsize = gsize
        self.board = [[''] * gsize for _ in range(gsize)]

    # Printing the board that was created
    def display(self):
        for row in self.board:
            print(row)


class Game_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SOS Game!")
        self.gboard = None
        self.players = []
        self.start()

    def start(self):
        # Grid size
        self.gsize_label = tk.Label(self.root, text="Grid Size:")
        self.gsize_label.pack()

        self.gsize_input = tk.Entry(self.root)
        self.gsize_input.pack()

        # Player 1 name
        self.p1_label = tk.Label(self.root, text="Name P1:")
        self.p1_label.pack()
        self.p1_input = tk.Entry(self.root)
        self.p1_input.pack()

        # Player 2 name
        self.p2_label = tk.Label(self.root, text="Name P2:")
        self.p2_label.pack()
        self.p2_input = tk.Entry(self.root)
        self.p2_input.pack()

        # Player types
        self.p1type = tk.StringVar(value="Human")
        self.p2type = tk.StringVar(value="Human")

        # Radiobuttons for Player 1
        tk.Radiobutton(
            self.root, text="Human", variable=self.p1type, value="Human", command=lambda: self.toggle_player_input(1)
        ).pack()
        tk.Radiobutton(
            self.root, text="Computer", variable=self.p1type, value="Computer", command=lambda: self.toggle_player_input(1)
        ).pack()

        # Radiobuttons for Player 2
        tk.Radiobutton(
            self.root, text="Human", variable=self.p2type, value="Human", command=lambda: self.toggle_player_input(2)
        ).pack()
        tk.Radiobutton(
            self.root, text="Computer", variable=self.p2type, value="Computer", command=lambda: self.toggle_player_input(2)
        ).pack()

        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def toggle_player_input(self, player_num):
        """Enable or disable the player's name input based on the selected type (Human/Computer)."""
        if player_num == 1:
            if self.p1type.get() == "Computer":
                self.p1_input.delete(0, tk.END)  
                self.p1_input.insert(0, "Computer") 
                self.p1_input.config(state=tk.DISABLED) 
            else:
                self.p1_input.config(state=tk.NORMAL)  
                if self.p1_input.get() == "Computer":
                    self.p1_input.delete(0, tk.END)  
        elif player_num == 2:
            if self.p2type.get() == "Computer":
                self.p2_input.delete(0, tk.END)  
                self.p2_input.insert(0, "Computer")  
                self.p2_input.config(state=tk.DISABLED)  
            else:
                self.p2_input.config(state=tk.NORMAL)  
                if self.p2_input.get() == "Computer":
                    self.p2_input.delete(0, tk.END) 

    def start_game(self):
        try:
            self.gsize = int(self.gsize_input.get())
            if self.gsize <= 2:
                raise ValueError("Grid too small")

            p1type = self.p1type.get()
            p2type = self.p2type.get()

            # Set player names based on their type
            if p1type == "Human":
                p1name = self.p1_input.get().strip() or "Player 1"
            else:
                p1name = "Computer"

            if p2type == "Human":
                p2name = self.p2_input.get().strip() or "Player 2"
            else:
                p2name = "Computer"

            self.gboard = Board(self.gsize)
            self.players = [(p1name, p1type), (p2name, p2type)]

            # Clear the initial setup widgets
            for widget in self.root.winfo_children():
                widget.destroy()

            # Recreate the game UI with the board and players
            self.setup_game_ui()
            print(f"Game Started: {p1name} vs {p2name} ({p1type} vs {p2type})")

        except ValueError as e:
            if hasattr(self, 'error_label'):
                self.error_label.destroy()
            error_message = "Error loading the game!"
            self.error_label = tk.Label(self.root, text=error_message, fg="red")
            self.error_label.pack()
            print(f"Details: {e}")

    def setup_game_ui(self):
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Left player label
        self.p1_label = tk.Label(self.main_frame, text=f"{self.players[0][0]} (Player 1)", font=("Arial", 12))
        self.p1_label.grid(row=0, column=0, padx=10)

        # Center board
        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.display_board(self.gsize)

        # Right player label
        self.p2_label = tk.Label(self.main_frame, text=f"{self.players[1][0]} (Player 2)", font=("Arial", 12))
        self.p2_label.grid(row=0, column=1, padx=10)

    def display_board(self, gsize):
        for i in range(gsize):
            for j in range(gsize):
                cell = tk.Label(self.grid_frame, text=" ", width=4, height=2, relief="solid")
                cell.grid(row=i, column=j, padx=2, pady=2)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = Game_GUI()
    gui.run()