"""
Game class - Main game logic for Neon Tetris
"""
import pygame
import copy
import time
from src.tetromino import Tetromino
from src.board import Board
from src.ai_helper import AIHelper
from src.theme_manager import ThemeManager
from src.performance_tracker import PerformanceTracker
from src.renderer import Renderer

class Game:
    def __init__(self, screen_width=800, screen_height=600, fullscreen=False):
        """Initialize the game"""
        # Game window settings
        self.width = screen_width
        self.height = screen_height
        self.fullscreen = fullscreen
        
        # Set up display
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        pygame.display.set_caption("Neon Tetris")
        
        # Initialize components
        self.theme_manager = ThemeManager()
        self.ai_helper = AIHelper()
        self.performance_tracker = PerformanceTracker()
        self.renderer = Renderer(self.screen, self.theme_manager)
        
        # Game objects
        self.board = Board()
        self.current_piece = None
        self.next_piece = None
        
        # Game state
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        # Feature toggles
        self.ai_helper_enabled = False
        self.ghost_piece_enabled = True
        self.dynamic_difficulty_enabled = True
        
        # AI suggestion state
        self.ai_suggestion = None
        self.ai_ghost_piece = None
        
        # Game timing
        self.clock = pygame.time.Clock()
        self.drop_time = 0
        self.drop_speed = 1000  # milliseconds
        self.last_move_time = 0
        
        # Initialize game
        self._spawn_piece()
        
        # Load theme-specific resources
        self.theme_manager.load_music()
    
    def _spawn_piece(self):
        """Create a new tetromino piece"""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = Tetromino()
        
        # Create the next piece with theme-specific colors
        self.next_piece = Tetromino()
        self.next_piece.update_colors(self.theme_manager.current_theme['piece_colors'])
        
        # Update current piece colors to match theme
        self.current_piece.update_colors(self.theme_manager.current_theme['piece_colors'])
        
        # Reset AI suggestion
        self.ai_suggestion = None
        self.ai_ghost_piece = None
        
        # Calculate AI suggestion if enabled
        if self.ai_helper_enabled:
            self._calculate_ai_suggestion()
    
    def _calculate_ai_suggestion(self):
        """Calculate the AI's suggested move"""
        best_x, best_rotation, _, best_y = self.ai_helper.get_best_move(self.board, self.current_piece)
        
        # Create a ghost piece for the AI suggestion
        self.ai_suggestion = (best_x, best_rotation)
        
        # Create a ghost piece to show the suggestion
        self.ai_ghost_piece = copy.deepcopy(self.current_piece)
        self.ai_ghost_piece.x = best_x
        self.ai_ghost_piece.rotation = best_rotation
        self.ai_ghost_piece.y = best_y
    
    def _create_ghost_piece(self):
        """Create a ghost piece showing where the current piece would land"""
        if not self.ghost_piece_enabled:
            return None
            
        return self.ai_helper.get_ghost_piece(self.board, self.current_piece)
    
    def _handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle window resize
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.width, self.height = event.size
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    self.renderer.update_screen_size(self.screen)
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    # Game over state controls
                    if event.key == pygame.K_r:
                        self._reset_game()
                    elif event.key == pygame.K_q:
                        return False
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"  # Return to menu
                elif self.paused:
                    # Paused state controls
                    if event.key == pygame.K_p:
                        self.paused = False
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"  # Return to menu
                else:
                    # Active game controls
                    if event.key == pygame.K_LEFT:
                        self.current_piece.move_left(self.board)
                        self.theme_manager.play_sound('move')
                        self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.move_right(self.board)
                        self.theme_manager.play_sound('move')
                        self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_DOWN:
                        self.current_piece.move_down(self.board)
                        self.theme_manager.play_sound('move')
                        self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_UP:
                        if self.current_piece.rotate(self.board):
                            self.theme_manager.play_sound('rotate')
                            self.last_move_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_SPACE:
                        self.current_piece.hard_drop(self.board)
                        self.theme_manager.play_sound('drop')
                        self._place_current_piece()
                    elif event.key == pygame.K_p:
                        self.paused = True
                    elif event.key == pygame.K_a:
                        self.ai_helper_enabled = not self.ai_helper_enabled
                        if self.ai_helper_enabled:
                            self._calculate_ai_suggestion()
                    elif event.key == pygame.K_g:
                        self.ghost_piece_enabled = not self.ghost_piece_enabled
                    elif event.key == pygame.K_t:
                        new_theme = self.theme_manager.cycle_theme()
                        # Update piece colors for the new theme
                        self.current_piece.update_colors(self.theme_manager.current_theme['piece_colors'])
                        self.next_piece.update_colors(self.theme_manager.current_theme['piece_colors'])
                        # Load theme-specific music
                        self.theme_manager.load_music()
                    elif event.key == pygame.K_f:
                        # Toggle fullscreen
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = True
        
        return True
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            # Save current window size for when we exit fullscreen
            self.windowed_size = (self.width, self.height)
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            # Restore previous window size
            self.width, self.height = self.windowed_size if hasattr(self, 'windowed_size') else (800, 600)
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        # Update renderer with new screen size
        self.renderer.update_screen_size(self.screen)
    
    def _place_current_piece(self):
        """Place the current piece on the board and handle consequences"""
        # Record the final position for performance tracking
        if self.ai_helper_enabled and self.ai_suggestion:
            self.performance_tracker.record_move(
                self.current_piece.x, 
                self.current_piece.rotation,
                self.ai_suggestion[0],
                self.ai_suggestion[1]
            )
        
        # Place the piece on the board
        self.board.place_piece(self.current_piece)
        
        # Check for completed lines
        lines = self.board.clear_lines()
        if lines > 0:
            self.theme_manager.play_sound('clear')
            self.lines_cleared += lines
            self.score += lines * 100 * self.level
            self.level = 1 + self.lines_cleared // 10
            
            # Record score for performance tracking
            self.performance_tracker.record_score(self.score, self.lines_cleared)
            
            # Adjust difficulty based on performance if enabled
            if self.dynamic_difficulty_enabled:
                self.drop_speed = self.performance_tracker.adjust_difficulty()
            else:
                # Standard difficulty progression
                self.drop_speed = max(100, 1000 - (self.level * 50))
        
        # Spawn a new piece
        self._spawn_piece()
        
        # Check for game over
        if self.board.is_collision(self.current_piece):
            self.game_over = True
            self.theme_manager.play_sound('game_over')
    
    def _update(self):
        """Update game state"""
        if self.paused or self.game_over:
            return
            
        current_time = pygame.time.get_ticks()
        
        if current_time - self.drop_time > self.drop_speed:
            self.drop_time = current_time
            if not self.current_piece.move_down(self.board):
                # Piece has landed
                self._place_current_piece()
    
    def _draw(self):
        """Draw the game state to the screen"""
        # Clear screen and draw background
        self.renderer.draw_background()
        
        # Draw board
        self.renderer.draw_board(self.board)
        
        if not self.game_over:
            # Draw ghost piece if enabled
            if self.ghost_piece_enabled:
                ghost_piece = self._create_ghost_piece()
                if ghost_piece:
                    self.renderer.draw_ghost_piece(ghost_piece)
            
            # Draw AI suggestion if enabled
            if self.ai_helper_enabled and self.ai_ghost_piece:
                self.renderer.draw_ai_suggestion(self.ai_ghost_piece)
            
            # Draw current piece
            self.renderer.draw_piece(self.current_piece)
        
        # Draw next piece preview
        self.renderer.draw_next_piece(self.next_piece)
        
        # Draw score, level, and lines cleared
        self.renderer.draw_score_and_level(self.score, self.level, self.lines_cleared)
        
        # Draw current theme name
        self.renderer.draw_current_theme()
        
        # Draw AI helper status
        self.renderer.draw_ai_helper_status(self.ai_helper_enabled)
        
        # Draw controls help
        self.renderer.draw_controls_help()
        
        # Draw pause screen if paused
        if self.paused:
            self.renderer.draw_pause_screen()
        
        # Draw game over screen if game over
        if self.game_over:
            self.renderer.draw_game_over(self.score)
        
        # Update display
        pygame.display.flip()
    
    def _reset_game(self):
        """Reset the game to initial state"""
        # Reset game objects
        self.board = Board()
        self.current_piece = None
        self.next_piece = None
        
        # Reset game state
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        # Reset timing
        self.drop_time = 0
        self.drop_speed = 1000
        
        # Reset performance tracker
        self.performance_tracker.reset()
        
        # Initialize game
        self._spawn_piece()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            result = self._handle_events()
            if result == "menu":
                return "menu"
            elif result is False:
                running = False
            
            self._update()
            self._draw()
            self.clock.tick(60)
        
        return "quit"
