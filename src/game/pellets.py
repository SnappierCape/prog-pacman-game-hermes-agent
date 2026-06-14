"""
Pellet / Collectible System.
Populates the map with 3 tiers of collectibles based on weighted probability.
Handles consumption logic and point tracking.
"""
import random
from game.level_loader import get_tile_map, TILE_SIZE

# --- Pellet Tier Definitions ---
PELLET_TIERS = {
    'DOT': {'color': (255, 255, 255), 'points': 1, 'radius': 3, 'weight': 70},   # White, common
    'POWER': {'color': (255, 223, 0), 'points': 5, 'radius': 6, 'weight': 25},     # Gold, medium
    'SUPER': {'color': (255, 0, 255), 'points': 10, 'radius': 9, 'weight': 5}       # Magenta, rare
}

class PelletManager:
    """Manages all collectibles on the board and tracks scoring."""
    
    def __init__(self):
        self.pellets = []      # List of active pellets [{'x', 'y', 'tier', ...}]
        self.score = 0
        self.populate_map()

    def populate_map(self):
        """Scan every empty path tile and roll dice to decide if a pellet spawns."""
        self.pellets = []
        rows = get_tile_map()
        
        # Total weight for probability math (70 + 25 + 5 = 100)
        total_weight = sum(t['weight'] for t in PELLET_TIERS.values())
        
        for y_idx, row in enumerate(rows):
            for x_idx, tile in enumerate(row):
                if tile == '.':   # Empty path is eligible for pellets
                    # Roll 1-100 and match against tier weights
                    roll = random.randint(1, total_weight)
                    
                    # Determine which tier was picked by subtracting weights
                    cumulative = 0
                    selected_tier = self._select_tier(roll)

                    if selected_tier:
                        pixel_x = (x_idx * TILE_SIZE) + (TILE_SIZE // 2)
                        pixel_y = (y_idx * TILE_SIZE) + (TILE_SIZE // 2)
                        
                        tier_data = PELLET_TIERS[selected_tier]
                        self.pellets.append({
                            'x': float(pixel_x),
                            'y': float(pixel_y),
                            'tier': selected_tier,
                            'color': tier_data['color'],
                            'radius': tier_data['radius'],
                            'points': tier_data['points']
                        })

    def _select_tier(self, roll):
        """Convert a random number into a specific pellet tier."""
        cumulative = 0
        for name, data in PELLET_TIERS.items():
            cumulative += data['weight']
            if roll <= cumulative:
                return name
        # Fallback to most common if rounding errors occur
        return 'DOT'

    def check_pickup(self, player_x, player_y):
        """
        Check if player is touching any active pellet.
        If yes, remove it and add points. Returns True if a pickup occurred.
        """
        hit = False
        remaining = []

        for pellet in self.pellets:
            dist = ((player_x - pellet['x'])**2 + (player_y - pellet['y'])**2)**0.5
            
            # If distance + radii overlap, it's a collision
            if dist < 12 + pellet['radius']:
                self.score += pellet['points']
                hit = True
            else:
                remaining.append(pellet)

        self.pellets = remaining
        return hit
