"""
AI Helper module for Neon Tetris
Provides AI-based suggestions for optimal piece placement
"""
import copy
from src.board import Board
from src.tetromino import Tetromino

class AIHelper:
    def __init__(self):
        """Initialize the AI Helper"""
        # Weights for different heuristics
        self.weights = {
            'aggregate_height': -0.510066,
            'complete_lines': 0.760666,
            'holes': -0.35663,
            'bumpiness': -0.184483
        }
    
    def get_best_move(self, board, current_piece):
        """
        Find the best move for the current piece
        Returns: (best_x, best_rotation, best_score, landing_y)
        """
        best_score = float('-inf')
        best_x = 0
        best_rotation = 0
        best_landing_y = 0
        
        # Try all possible rotations and positions
        for rotation in range(len(current_piece.shape)):
            # Create a copy of the piece with this rotation
            test_piece = copy.deepcopy(current_piece)
            test_piece.rotation = rotation
            
            # Get width of the piece in this rotation
            piece_width = self._get_piece_width(test_piece)
            
            # Try all possible x positions
            for x in range(-2, board.width - piece_width + 3):  # Allow slight overhang for rotations
                # Create a copy of the piece at this position
                test_piece = copy.deepcopy(current_piece)
                test_piece.rotation = rotation
                test_piece.x = x
                test_piece.y = 0
                
                # Skip if invalid position
                if board.is_collision(test_piece):
                    continue
                
                # Simulate dropping the piece
                landing_y = self._simulate_drop(board, test_piece)
                
                # Create a copy of the board with the piece placed
                test_board = copy.deepcopy(board)
                test_piece.y = landing_y
                
                # Skip if invalid final position (shouldn't happen but just in case)
                if test_board.is_collision(test_piece):
                    continue
                
                # Place the piece on the test board
                test_board.place_piece(test_piece)
                
                # Calculate score for this move
                score = self._evaluate_board(test_board)
                
                # Update best move if this is better
                if score > best_score:
                    best_score = score
                    best_x = x
                    best_rotation = rotation
                    best_landing_y = landing_y
        
        return best_x, best_rotation, best_score, best_landing_y
    
    def _get_piece_width(self, piece):
        """Get the effective width of a piece in its current rotation"""
        shape = piece.get_current_rotation()
        width = len(shape[0])
        
        # Trim empty columns from left and right
        min_x = width
        max_x = 0
        
        for y in range(len(shape)):
            for x in range(width):
                if shape[y][x]:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
        
        return max_x - min_x + 1 if min_x <= max_x else 0
    
    def _simulate_drop(self, board, piece):
        """Simulate dropping a piece and return the landing y-coordinate"""
        while not board.is_collision(piece):
            piece.y += 1
        
        # Move back up one step (to the last valid position)
        piece.y -= 1
        return piece.y
    
    def _evaluate_board(self, board):
        """
        Evaluate a board state using heuristics
        Returns a score (higher is better)
        """
        # Calculate aggregate height
        heights = self._get_column_heights(board)
        aggregate_height = sum(heights)
        
        # Calculate complete lines
        complete_lines = self._count_complete_lines(board)
        
        # Calculate holes
        holes = self._count_holes(board, heights)
        
        # Calculate bumpiness (sum of differences between adjacent columns)
        bumpiness = sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
        
        # Calculate final score using weights
        score = (
            self.weights['aggregate_height'] * aggregate_height +
            self.weights['complete_lines'] * complete_lines +
            self.weights['holes'] * holes +
            self.weights['bumpiness'] * bumpiness
        )
        
        return score
    
    def _get_column_heights(self, board):
        """Get the height of each column (highest block in each column)"""
        heights = [0] * board.width
        
        for x in range(board.width):
            for y in range(board.height):
                if board.grid[y][x]:
                    heights[x] = board.height - y
                    break
        
        return heights
    
    def _count_complete_lines(self, board):
        """Count the number of complete lines in the board"""
        complete_lines = 0
        
        for y in range(board.height):
            if all(board.grid[y]):
                complete_lines += 1
        
        return complete_lines
    
    def _count_holes(self, board, heights):
        """
        Count the number of holes in the board
        A hole is an empty cell with at least one filled cell above it in the same column
        """
        holes = 0
        
        for x in range(board.width):
            # Find the highest block in this column
            top_block_y = board.height
            for y in range(board.height):
                if board.grid[y][x]:
                    top_block_y = y
                    break
            
            # Count holes below the highest block
            for y in range(top_block_y + 1, board.height):
                if not board.grid[y][x]:
                    holes += 1
        
        return holes
    
    def get_ghost_piece(self, board, piece):
        """
        Create a ghost piece showing where the current piece would land
        Returns a copy of the piece at its landing position
        """
        ghost = copy.deepcopy(piece)
        ghost.y = self._simulate_drop(board, copy.deepcopy(piece))
        return ghost
