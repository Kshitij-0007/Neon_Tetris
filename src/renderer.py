"""
Renderer module for Neon Tetris
Handles all drawing operations
"""
import pygame

class Renderer:
    def __init__(self, screen, theme_manager):
        """Initialize the renderer"""
        self.screen = screen
        self.theme_manager = theme_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Font initialization
        pygame.font.init()
        self.update_fonts()
        
        # Board dimensions and position
        self.update_layout()
    
    def update_screen_size(self, screen):
        """Update renderer for new screen size"""
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.update_layout()
        self.update_fonts()
    
    def update_layout(self):
        """Update layout based on screen size"""
        # Calculate cell size based on screen height
        # We want the board to take up about 2/3 of the screen height
        board_height_pixels = self.height * 0.8
        self.cell_size = int(board_height_pixels / 20)  # 20 is the standard board height
        
        # Center the board horizontally
        self.board_x = max(50, (self.width - (10 * self.cell_size)) // 2 - 100)
        self.board_y = max(20, (self.height - (20 * self.cell_size)) // 2)
    
    def update_fonts(self):
        """Update font sizes based on screen size"""
        base_size = max(10, min(36, self.height // 20))
        self.font_lg = pygame.font.SysFont('Arial', base_size * 2)
        self.font_md = pygame.font.SysFont('Arial', base_size)
        self.font_sm = pygame.font.SysFont('Arial', int(base_size * 0.75))
    
    def draw_background(self):
        """Draw the game background"""
        theme = self.theme_manager.current_theme
        self.screen.fill(theme['background_color'])
    
    
    def draw_board(self, board):
        """Draw the game board"""
        theme = self.theme_manager.current_theme
        
        # Draw the grid
        for y in range(board.height):
            for x in range(board.width):
                # Calculate position on screen
                pos_x = x * self.cell_size + self.board_x
                pos_y = y * self.cell_size + self.board_y
                
                # Draw the cell
                if board.grid[y][x]:
                    color = board.colors[y][x]
                    pygame.draw.rect(self.screen, color, (pos_x, pos_y, self.cell_size-1, self.cell_size-1))
                    pygame.draw.rect(self.screen, theme['border_color'], (pos_x, pos_y, self.cell_size-1, self.cell_size-1), 1)
                else:
                    # Draw empty cell
                    pygame.draw.rect(self.screen, theme['grid_color'], (pos_x, pos_y, self.cell_size-1, self.cell_size-1), 1)
        
        # Draw board outline
        board_rect = pygame.Rect(
            self.board_x, 
            self.board_y, 
            board.width * self.cell_size, 
            board.height * self.cell_size
        )
        pygame.draw.rect(self.screen, theme['border_color'], board_rect, 2)
    
    def draw_piece(self, piece):
        """Draw a tetromino piece"""
        theme = self.theme_manager.current_theme
        shape = piece.get_current_rotation()
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate position on screen
                    pos_x = (piece.x + x) * self.cell_size + self.board_x
                    pos_y = (piece.y + y) * self.cell_size + self.board_y
                    
                    # Draw the block
                    pygame.draw.rect(self.screen, piece.color, (pos_x, pos_y, self.cell_size-1, self.cell_size-1))
                    pygame.draw.rect(self.screen, theme['border_color'], (pos_x, pos_y, self.cell_size-1, self.cell_size-1), 1)
    
    def draw_ghost_piece(self, ghost_piece):
        """Draw a ghost piece (semi-transparent)"""
        theme = self.theme_manager.current_theme
        shape = ghost_piece.get_current_rotation()
        
        # Create a surface for the ghost piece with alpha
        ghost_surface = pygame.Surface((self.cell_size-1, self.cell_size-1), pygame.SRCALPHA)
        r, g, b = ghost_piece.color
        ghost_color = (r, g, b, theme['ghost_alpha'])
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate position on screen
                    pos_x = (ghost_piece.x + x) * self.cell_size + self.board_x
                    pos_y = (ghost_piece.y + y) * self.cell_size + self.board_y
                    
                    # Draw the ghost block
                    ghost_surface.fill(ghost_color)
                    self.screen.blit(ghost_surface, (pos_x, pos_y))
                    pygame.draw.rect(self.screen, theme['border_color'], (pos_x, pos_y, self.cell_size-1, self.cell_size-1), 1)
    
    def draw_ai_suggestion(self, suggested_piece):
        """Draw the AI's suggested piece position"""
        theme = self.theme_manager.current_theme
        shape = suggested_piece.get_current_rotation()
        
        # Create a surface for the suggested piece with highlight
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate position on screen
                    pos_x = (suggested_piece.x + x) * self.cell_size + self.board_x
                    pos_y = (suggested_piece.y + y) * self.cell_size + self.board_y
                    
                    # Draw a highlighted border around the suggested position
                    pygame.draw.rect(self.screen, (255, 255, 255), 
                                    (pos_x, pos_y, self.cell_size-1, self.cell_size-1), 2)
    
    def draw_next_piece(self, next_piece):
        """Draw the next piece preview"""
        theme = self.theme_manager.current_theme
        shape = next_piece.shape[0]  # Always use first rotation for preview
        
        # Calculate the size of the piece
        piece_height = len(shape)
        piece_width = len(shape[0])
        
        # Calculate the position for the next piece preview
        # Use a fixed width of 10 for the board width
        preview_x = self.board_x + (10 * self.cell_size) + 20
        preview_y = self.board_y + 2 * self.cell_size
        
        # Draw the preview box
        preview_width = max(6, piece_width + 2) * self.cell_size // 2
        preview_height = max(6, piece_height + 2) * self.cell_size // 2
        
        # Draw preview box background
        pygame.draw.rect(self.screen, theme['ui_background'], 
                        (preview_x, preview_y, preview_width, preview_height))
        
        # Draw preview box border
        pygame.draw.rect(self.screen, theme['ui_color'], 
                        (preview_x, preview_y, preview_width, preview_height), 2)
        
        # Draw "Next Piece" text
        next_text = self.font_md.render("Next Piece", True, theme['text_color'])
        self.screen.blit(next_text, (preview_x + 10, preview_y - 30))
        
        # Calculate center position for the piece
        center_x = preview_x + preview_width // 2 - (piece_width * self.cell_size // 2) // 2
        center_y = preview_y + preview_height // 2 - (piece_height * self.cell_size // 2) // 2
        
        # Draw the next piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pos_x = center_x + x * self.cell_size // 2
                    pos_y = center_y + y * self.cell_size // 2
                    
                    pygame.draw.rect(self.screen, next_piece.color, 
                                    (pos_x, pos_y, self.cell_size//2-1, self.cell_size//2-1))
                    pygame.draw.rect(self.screen, theme['border_color'], 
                                    (pos_x, pos_y, self.cell_size//2-1, self.cell_size//2-1), 1)
    
    def draw_score_and_level(self, score, level, lines_cleared):
        """Draw the score, level, and lines cleared"""
        theme = self.theme_manager.current_theme
        
        # Position for the score display
        # Use a fixed width of 10 for the board width
        score_x = self.board_x + (10 * self.cell_size) + 20
        score_y = self.board_y + 12 * self.cell_size // 2
        
        # Draw score box background
        score_width = max(200, self.width // 5)
        score_height = 150
        pygame.draw.rect(self.screen, theme['ui_background'], 
                        (score_x, score_y, score_width, score_height))
        
        # Draw score box border
        pygame.draw.rect(self.screen, theme['ui_color'], 
                        (score_x, score_y, score_width, score_height), 2)
        
        # Draw score text
        score_label = self.font_md.render("Score:", True, theme['text_color'])
        score_value = self.font_lg.render(str(score), True, theme['text_color'])
        
        # Draw level text
        level_label = self.font_md.render("Level:", True, theme['text_color'])
        level_value = self.font_lg.render(str(level), True, theme['text_color'])
        
        # Draw lines cleared text
        lines_label = self.font_md.render("Lines:", True, theme['text_color'])
        lines_value = self.font_lg.render(str(lines_cleared), True, theme['text_color'])
        
        # Position and draw the text
        padding = 10
        self.screen.blit(score_label, (score_x + padding, score_y + padding))
        self.screen.blit(score_value, (score_x + padding + 100, score_y + padding))
        
        self.screen.blit(level_label, (score_x + padding, score_y + padding + 50))
        self.screen.blit(level_value, (score_x + padding + 100, score_y + padding + 50))
        
        self.screen.blit(lines_label, (score_x + padding, score_y + padding + 100))
        self.screen.blit(lines_value, (score_x + padding + 100, score_y + padding + 100))
    
    def draw_game_over(self, final_score):
        """Draw the game over screen"""
        theme = self.theme_manager.current_theme
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.font_lg.render("GAME OVER", True, theme['text_color'])
        score_text = self.font_md.render(f"Final Score: {final_score}", True, theme['text_color'])
        restart_text = self.font_md.render("Press R to Restart", True, theme['text_color'])
        quit_text = self.font_md.render("Press Q to Quit", True, theme['text_color'])
        menu_text = self.font_md.render("Press ESC for Menu", True, theme['text_color'])
        
        # Center the text
        game_over_x = self.width // 2 - game_over_text.get_width() // 2
        score_x = self.width // 2 - score_text.get_width() // 2
        restart_x = self.width // 2 - restart_text.get_width() // 2
        quit_x = self.width // 2 - quit_text.get_width() // 2
        menu_x = self.width // 2 - menu_text.get_width() // 2
        
        # Draw the text
        self.screen.blit(game_over_text, (game_over_x, self.height // 2 - 80))
        self.screen.blit(score_text, (score_x, self.height // 2 - 20))
        self.screen.blit(restart_text, (restart_x, self.height // 2 + 40))
        self.screen.blit(quit_text, (quit_x, self.height // 2 + 80))
        self.screen.blit(menu_text, (menu_x, self.height // 2 + 120))
    
    def draw_current_theme(self):
        """Draw the current theme name"""
        theme = self.theme_manager.current_theme
        theme_text = self.font_sm.render(f"Theme: {self.theme_manager.current_theme_name}", True, theme['text_color'])
        self.screen.blit(theme_text, (10, self.height - 30))
    
    def draw_ai_helper_status(self, ai_enabled):
        """Draw the AI helper status"""
        theme = self.theme_manager.current_theme
        status = "ON" if ai_enabled else "OFF"
        ai_text = self.font_sm.render(f"AI Helper: {status}", True, theme['text_color'])
        self.screen.blit(ai_text, (10, self.height - 60))
    
    def draw_controls_help(self):
        """Draw the controls help text"""
        theme = self.theme_manager.current_theme
        
        # Position for the controls display
        controls_x = 10
        controls_y = 10
        
        # Draw controls text
        controls = [
            "Controls:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "Space : Hard Drop",
            "A : Toggle AI Helper",
            "T : Change Theme",
            "G : Toggle Ghost Piece",
            "F : Toggle Fullscreen",
            "P : Pause Game",
            "ESC : Menu"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.font_sm.render(text, True, theme['text_color'])
            self.screen.blit(control_text, (controls_x, controls_y + i * 20))
    
    def draw_pause_screen(self):
        """Draw the pause screen overlay"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        theme = self.theme_manager.current_theme
        pause_text = self.font_lg.render("PAUSED", True, theme['text_color'])
        continue_text = self.font_md.render("Press P to Continue", True, theme['text_color'])
        menu_text = self.font_md.render("Press ESC for Menu", True, theme['text_color'])
        
        # Center the text
        pause_x = self.width // 2 - pause_text.get_width() // 2
        continue_x = self.width // 2 - continue_text.get_width() // 2
        menu_x = self.width // 2 - menu_text.get_width() // 2
        
        # Draw the text
        self.screen.blit(pause_text, (pause_x, self.height // 2 - 50))
        self.screen.blit(continue_text, (continue_x, self.height // 2))
        self.screen.blit(menu_text, (menu_x, self.height // 2 + 50))
