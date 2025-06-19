"""
Performance Tracker for Neon Tetris
Monitors player performance and adjusts difficulty
"""
import time

class PerformanceTracker:
    def __init__(self):
        """Initialize the Performance Tracker"""
        # Performance metrics
        self.score_history = []
        self.lines_history = []
        self.move_history = []
        self.time_history = []
        
        # Timing
        self.start_time = time.time()
        self.last_check_time = self.start_time
        
        # Difficulty adjustment
        self.base_drop_speed = 1000  # Base speed in milliseconds
        self.min_drop_speed = 100    # Minimum drop speed (fastest)
        self.difficulty_factor = 1.0 # Current difficulty multiplier
        
        # AI recommendation tracking
        self.ai_recommendations = []  # List of (recommended_x, recommended_rotation)
        self.player_moves = []        # List of (actual_x, actual_rotation)
    
    def record_score(self, score, lines_cleared):
        """Record the current score and lines cleared"""
        current_time = time.time()
        self.score_history.append((current_time, score))
        self.lines_history.append((current_time, lines_cleared))
    
    def record_move(self, piece_x, piece_rotation, ai_recommended_x=None, ai_recommended_rotation=None):
        """Record a move made by the player and the AI recommendation if available"""
        current_time = time.time()
        self.move_history.append((current_time, piece_x, piece_rotation))
        
        if ai_recommended_x is not None and ai_recommended_rotation is not None:
            self.ai_recommendations.append((current_time, ai_recommended_x, ai_recommended_rotation))
            self.player_moves.append((current_time, piece_x, piece_rotation))
    
    def get_score_per_minute(self):
        """Calculate the average score per minute"""
        if not self.score_history:
            return 0
        
        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes < 0.1:  # Avoid division by very small numbers
            return 0
            
        latest_score = self.score_history[-1][1]
        return latest_score / elapsed_minutes
    
    def get_lines_per_minute(self):
        """Calculate the average lines cleared per minute"""
        if not self.lines_history:
            return 0
            
        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes < 0.1:  # Avoid division by very small numbers
            return 0
            
        latest_lines = self.lines_history[-1][1]
        return latest_lines / elapsed_minutes
    
    def calculate_move_accuracy(self):
        """
        Calculate how closely the player follows AI recommendations
        Returns a value between 0 (never follows) and 1 (always follows)
        """
        if not self.ai_recommendations or not self.player_moves:
            return 0.5  # Default middle value when no data
        
        # Only consider the last 20 moves to be responsive to recent play style
        ai_recent = self.ai_recommendations[-20:] if len(self.ai_recommendations) > 20 else self.ai_recommendations
        player_recent = self.player_moves[-20:] if len(self.player_moves) > 20 else self.player_moves
        
        if len(ai_recent) != len(player_recent):
            return 0.5  # Should be equal, but just in case
        
        # Calculate match percentage
        matches = 0
        for i in range(len(ai_recent)):
            ai_time, ai_x, ai_rot = ai_recent[i]
            player_time, player_x, player_rot = player_recent[i]
            
            # Consider a match if both position and rotation are the same
            if ai_x == player_x and ai_rot == player_rot:
                matches += 1
        
        return matches / len(ai_recent) if ai_recent else 0.5
    
    def adjust_difficulty(self):
        """
        Adjust difficulty based on player performance
        Returns the new drop speed in milliseconds
        """
        current_time = time.time()
        
        # Only adjust every 30 seconds
        if current_time - self.last_check_time < 30:
            return self.get_current_drop_speed()
        
        self.last_check_time = current_time
        
        # Get performance metrics
        spm = self.get_score_per_minute()
        lpm = self.get_lines_per_minute()
        accuracy = self.calculate_move_accuracy()
        
        # Adjust difficulty factor based on performance
        # Higher score/lines per minute and higher accuracy = higher difficulty
        
        # Base adjustment from score per minute (normalize to expected range)
        score_factor = min(1.5, max(0.5, spm / 1000))
        
        # Adjustment from lines per minute
        lines_factor = min(1.5, max(0.5, lpm / 5))
        
        # Adjustment from AI recommendation accuracy
        # If player follows AI a lot, make it harder
        accuracy_factor = 1.0 + (accuracy - 0.5)
        
        # Combine factors with weights
        self.difficulty_factor = (
            0.5 * score_factor +
            0.3 * lines_factor +
            0.2 * accuracy_factor
        )
        
        # Ensure difficulty stays in reasonable range
        self.difficulty_factor = min(2.0, max(0.5, self.difficulty_factor))
        
        return self.get_current_drop_speed()
    
    def get_current_drop_speed(self):
        """Get the current drop speed based on difficulty factor"""
        # Lower value = faster speed
        speed = self.base_drop_speed / self.difficulty_factor
        
        # Ensure speed stays within limits
        return max(self.min_drop_speed, int(speed))
    
    def reset(self):
        """Reset the performance tracker"""
        self.__init__()
