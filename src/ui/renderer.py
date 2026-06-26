"""
UI Render Module.
Handles visualizing the maze structure, entities, collectibles, and HUD.
Uses positional arguments strictly to support older Pygame kernels locally.
"""
import pygame
from config import BLACK, BLUE, YELLOW, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT
from game.level_loader import get_tile_map, TILE_SIZE

def draw_maze(screen):
    """Iterates over grid data and draws walls (BLUE rectangles)."""
    rows = get_tile_map()
    
    for y_idx, row in enumerate(rows):
        for x_idx, tile_type in enumerate(row):
            rect_x = x_idx * TILE_SIZE
            rect_y = y_idx * TILE_SIZE
            
            if tile_type == '#':
                pygame.draw.rect(screen, BLUE, (rect_x, rect_y, TILE_SIZE, TILE_SIZE))
            elif tile_type == '.':
                # Render a little white dot in the center of empty lanes
                pygame.draw.rect(screen, WHITE, 
                                (rect_x + 14, rect_y + 14, 4, 5))

def draw_pacman(screen, pm):
    """Draws the player entity as a yellow circle."""
    radius = 12
    pygame.draw.circle(screen, YELLOW, (int(pm.pos_x), int(pm.pos_y)), radius)

def draw_pellets(screen, pellet_manager):
    """Draws all active pellets on the board based on their tier."""
    for p in pellet_manager.pellets:
        # Positional args ONLY
        pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['radius'])

def draw_ghosts(screen, ghosts):
    """Renders all active ghost entities on the screen buffer."""
    for g in ghosts:
        pygame.draw.circle(screen, g.color, (int(g.pos_x), int(g.pos_y)), g.radius)

def draw_hud(screen, score):
    """Renders the Score counter in the top-left corner."""
    hud_font = pygame.font.SysFont('segoeuisemibold', 24) 
    # STRICTLY positional rendering (text, antialias_bool, color_tuple)
    text = hud_font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_lives(screen, lives):
    """Renders the remaining lives in the top-right corner as yellow circles."""
    for i in range(lives - 1):
        pygame.draw.circle(screen, YELLOW, (WINDOW_WIDTH - 30 - (i * 30), 25), 8)

def draw_game_over(screen):
    """Renders a big red 'GAME OVER' overlay when lives hit zero."""
    go_font = pygame.font.SysFont('segoeuisemibold', 48)
    text = go_font.render("GAME OVER", True, (255, 0, 0))
    rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, rect)

def clear_screen(screen):
    """Wipes the display to solid black before re-rendering the frame."""
    screen.fill(BLACK)
