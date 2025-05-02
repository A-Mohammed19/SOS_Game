from tkinter import *
from tkinter import messagebox, ttk
from Game_Logic import GLogic, GeneralGame
from CPlayer import ComputerPlayer
from Recording import GameRecorder
import time

class SoS_GUI: 
    def __init__(self):
        self.root = Tk()
        self.root.title("Ready...")
        self.root.configure(bg='black') 
        
        self.game_choice = StringVar(value="Simple")
        self.r_letter_choice = StringVar(value="S")
        self.b_letter_choice = StringVar(value="S")
        self.r_player_type = StringVar(value="Human")
        self.b_player_type = StringVar(value="Human")
        self.record_game = BooleanVar(value=False)
        
        self.create()
        
        self.sos_logic = GLogic()
        self.computer_player = None
        self.turn_label = None
        self.cells = {}
        self.score_labels = {}
        self.computer_thinking = False
        self.recorder = GameRecorder()
        self.replaying = False
        self.current_replay_move = 0
        self.replay_moves = []
        self.replay_game_id = None
        
    def mainloop(self):
        self.root.mainloop() 
    
    def display_board(self, gsize):
        if hasattr(self, 'grid_frame') and self.grid_frame:
            self.grid_frame.destroy()
        
        if hasattr(self, 'score_frame') and self.score_frame:
            self.score_frame.destroy()

        if hasattr(self, 'turn_label') and self.turn_label:
            self.turn_label.destroy()

        self.grid_frame = Frame(self.root, bg='black')
        self.grid_frame.grid(row=5, column=0, columnspan=3, rowspan=4, pady=10)

        self.cells.clear()
        
        for i in range(gsize):
            for j in range(gsize):
                cell = Button(self.grid_frame, text=" ", width=4, height=2, relief="solid",
                            command=lambda row=i, col=j: self.move_letter(row, col))
                cell.grid(row=i, column=j, padx=2, pady=2)
                self.cells[(i, j)] = cell  
        
        # score to keep track of points 
        self.score_frame = Frame(self.root, bg='black')
        self.score_frame.grid(row=16, column=0, columnspan=3, pady=5)
        
        # colorized labels for players 
        self.score_labels['Red'] = Label(self.score_frame, text="Red: 0", 
                                       bg='black', fg='red', 
                                       font=("Times New Roman", 12))
        self.score_labels['Red'].pack(side=LEFT, padx=20)
        
        self.score_labels['Blue'] = Label(self.score_frame, text="Blue: 0", 
                                        bg='black', fg='blue', 
                                        font=("Times New Roman", 12))
        self.score_labels['Blue'].pack(side=LEFT, padx=20)
        
        self.turn_label = Label(self.root, text=f"{self.sos_logic.turn}'s Turn", 
                             bg='black', fg='white', font=("Times New Roman", 14))
        self.turn_label.grid(row=15, column=1, pady=5)
        
        self.update_letter_choice_visibility()
        
        self.computer_player = ComputerPlayer(self.sos_logic)
        self.check_computer_turn()
        
        self.update_board()
    
    def highlight_sos(self):
        for cell in self.cells.values():
            cell.config(bg='SystemButtonFace', fg='black')
            
        for player, positions in self.sos_logic.sos_positions.items():
            player_color = 'red' if player == 'Red' else 'blue'
            
            for sos_sequence in positions:
                for row, col in sos_sequence:
                    if (row, col) in self.cells:
                        self.cells[(row, col)].config(bg=player_color)
                        self.cells[(row, col)].config(fg='white')
                        
        self.root.update_idletasks()
    
    def update_scoreboard(self):
        if isinstance(self.sos_logic.game, GeneralGame):
            red_score = self.sos_logic.scores.get('Red', 0)
            blue_score = self.sos_logic.scores.get('Blue', 0)
            
            self.score_labels['Red'].config(text=f"Red: {red_score}")
            self.score_labels['Blue'].config(text=f"Blue: {blue_score}")
            
            self.root.update_idletasks()
    
    def check_computer_turn(self):
        if not self.computer_thinking and self.sos_logic.grid is not None and not self.replaying:
            current_player = self.sos_logic.turn
            player_type = self.sos_logic.get_player_type(current_player)
            
            if player_type == "Computer":
                self.computer_thinking = True
                self.root.after(500, self.make_computer_move)
    
    def make_computer_move(self):
        if self.computer_player and not self.check_game_over() and not self.replaying:
            try:
                move_result = self.computer_player.make_move()

                if move_result:
                    row, col, letter = move_result

                    if self.sos_logic.turn == 'Red':
                        self.sos_logic.players['Red'] = letter
                    else:
                        self.sos_logic.players['Blue'] = letter

                    result = self.sos_logic.letter_placement(row, col, letter)

                    if result:
                        # Record the move if recording is enabled
                        if self.record_game.get() and self.recorder.recording:
                            self.recorder.record_move(self.sos_logic.turn, row, col, letter)

                        self.update_board()
                        self.update_scoreboard()
                        self.highlight_sos()

                        if self.check_game_over():
                            self.computer_thinking = False
                            return

                        if result == "AGAIN":
                            # Stay on current player, call again
                            self.root.after(500, self.make_computer_move)
                        else:
                            self.update_turn()
                            self.computer_thinking = False
                            self.check_computer_turn()
                    else:
                        self.computer_thinking = False  # Just in case of invalid move
            except Exception as e:
                print(f"Error in computer move: {e}")
                self.computer_thinking = False
    
    def check_game_over(self):
        status = self.sos_logic.get_game_status()
        if status:
            winner = None
            red_score = 0
            blue_score = 0
            
            if isinstance(self.sos_logic.game, GeneralGame):
                red_score = self.sos_logic.scores.get('Red', 0)
                blue_score = self.sos_logic.scores.get('Blue', 0)
                winner = 'Red' if red_score > blue_score else 'Blue' if blue_score > red_score else None
            
            if "won" in status:
                winner = status.split(" ")[1].replace("!", "")
            
            if self.record_game.get() and self.recorder.recording:
                self.recorder.end_recording(winner, red_score, blue_score)
            
            messagebox.showinfo("Game Over", status)
            self.root.title("Ready for New Game")
            self.r_player_frame.grid(row=2, column=0, pady=5)
            self.b_player_frame.grid(row=2, column=2, pady=5)
            return True
        return False
                
    def move_letter(self, row, col): #human
        if self.replaying:
            return
            
        current_player = self.sos_logic.turn
        if self.sos_logic.get_player_type(current_player) == "Computer":
            messagebox.showinfo("Computer's Turn", "Please wait for the computer to make a move.")
            return
            
        if self.sos_logic.turn == 'Red':
            letter_choice = self.r_letter_choice.get()
        else:
            letter_choice = self.b_letter_choice.get()
            
        self.sos_logic.players[self.sos_logic.turn] = letter_choice
        
        result = self.sos_logic.letter_placement(row, col, letter_choice)
        if result:
            # Record the move if recording is enabled
            if self.record_game.get() and self.recorder.recording:
                self.recorder.record_move(self.sos_logic.turn, row, col, letter_choice)
            
            self.cells[(row, col)].config(text=letter_choice)
            self.update_turn()
            self.update_scoreboard()
            self.highlight_sos()  # highlight sos 
            
            status = self.sos_logic.get_game_status()
            if status:
                messagebox.showinfo("Game Over", status)
                self.root.title("Ready for New Game")
                self.r_player_frame.grid(row=2, column=0, pady=5)
                self.b_player_frame.grid(row=2, column=2, pady=5)
                return
            
            self.check_computer_turn()
        else:
            messagebox.showerror("Error", "Invalid move, cell is occupied")
            
    def update_board(self):
        if not self.sos_logic.grid:
            return
            
        print(f"Updating board with grid: {self.sos_logic.grid}")  # Debug print
        
        for i in range(len(self.sos_logic.grid)):
            for j in range(len(self.sos_logic.grid[i])):
                cell_value = self.sos_logic.grid[i][j]
                if (i, j) in self.cells:
                    self.cells[(i, j)].config(text=cell_value if cell_value else " ")
                    # Force the update to show immediately
                    self.cells[(i, j)].update()
        
        self.highlight_sos()
        self.root.update_idletasks()
    
    def update_turn(self):
        if self.turn_label:
            self.turn_label.config(text=f"{self.sos_logic.turn}'s Turn")
            
            if self.sos_logic.turn == 'Red':
                self.turn_label.config(fg='red')
            else:
                self.turn_label.config(fg='blue')
    
    def update_letter_choice_visibility(self):
        r_type = self.r_player_type.get()
        b_type = self.b_player_type.get()
        
        if r_type == "Human":
            self.r_label.grid()
            self.rS.grid()
            self.rO.grid()
        else:
            self.r_label.grid_remove()
            self.rS.grid_remove()
            self.rO.grid_remove()
            
        if b_type == "Human":
            self.b_label.grid()
            self.bS.grid()
            self.bO.grid()
        else:
            self.b_label.grid_remove()
            self.bS.grid_remove()
            self.bO.grid_remove()
   
    def create(self):
        # title 
        self.game_title = Label(self.root, text="SOS Game!", 
                              font=("Times New Roman", 20, "bold"), 
                              bg='black', fg='white')
        self.game_title.grid(row=0, column=0, columnspan=3, pady=10)
        
        #game mode selection
        self.Simple = Radiobutton(self.root, text='Simple Game', 
                                variable=self.game_choice, value="Simple", 
                                bg='black', fg='white', selectcolor='black')
        self.Simple.grid(row=1, column=0, pady=5)
        
        self.General = Radiobutton(self.root, text='General Game', 
                                 variable=self.game_choice, value="General", 
                                 bg='black', fg='white', selectcolor='black')
        self.General.grid(row=1, column=2, pady=5)
        
        # Type of player for Red
        self.r_player_frame = Frame(self.root, bg='black')
        self.r_player_frame.grid(row=2, column=0, pady=5)
        
        self.r_player_label = Label(self.r_player_frame, text="Red Player:", bg='black', fg='white')
        self.r_player_label.pack(side=LEFT)
        
        self.r_human = Radiobutton(self.r_player_frame, text='Human', 
                                  variable=self.r_player_type, value="Human", 
                                  bg='black', fg='white', selectcolor='black',
                                  command=self.update_letter_choice_visibility)
        self.r_human.pack(side=LEFT)
        
        self.r_computer = Radiobutton(self.r_player_frame, text='Computer', 
                                     variable=self.r_player_type, value="Computer", 
                                     bg='black', fg='white', selectcolor='black',
                                     command=self.update_letter_choice_visibility)
        self.r_computer.pack(side=LEFT)
        
        # Type of player for  Blue
        self.b_player_frame = Frame(self.root, bg='black')
        self.b_player_frame.grid(row=2, column=2, pady=5)
        
        self.b_player_label = Label(self.b_player_frame, text="Blue Player:", bg='black', fg='white')
        self.b_player_label.pack(side=LEFT)
        
        self.b_human = Radiobutton(self.b_player_frame, text='Human', 
                                  variable=self.b_player_type, value="Human", 
                                  bg='black', fg='white', selectcolor='black',
                                  command=self.update_letter_choice_visibility)
        self.b_human.pack(side=LEFT)
        
        self.b_computer = Radiobutton(self.b_player_frame, text='Computer', 
                                     variable=self.b_player_type, value="Computer", 
                                     bg='black', fg='white', selectcolor='black',
                                     command=self.update_letter_choice_visibility)
        self.b_computer.pack(side=LEFT)
        
        #box for grid size  
        self.gsize_lable = Label(self.root, text="Grid Size:", bg='black', fg='white')
        self.gsize_lable.grid(row=3, column=1, pady=5)

        self.gsize_input = Entry(self.root, bg='black', fg='white', width=10) 
        self.gsize_input.grid(row=4, column=1, pady=5)
        
        # Record game checkbox
        self.record_check = Checkbutton(self.root, text="Record Game", 
                                      variable=self.record_game,
                                      bg='black', fg='white', selectcolor='black')
        self.record_check.grid(row=3, column=0, pady=5)
        
        # Replay controls
        self.replay_button = Button(self.root, text="Replay Game", 
                                   bg='black', fg='white',
                                   command=self.show_replay_dialog)
        self.replay_button.grid(row=3, column=2, pady=5)
        
        #Letters choice = Red player
        self.r_label = Label(self.root, text="Red Player", bg='black', fg='red')
        self.r_label.grid(row=10, column=0, pady=5, sticky='e')                         
         
        self.rS = Radiobutton(self.root, text='S', variable=self.r_letter_choice, 
                            value="S", bg='black', fg='red', selectcolor='black')
        self.rS.grid(row=11, column=0, pady=10, sticky='e')
        
        self.rO = Radiobutton(self.root, text='O', variable=self.r_letter_choice, 
                            value="O", bg='black', fg='red', selectcolor='black')
        self.rO.grid(row=12, column=0, pady=10, sticky='e')
        
        #Letters choice =  Blue player
        self.b_label = Label(self.root, text="Blue Player", bg='black', fg='blue')
        self.b_label.grid(row=10, column=2, pady=5, sticky='w')   
        
        self.bS = Radiobutton(self.root, text='S', variable=self.b_letter_choice, 
                            value="S", bg='black', fg='blue', selectcolor='black')
        self.bS.grid(row=11, column=2, pady=10, sticky='w')
        
        self.bO = Radiobutton(self.root, text='O', variable=self.b_letter_choice, 
                            value="O", bg='black', fg='blue', selectcolor='black')
        self.bO.grid(row=12, column=2, pady=10, sticky='w')
        
        #start button 
        self.start = Button(self.root, text="Start Game!", bg='black', fg='white', 
                          command=self.starting) 
        self.start.grid(row=14, column=1, pady=5)
        
    def show_replay_dialog(self):
        if self.replaying:
            messagebox.showinfo("Info", "A replay is already in progress")
            return
            
        games = self.recorder.get_all_games()
        if not games:
            messagebox.showinfo("Info", "No recorded games found")
            return
            
        dialog = Toplevel(self.root)
        dialog.title("Select Game to Replay")
        dialog.configure(bg='black')
        
        tree = ttk.Treeview(dialog, columns=('ID', 'Mode', 'Red', 'Blue', 'Size', 'Date'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Mode', text='Game Mode')
        tree.heading('Red', text='Red Player')
        tree.heading('Blue', text='Blue Player')
        tree.heading('Size', text='Grid Size')
        tree.heading('Date', text='Start Time')
        
        for game in games:
            tree.insert('', 'end', values=game)
            
        tree.pack(padx=10, pady=10)
        
        def on_select():
            selected_item = tree.focus()
            if not selected_item:
                return
                
            game_data = tree.item(selected_item)['values']
            self.replay_game_id = game_data[0]
            self.start_replay()
            dialog.destroy()
            
        select_button = Button(dialog, text="Replay Selected Game", command=on_select, bg='black', fg='white')
        select_button.pack(pady=10)
        
    def start_replay(self):
        # Get game details first
        game_details = self.recorder.get_game_details(self.replay_game_id)
        if not game_details:
            messagebox.showerror("Error", "Could not load game details")
            return
            
        game_mode, red_type, blue_type, grid_size = game_details
        
        # Reset game state with correct parameters
        self.sos_logic = GLogic()
        self.sos_logic.set_game_mode(game_mode)
        self.sos_logic.set_player_type('Red', red_type)
        self.sos_logic.set_player_type('Blue', blue_type)
        
        # Initialize grid
        num = self.sos_logic.g_verify(grid_size)
        if isinstance(num, str):
            messagebox.showerror("Error", f"Failed to initialize grid: {num}")
            return
        
        # Get moves
        self.replay_moves = self.recorder.get_game_moves(self.replay_game_id)
        if not self.replay_moves:
            messagebox.showinfo("Info", "No moves found for this game")
            return
            
        # Set up display
        self.display_board(num)
        self.replaying = True
        self.current_replay_move = 0
        
        # Set initial player letters (use defaults since we don't store these)
        self.sos_logic.players['Red'] = 'S'
        self.sos_logic.players['Blue'] = 'S'
        
        # Start replay
        self.play_next_replay_move()
        
    def play_next_replay_move(self):
        if not self.replaying or self.current_replay_move >= len(self.replay_moves):
            self.replaying = False
            messagebox.showinfo("Replay Complete", "Game replay has finished")
            return
            
        move = self.replay_moves[self.current_replay_move]
        move_num, player, row, col, letter = move
        
        # Ensure it's the correct player's turn
        if self.sos_logic.turn != player:
            self.sos_logic.turn = player
            self.update_turn()
        
        # Set player's letter choice
        self.sos_logic.players[player] = letter
        
        # Make the move
        result = self.sos_logic.letter_placement(row, col, letter)
        
        if result:
            self.update_board()
            self.update_scoreboard()
            self.highlight_sos()
            
            self.current_replay_move += 1
            self.root.after(1000, self.play_next_replay_move)  # 1 second delay between moves
        else:
            self.replaying = False
            messagebox.showerror("Replay Error", f"Failed to replay move {move_num} at ({row}, {col})")
    
    def starting(self): 
        g_size = self.gsize_input.get()
        print(f"Grid Size entered: {g_size}")
        
        # Reset game 
        self.sos_logic = GLogic() 
        self.computer_thinking = False
        self.replaying = False
        
        # set game mode
        game_mode = self.game_choice.get()
        self.sos_logic.set_game_mode(game_mode)
        
        # Set player types
        red_type = self.r_player_type.get()
        blue_type = self.b_player_type.get()
        self.sos_logic.set_player_type('Red', red_type)
        self.sos_logic.set_player_type('Blue', blue_type)
        
        num = self.sos_logic.g_verify(g_size)
        
        if isinstance(num, str): 
            messagebox.showerror("Error", num)
        else:
            print(f"Game starting with grid size: {num}")
            self.sos_logic.players['Red'] = self.r_letter_choice.get()
            self.sos_logic.players['Blue'] = self.b_letter_choice.get()
            self.root.title("SOS Game - Playing")
            
            # Start recording if checkbox is checked
            if self.record_game.get():
                self.recorder.start_recording(
                    game_mode,
                    red_type,
                    blue_type,
                    num
                )
            
            self.display_board(num)
            
            # Force immediate computer move if computer starts
            if self.sos_logic.get_player_type(self.sos_logic.turn) == "Computer":
                self.check_computer_turn()
    
if __name__ == "__main__":
    gui = SoS_GUI()
    gui.mainloop()