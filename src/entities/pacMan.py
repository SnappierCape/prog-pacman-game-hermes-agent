"""Pac-Man Player Entity with Hold-to-Move Logic."""
import math
from config import WINDOW_HEIGHT, WINDOW_WIDTH, MOVEMENT_SPEED
from game.level_loader import TILE_SIZE
from game.collisions import try_move_player

# Fixed: PI -> pi (Lowercase is correct Python standard)
DIRS = dict(RIGHT=0, DOWN=math.pi/2, LEFT=math.pi, UP=-math.pi/2)

class PacMan:
    """Represents the player-controlled character."""
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Spawn Pac-Man in an open lane ('.') so he isn't stuck inside a wall on startup."""
        self.pos_x = float(WINDOW_WIDTH // 2) 
        self.pos_y = float(TILE_SIZE * 4 + 16)
        self.target_angle = DIRS['RIGHT']
        self.is_moving = False   # Default state: Brake is ON
        
    def set_direction(self, key_code):
        """Translate Pygame key codes into movement angles."""
        mapping = {
            'UP': DIRS['UP'],
            'DOWN': DIRS['DOWN'],
            'LEFT': DIRS['LEFT'],
            'RIGHT': DIRS['RIGHT'],
        }
        
        if key_code == 'STILL':
            self.is_moving = False   # The brake!
        else:
            self.target_angle = mapping.get(key_code, self.target_angle)
            self.is_moving = True
        
    def update(self):
        """Move Pac-Man one step in target direction; blocked by walls."""
        if not self.is_moving:
            return # Stand still until a key is held
            
        # 1. Calculate prospective destination based on angle and speed
        delta_x = MOVEMENT_SPEED * math.cos(self.target_angle)
        delta_y = MOVEMENT_SPEED * math.sin(self.target_angle)
        
        desired_x = self.pos_x + delta_x
        desired_y = self.pos_y + delta_y
        
        # 2. Ask collision engine if the move is safe (doesn't overlap a wall tile)
        success, final_x, final_y = try_move_player(
            self.pos_x, self.pos_y, desired_x, desired_y
        )
        
        # 3. Only update position coordinates if the move was approved
        if success:
            self.pos_x = final_x
            self.pos_y = final_y
