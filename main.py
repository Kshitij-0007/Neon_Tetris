#!/usr/bin/env python3
"""
Neon Tetris Game - Main Entry Point

A modern Tetris implementation with AI assistance, dynamic difficulty,
theme switching, and other enhancements.

Controls:
- Arrow keys: Move and rotate pieces
- Space: Hard drop
- A: Toggle AI helper
- T: Change theme
- G: Toggle ghost piece
- F: Toggle fullscreen
- P: Pause game
- ESC: Return to menu
- R: Restart game (when game over)
- Q: Quit game (when game over)
"""
import pygame
import sys
from src.game import Game
from src.menu import Menu
from src.theme_manager import ThemeManager

def main():
    """Main entry point for the game"""
    # Initialize pygame
    pygame.init()
    
    # Initialize mixer for sound effects
    pygame.mixer.init()
    
    # Default screen size
    screen_width = 800
    screen_height = 600
    fullscreen = False
    
    # Set up display
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    
    pygame.display.set_caption("Neon Tetris")
    
    # Create theme manager (shared between menu and game)
    theme_manager = ThemeManager()
    
    # Create menu
    menu = Menu(screen, theme_manager)
    
    # Main application loop
    running = True
    current_state = "menu"  # Start with the menu
    
    while running:
        if current_state == "menu":
            # Run the menu
            action = menu.run()
            
            if action == "play":
                # Start the game
                current_state = "game"
                game = Game(screen.get_width(), screen.get_height(), fullscreen)
            elif action == "quit":
                running = False
        
        elif current_state == "game":
            # Run the game
            result = game.run()
            
            if result == "menu":
                current_state = "menu"
            elif result == "quit":
                running = False
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
