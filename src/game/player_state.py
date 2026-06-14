"""
Player State Module
Tracks lives, score, and game over conditions
"""

STARTING_LIVES = 3

class PlayerState:
    def __init__(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.game_over = False
        
    def lose_life(self):
        """Called when pacman dies - loses a life and checks for game over"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            
    def add_score(self, points):
        """Add points to the player's score"""
        self.score += points
        
    def reset_player_position(self):
        """Reset pacman to starting position after dying"""
        # This will be called from main.py when needed
        pass
        
    def restart_game(self):
        """Full game restart - resets lives and score"""
        self.lives = STARTING_LIVES
        self.score = 0
        self.game_over = False
