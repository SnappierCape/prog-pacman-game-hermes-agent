"""Ghost Entity Module - Enemy AI with pathfinding and tracking behavior"""
import math
import random
from config import WINDOW_HEIGHT, WINDOW_WIDTH
from game.level_loader import TILE_SIZE
from game.collisions import try_move_player

class Ghost:
    """Represents a ghost entity with basic AI tracking toward the player"""
    
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
        # Spawn in center box (rows 8-10, cols 9-10)
        self.pos_x = float(WINDOW_WIDTH / 2 - 16)  
        self.pos_y = float(WINDOW_HEIGHT / 2 - 48)
        
        self.speed = 0.0 # Set based on difficulty
        self.direction = None
        self.radius = 8
        
    def update(self, player_x=None, player_y=None):
        """Basic AI: move toward player's coordinates while respecting walls"""
        if player_x is not None and player_y is not None:
            dx = player_x - self.pos_x
            dy = player_y - self.pos_y
            angle = math.atan2(dy, dx)
            
            # Calculate new position using vector attraction
            desired_x = self.pos_x + (self.speed * math.cos(angle))
            desired_y = self.pos_y + (self.speed * math.sin(angle))
            
            # Ask collision engine if move is valid
            success, final_x, final_y = try_move_player(
                self.pos_x, self.pos_y, desired_x, desired_y
            )
            
            if success:
                self.pos_x = final_x
                self.pos_y = final_y
            else:
                # If blocked by a wall, wiggle randomly to find an opening around the obstacle
                wobble_angle = angle + random.choice([-1.5, -0.7, 0.7, 1.5])
                w_x = self.pos_x + (self.speed * math.cos(wobble_angle))
                w_y = self.pos_y + (self.speed * math.sin(wobble_angle))
                
                # Try the wobble move
                w_success, w_final_x, w_final_y = try_move_player(
                    self.pos_x, self.pos_y, w_x, w_y
                )
                
                if w_success:
                    self.pos_x = w_final_x
                    self.pos_y = w_final_y
    
    def distance_to_player(self, player_x, player_y):
        """Calculate distance to player"""
        return math.sqrt((self.pos_x - player_x)**2 + (self.pos_y - player_y)**2)
