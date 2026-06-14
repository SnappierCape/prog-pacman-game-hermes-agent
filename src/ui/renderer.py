"""
UI Render Module.
Handles visualizing the maze structure, entities, collectibles, and HUD.
"""
import pygame
from config import BLACK, BLUE, YELLOW, WHITE
from game.level_loader import get_tile_map, TILE_SIZE

FONT = pygame.font.SysFont(None, 24)

def draw_maze(screen):
    """Iterates over grid data and draws walls (BLUE rectangles)."""
    rows = get_tile_map()
    
    for y_idx, row in enumerate(rows):
        for x_idx, tile_type in enumerate(row):
            if tile_type == '#':
                # Calculate pixel coordinates from tile indices
                rect_x = x_idx * TILE_SIZE
                rect_y = y_idx * TILE_SIZE
                
                # Draw a rectangle of exactly one tile size
                pygame.draw.rect(screen, BLUE, 
                                (rect_x, rect_y, TILE_SIZE, TILE_SIZE))

def draw_pacman(screen, pm):
    """Draws the player entity as a yellow circle."""
    # Note: Pygame draws from the top-left corner. 
    # Our entity pos is the CENTER, so we subtract half the radius for alignment.
    radius = 12 
    
    pygame.draw.circle(screen, YELLOW, 
                      (int(pm.pos_x), int(pm.pos_y)), 
                      radius)

def draw_pellets(screen, pellet_manager):
    """Draws all active pellets on the board based on their tier."""
    for p in pellet_manager.pellets:
        pygame.draw.circle(
            screen,
            p['color'],
            (int(p['x']), int(p['y'])),
            p['radius']
        )

def draw_hud(screen, score):
    """Renders the Score counter in the top-left corner."""
    text = FONT.render(f"Score: {score}", antialias=True, color=WHITE)
    screen.blit(text, (10, 10))

def clear_screen(screen):
    """Wipes the display to solid black before re-rendering the frame."""
    screen.fill(BLACK)
