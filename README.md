# SOS Game
A classic SOS game implementation with multiple game modes and features developed using Python, Tkinter, SQLite, and unittest.

## Features

- **Multiple Game Modes**:
  - Human vs Computer
  - Human vs Human
  - Computer vs Computer

- **Game Types**:
  - Simple Game Mode
  - General Game Mode
    
- **Customizable Game Board**: Play on different board sizes (3x3, 5x5, 7x7, etc.)

- **Game Recording & Replay**: All games are recorded for later analysis and replay
  
- **Database Integration**:
  - Games are recorded and stored using `SQLite`
  - Replay feature for previously saved games

- **Automated Testing**: Comprehensive unit tests using Python's unittest framework

- **User-Friendly GUI**:
  - Built with Tkinter for an intuitive playing experience
  - Player configuration with radio buttons, text inputs, and real-time interaction


## Technologies Used

- **Python**: Core programming language
- **Tkinter**: For creating the graphical user interface (GUI)
- **SQLite**: For database management to store and replay games (Persistent storage) 
- **unittest**: For automated testing to ensure code reliability (Testing)
  

## How to Run

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/A-Mohammed19/SOS_Game.git

# Change directory
cd SOS_Game

# Run the game
python GUI.py
```

## Game Rules & How to Play

1. **Setup**: Select your preferred player mode (Human vs Computer, Human vs Human, or Computer vs Computer), board size, and game type (Simple or General)

2. **Gameplay**:
   - Players take turns placing either an 'S' or an 'O' on the board
   - When a player completes the sequence 'SOS' (horizontally, vertically, or diagonally), they earn a point
   - After completing an SOS, the player gets another turn

3. **Winning Conditions**:
   - **Simple Game Mode**: The first player to create an SOS pattern wins immediately
   - **General Game Mode**: Play continues until the board is filled, and the player with the most SOS patterns wins

## Testing

Run the automated tests with:

```bash
python -m unittest discover tests
```

## License

[MIT](LICENSE)

## Author

- A. Mohammed
