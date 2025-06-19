"""
Tetromino class - Represents a tetris piece
"""
import pygame
import random

class Tetromino:
    # Tetromino shapes and their rotations
    SHAPES = {
        'I': [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            
            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]],
            
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0]],
            
            [[0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
        ],
        'J': [
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 1],
             [0, 1, 0],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [0, 0, 1]],
            
            [[0, 1, 0],
             [0, 1, 0],
             [1, 1, 0]]
        ],
        'L': [
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 0],
             [0, 1, 1]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [1, 0, 0]],
            
            [[1, 1, 0],
             [0, 1, 0],
             [0, 1, 0]]
        ],
        'O': [
            [[0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]]
        ],
        'S': [
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 1],
             [0, 0, 1]],
            
            [[0, 0, 0],
             [0, 1, 1],
             [1, 1, 0]],
            
            [[1, 0, 0],
             [1, 1, 0],
             [0, 1, 0]]
        ],
        'T': [
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 0],
             [0, 1, 1],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 1],
             [0, 1, 0]],
            
            [[0, 1, 0],
             [1, 1, 0],
             [0, 1, 0]]
        ],
        'Z': [
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
            
            [[0, 0, 1],
             [0, 1, 1],
             [0, 1, 0]],
            
            [[0, 0, 0],
             [1, 1, 0],
             [0, 1, 1]],
            
            [[0, 1, 0],
             [1, 1, 0],
             [1, 0, 0]]
        ]
    }
    
    # Default colors for each shape
    DEFAULT_COLORS = {
        'I': (0, 255, 255),   # Cyan
        'J': (0, 0, 255),     # Blue
        'L': (255, 165, 0),   # Orange
        'O': (255, 255, 0),   # Yellow
        'S': (0, 255, 0),     # Green
        'T': (128, 0, 128),   # Purple
        'Z': (255, 0, 0)      # Red
    }
    
    def __init__(self):
        """Initialize a new tetromino piece"""
        # Randomly select a shape
        self.shape_name = random.choice(list(self.SHAPES.keys()))
        self.shape = self.SHAPES[self.shape_name]
        self.color = self.DEFAULT_COLORS[self.shape_name]
        self.rotation = 0
        
        # Starting position (centered at top)
        self.x = 3
        self.y = 0
    
    def update_colors(self, theme_colors):
        """Update the piece color based on the current theme"""
        if self.shape_name in theme_colors:
            self.color = theme_colors[self.shape_name]
    
    def get_current_rotation(self):
        """Get the current rotation of the shape"""
        return self.shape[self.rotation]
    
    def rotate(self, board):
        """Rotate the tetromino if possible"""
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(self.shape)
        
        # Check if rotation is valid
        if board.is_collision(self):
            # Try wall kicks - shift left or right if rotation against wall
            original_x = self.x
            
            # Try shifting right
            self.x += 1
            if not board.is_collision(self):
                return True
                
            # Try shifting left
            self.x = original_x - 1
            if not board.is_collision(self):
                return True
                
            # Try shifting two spaces right (for I piece)
            self.x = original_x + 2
            if not board.is_collision(self):
                return True
                
            # Try shifting two spaces left (for I piece)
            self.x = original_x - 2
            if not board.is_collision(self):
                return True
            
            # If all wall kicks fail, revert rotation and position
            self.x = original_x
            self.rotation = old_rotation
            return False
            
        return True
    
    def move_left(self, board):
        """Move the tetromino left if possible"""
        self.x -= 1
        if board.is_collision(self):
            self.x += 1
            return False
        return True
    
    def move_right(self, board):
        """Move the tetromino right if possible"""
        self.x += 1
        if board.is_collision(self):
            self.x -= 1
            return False
        return True
    
    def move_down(self, board):
        """Move the tetromino down if possible"""
        self.y += 1
        if board.is_collision(self):
            self.y -= 1
            return False
        return True
    
    def hard_drop(self, board):
        """Drop the tetromino to the bottom"""
        while self.move_down(board):
            pass
