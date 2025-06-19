"""
Theme Manager for Neon Tetris
Handles different visual themes and audio settings
"""
import pygame
import os

class ThemeManager:
    def __init__(self):
        """Initialize the Theme Manager"""
        # Define available themes
        self.themes = {
            'Neon': {
                'background_color': (0, 0, 30),
                'grid_color': (20, 20, 60),
                'border_color': (0, 200, 255),
                'text_color': (0, 255, 255),
                'piece_colors': {
                    'I': (0, 255, 255),   # Cyan
                    'J': (50, 150, 255),  # Blue
                    'L': (255, 165, 0),   # Orange
                    'O': (255, 255, 0),   # Yellow
                    'S': (50, 255, 50),   # Green
                    'T': (200, 50, 255),  # Purple
                    'Z': (255, 50, 50)    # Red
                },
                'ghost_alpha': 128,       # Transparency for ghost pieces
                'ui_color': (0, 200, 255),
                'ui_background': (0, 0, 60)
            },
            'Dark': {
                'background_color': (20, 20, 20),
                'grid_color': (40, 40, 40),
                'border_color': (100, 100, 100),
                'text_color': (200, 200, 200),
                'piece_colors': {
                    'I': (0, 180, 180),   # Dark Cyan
                    'J': (0, 0, 180),     # Dark Blue
                    'L': (180, 100, 0),   # Dark Orange
                    'O': (180, 180, 0),   # Dark Yellow
                    'S': (0, 180, 0),     # Dark Green
                    'T': (100, 0, 100),   # Dark Purple
                    'Z': (180, 0, 0)      # Dark Red
                },
                'ghost_alpha': 80,        # Transparency for ghost pieces
                'ui_color': (150, 150, 150),
                'ui_background': (30, 30, 30)
            },
            'Retro': {
                'background_color': (0, 0, 0),
                'grid_color': (30, 30, 30),
                'border_color': (255, 255, 255),
                'text_color': (255, 255, 255),
                'piece_colors': {
                    'I': (170, 170, 170),  # Light Gray
                    'J': (100, 100, 255),  # Blue
                    'L': (255, 100, 100),  # Red
                    'O': (255, 255, 100),  # Yellow
                    'S': (100, 255, 100),  # Green
                    'T': (255, 100, 255),  # Magenta
                    'Z': (255, 170, 100)   # Orange
                },
                'ghost_alpha': 100,        # Transparency for ghost pieces
                'ui_color': (255, 255, 255),
                'ui_background': (0, 0, 0)
            }
        }
        
        # Set default theme
        self.current_theme_name = 'Neon'
        self.current_theme = self.themes[self.current_theme_name]
        
        # Load sounds
        self.sounds = {}
        self._load_sounds()
        
        # Audio state
        self.sound_enabled = True
        self.music_enabled = True
        self.current_music = None
    
    def _load_sounds(self):
        """Load sound effects"""
        sound_dir = os.path.join('assets', 'sounds')
        
        # Check if directory exists
        if not os.path.exists(sound_dir):
            os.makedirs(sound_dir, exist_ok=True)
        
        # Define sound files to load
        sound_files = {
            'rotate': 'rotate.wav',
            'move': 'move.wav',
            'drop': 'drop.wav',
            'clear': 'clear.wav',
            'game_over': 'game_over.wav',
            'select': 'select.wav'  # Added for menu selection
        }
        
        # Load available sounds
        for name, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except:
                    print(f"Could not load sound: {path}")
    
    def cycle_theme(self):
        """Switch to the next available theme"""
        theme_names = list(self.themes.keys())
        current_index = theme_names.index(self.current_theme_name)
        next_index = (current_index + 1) % len(theme_names)
        self.current_theme_name = theme_names[next_index]
        self.current_theme = self.themes[self.current_theme_name]
        return self.current_theme_name
    
    def set_theme(self, theme_name):
        """Set a specific theme by name"""
        if theme_name in self.themes:
            self.current_theme_name = theme_name
            self.current_theme = self.themes[theme_name]
            return True
        return False
    
    def play_sound(self, sound_name):
        """Play a sound effect if available and enabled"""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled and self.current_music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        
        return self.music_enabled
    
    def load_music(self, theme=None):
        """Load music for the current or specified theme"""
        if theme is None:
            theme = self.current_theme_name
            
        music_file = os.path.join('assets', 'sounds', f"{theme.lower()}_music.mp3")
        
        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                self.current_music = music_file
                if self.music_enabled:
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                return True
            except:
                print(f"Could not load music: {music_file}")
        
        return False
    
    def get_ghost_color(self, original_color):
        """Create a semi-transparent version of a color for ghost pieces"""
        r, g, b = original_color
        return (r, g, b, self.current_theme['ghost_alpha'])
