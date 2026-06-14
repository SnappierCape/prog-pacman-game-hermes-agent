"""
Level Loader Module.
Defines the raw map data for the game world using a tile-based system.
Maps '#' to Walls and '.' to Walkable paths.
"""

# 20 Columns x 22 Rows (Tile size: 32x32px -> Total: 640x704px approx + margins)
LEVEL_DATA = [
    "####################",
    "#......##.........##",
    "#.##.###.####.###.##",
    "#.##.###.####.###.##",
    "#..................#",
    "#.##.###.##.###.#.##",
    "#.##.###.##.###.#.##",
    "####.#####    #####.",
    "  ####.#####.   ####",
    "     #.......#      ",
    "     #.####.#       ",
    "     #.####.#       ",
    "     #.......#      ",
    "  ####.#####.   ####",
    "####.#####    #####.",
    "#..................#",
    "#.##.######.###.####",
    "#.##.######.###.####",
    "#......##.........##",
    "####################",
]

TILE_SIZE = 32

def get_tile_map():
    """Returns the raw string map."""
    return LEVEL_DATA

def is_wall(x_tile, y_tile):
    """
    Checks if a specific grid coordinate is a wall.
    Returns True if it's a '#', False otherwise (including out-of-bounds safety).
    """
    try:
        row = LEVEL_DATA[y_tile]
        if len(row) > x_tile and row[x_tile] == "#":
            return True
    except IndexError:
        pass
    # Out of bounds or non-wall characters treated as empty space for now.
    return False
