"""
Constants and tuning parameters for Pac-Man Game.
Separates "magic numbers" from logic so the game can be easily tuned.
"""

# --- Window / Display Settings ---
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 720
TITLE = "Hermes Arcade: Pacman"
FPS = 60

# --- Color Palette (Retro RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GHOST_SCARED = (33, 33, 222)
GHOST_REDS = [(255, 0, 0), (255, 255, 0), (0, 255, 255)] # Blinky is Red, Inky is Cyan
WALL_COLOR = BLUE

# --- Gameplay Tuning ---
MOVEMENT_SPEED = 2.0   # Halved speed (was 4.0)
COLLISION_RADIUS = 12  # Approximate radius for circle-based collision checks
