"""
Collision Detection Module.
Translates entity pixel coordinates into grid logic to prevent walking through walls.
Acts as the bridge between Entity pixels and Level Tiles.
"""
from game.level_loader import is_wall, TILE_SIZE

def check_collision(pos_x, pos_y):
    """
    Checks if the center point (pos_x, pos_y) overlaps with a wall tile.
    Returns True if COLLISION detected, False otherwise.
    """
    # Convert pixel coordinates to tile grid coordinates (Integer division)
    x_tile = int(pos_x // TILE_SIZE)
    y_tile = int(pos_y // TILE_SIZE)
    
    # Ask the map loader if this specific tile is a wall (#)
    return is_wall(x_tile, y_tile)

def try_move_player(old_x, old_y, new_x, new_y):
    """
    Logic gate for movement. 
    1. Checks if NEW position hits a wall.
    2. If safe: Returns [True] + new coordinates.
    3. If blocked: Returns [False] + original coordinates (staying put).
    """
    if check_collision(new_x, new_y):
        # Wall hit! Revert to previous position.
        return False, old_x, old_y
        
    # Clear path. Apply the move.
    return True, new_x, new_y
