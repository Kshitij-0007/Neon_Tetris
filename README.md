# 🎮 Neon Tetris

A modern Tetris implementation with AI assistance, dynamic difficulty, theme switching, and other enhancements.

## ✨ Features

- **🧩 Core Tetris Gameplay**: Classic Tetris mechanics including block falling, line clearing, scoring, and increasing speed over time.
- **🤖 AI Helper Mode**: Recommends the best placement and rotation for the current falling piece based on heuristics.
- **👻 Ghost Piece**: Shows where the current piece would land if dropped instantly.
- **📈 Dynamic Difficulty Scaling**: Automatically adjusts game speed based on player performance.
- **🎨 Theme Switching**: Multiple visual themes (Neon, Dark, Retro) with different colors and styles.
- **📊 Performance Tracking**: Monitors player performance to adjust difficulty.

## 🎛️ Controls

- **⬅️⬆️➡️⬇️ Arrow Keys**: Move and rotate pieces
- **🔳 Space**: Hard drop
- **🅰️ A**: Toggle AI helper
- **🔤 T**: Change theme
- **🔍 G**: Toggle ghost piece
- **⏸️ P**: Pause game
- **🔄 R**: Restart game (when game over)
- **❌ Q**: Quit game (when game over)

## 🔧 Requirements

- 🐍 Python 3.6+
- 🎯 Pygame 2.5.2+

## 📥 Installation

1. 📋 Clone the repository
2. 📦 Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. 🚀 Run the game:
   ```
   python main.py
   ```

## 📁 Project Structure

- `main.py`: Main entry point
- `src/`: Source code directory
  - `game.py`: Main game logic
  - `board.py`: Game board representation
  - `tetromino.py`: Tetris piece logic
  - `ai_helper.py`: AI recommendation system
  - `theme_manager.py`: Theme and audio management
  - `performance_tracker.py`: Player performance monitoring
  - `renderer.py`: Game rendering
- `assets/`: Game assets
  - `sounds/`: Sound effects and music
  - `images/`: Images and textures

## 🧠 AI Helper Logic

The AI helper uses several heuristics to evaluate potential moves:

1. **📏 Aggregate Height**: Sum of the heights of each column
2. **✅ Complete Lines**: Number of complete lines
3. **🕳️ Holes**: Empty cells with filled cells above them
4. **📊 Bumpiness**: Sum of differences between adjacent columns

These factors are weighted and combined to score each possible move, with the highest scoring move being recommended to the player.

## 🎚️ Dynamic Difficulty

The game monitors player performance metrics:

- 🏆 Score per minute
- 🧹 Lines cleared per minute
- 🎯 How closely the player follows AI recommendations

Based on these metrics, the game adjusts the drop speed to provide an appropriate challenge level for the player's skill.
