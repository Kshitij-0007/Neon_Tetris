"""
Menu system for Neon Tetris
Handles start menu, options, and other UI screens
"""
import pygame
import sys

class Button:
    def __init__(self, x, y, width, height, text, font, theme_manager, action=None):
        """Initialize a button"""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.theme_manager = theme_manager
        self.action = action
        self.hovered = False
    
    def draw(self, screen):
        """Draw the button"""
        theme = self.theme_manager.current_theme
        
        # Button colors based on hover state
        bg_color = theme['ui_background']
        if self.hovered:
            # Lighter color when hovered
            r, g, b = theme['ui_color']
            border_color = (min(255, r + 50), min(255, g + 50), min(255, b + 50))
            
            r, g, b = theme['text_color']
            text_color = (min(255, r + 50), min(255, g + 50), min(255, b + 50))
        else:
            border_color = theme['ui_color']
            text_color = theme['text_color']
        
        # Draw button background
        pygame.draw.rect(screen, bg_color, self.rect)
        
        # Draw button border
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Draw button text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """Handle mouse events on the button"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:  # Left mouse button
                if self.action:
                    self.theme_manager.play_sound('select')
                    return self.action
        return None

class Menu:
    def __init__(self, screen, theme_manager):
        """Initialize the menu system"""
        self.screen = screen
        self.theme_manager = theme_manager
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Font initialization
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 72)
        self.button_font = pygame.font.SysFont('Arial', 36)
        self.info_font = pygame.font.SysFont('Arial', 24)
        
        # Create buttons for main menu
        button_width = 300
        button_height = 60
        button_spacing = 20
        start_y = self.height // 2 - 50
        
        self.main_menu_buttons = [
            Button(
                self.width // 2 - button_width // 2,
                start_y,
                button_width,
                button_height,
                "Play Game",
                self.button_font,
                self.theme_manager,
                "play"
            ),
            Button(
                self.width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height,
                "Options",
                self.button_font,
                self.theme_manager,
                "options"
            ),
            Button(
                self.width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width,
                button_height,
                "Controls",
                self.button_font,
                self.theme_manager,
                "controls"
            ),
            Button(
                self.width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width,
                button_height,
                "Quit",
                self.button_font,
                self.theme_manager,
                "quit"
            )
        ]
        
        # Create buttons for options menu
        self.options_menu_buttons = [
            Button(
                self.width // 2 - button_width // 2,
                start_y,
                button_width,
                button_height,
                "Sound: ON",
                self.button_font,
                self.theme_manager,
                "toggle_sound"
            ),
            Button(
                self.width // 2 - button_width // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height,
                "Music: ON",
                self.button_font,
                self.theme_manager,
                "toggle_music"
            ),
            Button(
                self.width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width,
                button_height,
                "Theme: Neon",
                self.button_font,
                self.theme_manager,
                "cycle_theme"
            ),
            Button(
                self.width // 2 - button_width // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width,
                button_height,
                "Back",
                self.button_font,
                self.theme_manager,
                "back"
            )
        ]
        
        # Create back button for controls screen
        self.controls_menu_buttons = [
            Button(
                self.width // 2 - button_width // 2,
                self.height - 100,
                button_width,
                button_height,
                "Back",
                self.button_font,
                self.theme_manager,
                "back"
            )
        ]
        
        # Menu state
        self.current_menu = "main"  # "main", "options", "controls"
        self.sound_enabled = True
        self.music_enabled = True
    
    def update_button_text(self):
        """Update button text based on current settings"""
        # Update sound button text
        sound_text = "Sound: ON" if self.sound_enabled else "Sound: OFF"
        self.options_menu_buttons[0].text = sound_text
        
        # Update music button text
        music_text = "Music: ON" if self.music_enabled else "Music: OFF"
        self.options_menu_buttons[1].text = music_text
        
        # Update theme button text
        theme_text = f"Theme: {self.theme_manager.current_theme_name}"
        self.options_menu_buttons[2].text = theme_text
    
    def draw_main_menu(self):
        """Draw the main menu"""
        theme = self.theme_manager.current_theme
        
        # Draw background
        self.screen.fill(theme['background_color'])
        
        # Draw title
        title_text = self.title_font.render("NEON TETRIS", True, theme['text_color'])
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.main_menu_buttons:
            button.draw(self.screen)
        
        # Draw version info
        version_text = self.info_font.render("v1.0", True, theme['text_color'])
        self.screen.blit(version_text, (self.width - 60, self.height - 30))
    
    def draw_options_menu(self):
        """Draw the options menu"""
        theme = self.theme_manager.current_theme
        
        # Draw background
        self.screen.fill(theme['background_color'])
        
        # Draw title
        title_text = self.title_font.render("OPTIONS", True, theme['text_color'])
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Update button text based on current settings
        self.update_button_text()
        
        # Draw buttons
        for button in self.options_menu_buttons:
            button.draw(self.screen)
    
    def draw_controls_menu(self):
        """Draw the controls menu"""
        theme = self.theme_manager.current_theme
        
        # Draw background
        self.screen.fill(theme['background_color'])
        
        # Draw title
        title_text = self.title_font.render("CONTROLS", True, theme['text_color'])
        title_rect = title_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw controls information
        controls = [
            "Arrow Left/Right: Move piece",
            "Arrow Up: Rotate piece",
            "Arrow Down: Soft drop",
            "Space: Hard drop",
            "A: Toggle AI helper",
            "G: Toggle ghost piece",
            "T: Change theme",
            "P: Pause game",
            "R: Restart game (when game over)",
            "Q: Quit game (when game over)"
        ]
        
        start_y = 200
        for i, control in enumerate(controls):
            control_text = self.info_font.render(control, True, theme['text_color'])
            control_rect = control_text.get_rect(center=(self.width // 2, start_y + i * 40))
            self.screen.blit(control_text, control_rect)
        
        # Draw back button
        for button in self.controls_menu_buttons:
            button.draw(self.screen)
    
    def draw(self):
        """Draw the current menu"""
        if self.current_menu == "main":
            self.draw_main_menu()
        elif self.current_menu == "options":
            self.draw_options_menu()
        elif self.current_menu == "controls":
            self.draw_controls_menu()
    
    def handle_events(self):
        """Handle menu events"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        if self.current_menu == "main":
            buttons = self.main_menu_buttons
        elif self.current_menu == "options":
            buttons = self.options_menu_buttons
        elif self.current_menu == "controls":
            buttons = self.controls_menu_buttons
        
        for button in buttons:
            button.update(mouse_pos)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_menu == "main":
                        return "quit"
                    else:
                        self.current_menu = "main"
            
            # Handle button clicks
            for button in buttons:
                action = button.handle_event(event)
                if action:
                    if action == "play":
                        return "play"
                    elif action == "options":
                        self.current_menu = "options"
                    elif action == "controls":
                        self.current_menu = "controls"
                    elif action == "back":
                        self.current_menu = "main"
                    elif action == "quit":
                        return "quit"
                    elif action == "toggle_sound":
                        self.sound_enabled = not self.sound_enabled
                        # Update sound settings in theme manager
                        # (This would need to be implemented in ThemeManager)
                    elif action == "toggle_music":
                        self.music_enabled = not self.music_enabled
                        self.theme_manager.toggle_music()
                    elif action == "cycle_theme":
                        self.theme_manager.cycle_theme()
                        self.theme_manager.load_music()
        
        return None  # No action to exit the menu
    
    def run(self):
        """Run the menu loop"""
        clock = pygame.time.Clock()
        
        while True:
            action = self.handle_events()
            if action in ["play", "quit"]:
                return action
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
