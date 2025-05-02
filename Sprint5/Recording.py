import sqlite3
from datetime import datetime

class GameRecorder:
    def __init__(self):
        #connecting to SQLite 
        self.conn = sqlite3.connect('SOS_Games.db')
        self.create_table()
        self.current_game_id = None
        self.recording = False
        self.move_log_file = "Game_Moves.txt"

    def _write_move_to_text_file(self, move_number, player, row, col, letter):
        with open(self.move_log_file, 'a') as f:
            f.write(f"{move_number}. {player}: {letter} at ({row},{col})\n")

    def _write_game_header(self, game_mode, red_type, blue_type, grid_size):
        """Write the game header info to text file"""
        with open(self.move_log_file, 'w') as f:
            f.write(f"New Game Started\nMode: {game_mode}\n")
            f.write(f"Red: {red_type}, Blue: {blue_type}\n")
            f.write(f"Grid Size: {grid_size}x{grid_size}\n\n")
            f.write("Move Log:\n")

    def _write_game_footer(self, winner, red_score, blue_score):
        """Write the game results to text file"""
        with open(self.move_log_file, 'a') as f:
            f.write("\nGame Over\n")
            if winner:
                f.write(f"Winner: {winner}\n")
            else:
                f.write("Game was a tie\n")
            f.write(f"Final Score - Red: {red_score}, Blue: {blue_score}\n")
    
    def create_table(self):
        cursor = self.conn.cursor()
        #create a game table that will store the game info
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_mode TEXT,
                red_player_type TEXT,
                blue_player_type TEXT,
                grid_size INTEGER,
                start_time TEXT,
                end_time TEXT,
                winner TEXT,
                red_score INTEGER DEFAULT 0,
                blue_score INTEGER DEFAULT 0
            )
        ''')
        #create a moves tabel to track the player moves
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moves (
                move_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                move_number INTEGER,
                player TEXT,
                row INTEGER,
                col INTEGER,
                letter TEXT,
                FOREIGN KEY (game_id) REFERENCES games (game_id)
            )
        ''')
        self.conn.commit()
        

    
    def start_recording(self, game_mode, red_type, blue_type, grid_size):
        if self.recording:
            return
            
        self.recording = True
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO games (game_mode, red_player_type, blue_player_type, grid_size, start_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (game_mode, red_type, blue_type, grid_size, datetime.now().isoformat()))
        self.current_game_id = cursor.lastrowid
        self.conn.commit()
        self._write_game_header(game_mode, red_type, blue_type, grid_size)

    def record_move(self, player, row, col, letter):
        if not self.recording or self.current_game_id is None:
            return
            
        cursor = self.conn.cursor()
        # Get current move number
        cursor.execute('''
            SELECT COUNT(*) FROM moves WHERE game_id = ?
        ''', (self.current_game_id,))
        move_number = cursor.fetchone()[0] + 1
        
        cursor.execute('''
            INSERT INTO moves (game_id, move_number, player, row, col, letter)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.current_game_id, move_number, player, row, col, letter))
        self.conn.commit()
        self._write_move_to_text_file(move_number, player, row, col, letter)

    def end_recording(self, winner=None, red_score=0, blue_score=0):
        if not self.recording or self.current_game_id is None:
            return
            
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE games 
            SET end_time = ?, winner = ?, red_score = ?, blue_score = ?
            WHERE game_id = ?
        ''', (datetime.now().isoformat(), winner, red_score, blue_score, self.current_game_id))
        self.conn.commit()
        self.recording = False
        self.current_game_id = None
        self._write_game_footer(winner, red_score, blue_score)

    def get_all_games(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT game_id, game_mode, red_player_type, blue_player_type, grid_size, start_time 
            FROM games 
            ORDER BY start_time DESC
        ''')
        return cursor.fetchall()
    def get_game_details(self, game_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT game_mode, red_player_type, blue_player_type, grid_size 
            FROM games 
            WHERE game_id = ?
        ''', (game_id,))
        return cursor.fetchone()

    def get_game_moves(self, game_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT move_number, player, row, col, letter 
            FROM moves 
            WHERE game_id = ? 
            ORDER BY move_number
        ''', (game_id,))
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()