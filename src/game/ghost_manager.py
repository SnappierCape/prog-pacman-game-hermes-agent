"""Ghost Management Module - Handles spawning, lifecycle, and collision detection with player"""
import time
from entities.ghost import Ghost

# Ghost definition templates
GHOST_TEMPLATES = [
    {'name': 'Blinky', 'color': (255, 0, 0)},      # Red
    {'name': 'Pinky', 'color': (255, 192, 203)},  # Pink  
    {'name': 'Inky', 'color': (0, 255, 255)},      # Cyan
    {'name': 'Clyde', 'color': (255, 165, 0)}      # Orange
]

class GhostManager:
    """Manages ghost entities, spawning schedule, and collision logic"""
    
    def __init__(self, difficulty_settings):
        self.ghosts = []
        self.settings = difficulty_settings
        
        # Extract difficulty configuration
        self.max_ghosts = difficulty_settings['ghost_count']
        # Speed strictly matches Pac-Man (2.0), ignoring difficulty speed factor!
        from config import MOVEMENT_SPEED
        self.base_speed = MOVEMENT_SPEED
        self.spawn_delay = difficulty_settings['spawn_delay']
        
        self.next_spawn_time = time.time() + self.spawn_delay
        
    def update(self, player_x, player_y):
        """Update all active ghosts toward player position"""
        # Handle spawning new ghosts over time based on difficulty
        current_time = time.time()
        while len(self.ghosts) < self.max_ghosts and current_time >= self.next_spawn_time:
            self._spawn_new_ghost()
            self.next_spawn_time = current_time + self.spawn_delay
            
        # Update existing ghost positions via tracking AI  
        for ghost in self.ghosts:
            ghost.update(player_x=player_x, player_y=player_y)
            
    def _spawn_new_ghost(self):
        """Create a new ghost entity with randomized properties"""
        if len(self.ghosts) >= len(GHOST_TEMPLATES):
            return  # Max variety reached
            
        template = GHOST_TEMPLATES[len(self.ghosts)]
        ghost = Ghost(name=template['name'], color=template['color'])
        ghost.speed = self.base_speed
        
        self.ghosts.append(ghost)
        
    def check_player_overlap(self, px, py):
        """Check if any active ghost is touching the player - returns True if collision"""
        for g in self.ghosts:
            dist = g.distance_to_player(px, py)
            # Collision radius sum (ghost radius + pacman radius + buffer)
            if dist < (g.radius + 12 + 4):  
                return True
        return False
