"""
Board class - Represents the Tetris game board
"""
import pygame
import copy

class Board:
    def __init__(self, width=10, height=20):
        """Initialize the game board"""
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.colors = [[None for _ in range(width)] for _ in range(height)]
    
    def is_collision(self, tetromino):
        """
        Check if tetromino collides with the board or other pieces
        Returns True if collision detected, False otherwise
        """
        shape = tetromino.get_current_rotation()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate board coordinates
                    board_x = tetromino.x + x
                    board_y = tetromino.y + y
                    
                    # Check if out of bounds or colliding with placed pieces
                    if (board_x < 0 or board_x >= self.width or 
                        board_y >= self.height or 
                        (board_y >= 0 and self.grid[board_y][board_x])):
                        return True
        return False
    
    def place_piece(self, tetromino):
        """
        Place the tetromino on the board
        Updates the grid and colors arrays
        """
        shape = tetromino.get_current_rotation()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = tetromino.x + x
                    board_y = tetromino.y + y
                    
                    # Only place cells that are within the board
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        self.grid[board_y][board_x] = 1
                        self.colors[board_y][board_x] = tetromino.color
    
    def clear_lines(self):
        """
        Clear completed lines and return the number of lines cleared
        Moves all lines above the cleared line down
        """
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(self.grid[y]):
                # Line is complete, remove it
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1][:]
                    self.colors[y2] = self.colors[y2 - 1][:]
                
                # Clear the top line
                self.grid[0] = [0] * self.width
                self.colors[0] = [None] * self.width
                
                lines_cleared += 1
            else:
                y -= 1
        
        return lines_cleared
    
    def get_height_profile(self):
        """
        Get the height profile of the board
        Returns a list where each element is the height of a column
        """
        heights = [0] * self.width
        
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x]:
                    heights[x] = self.height - y
                    break
        
        return heights
    
    def count_holes(self):
        """
        Count the number of holes in the board
        A hole is an empty cell with at least one filled cell above it
        """
        holes = 0
        
        for x in range(self.width):
            found_block = False
            for y in range(self.height):
                if self.grid[y][x]:
                    found_block = True
                elif found_block:
                    # This is a hole - empty cell with a block above it
                    holes += 1
        
        return holes
    
    def get_aggregate_height(self):
        """
        Calculate the sum of all column heights
        """
        return sum(self.get_height_profile())
    
    def get_bumpiness(self):
        """
        Calculate the sum of differences between adjacent columns
        """
        heights = self.get_height_profile()
        return sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
    
    def clone(self):
        """
        Create a deep copy of the board
        Useful for AI simulations
        """
        new_board = Board(self.width, self.height)
        new_board.grid = copy.deepcopy(self.grid)
        new_board.colors = copy.deepcopy(self.colors)
        return new_board
