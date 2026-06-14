"""Ghost Entity Module - Enemy AI with pathfinding and tracking behavior"""
import math
from config import WINDOW_HEIGHT, WINDOW_WIDTH
from game.level_loader import TILE_SIZE, is_wall

class Ghost:
    """Represents a ghost entity with basic AI tracking toward the player"""
    
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
        # Spawn in center box (rows 8-10, cols 9-10)
        self.pos_x = WINDOW_WIDTH / 2 - 16  
        self.pos_y = WINDOW_HEIGHT / 2 - 48 
        
        self.speed = 0  # Set based on difficulty
        self.direction = None
        self.radius = 10
        
    def update(self, player_x=None, player_y=None):
        """Basic AI: move toward player's coordinates"""
        if player_x is not None and player_y is not None:
            dx = player_x - self.pos_x
            dy = player_y - self.pos_y
            angle = math.atan2(dy, dx)
            
            # Calculate new position
            new_x = self.pos_x + (self.speed * math.cos(angle))
            new_y = self.pos_y + (self.speed * math.sin(angle))
            
            # Check if move is valid (no wall collision)
            tile_x = int(new_x // TILE_SIZE)
            tile_y = int(new_y // TILE_SIZE)
            
            if not is_wall(tile_x, tile_y):
                self.pos_x = new_x
                self.pos_y = new_y
    
    def distance_to_player(self, player_x, player_y):
        """Calculate distance to player"""
        return math.sqrt((self.pos_x - player_x)**2 + (self.pos_y - player_y)**2)
