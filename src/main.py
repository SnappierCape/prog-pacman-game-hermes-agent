"""
Pac-Man Game: Entry Point & Main Game Loop.
Handles window setup, event polling (controls), and the primary render cycle.
"""
import pygame
from config import *
from entities.pacMan import PacMan
from game.pellets import PelletManager
from ui.renderer import clear_screen, draw_maze, draw_pacman, draw_pellets, draw_hud

# Initialize pygame modules
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

def run_game():
    """Core game loop."""
    running = True
    
    # Game entities and managers
    player = PacMan()
    pellets = PelletManager()
    
    while running:
        # 1. Handle Window Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # 2. Poll Input State (Checks every frame what is currently held)
        keys = pygame.key.get_pressed()
        
        # Quit command
        if keys[pygame.K_ESCAPE]:
            running = False
            
        # Movement commands via polling (hold to move, release to stop)
        current_dir = 'STILL'  
        if keys[pygame.K_UP]:
            current_dir = 'UP'
        elif keys[pygame.K_RIGHT]:
            current_dir = 'RIGHT'
        elif keys[pygame.K_DOWN]:
            current_dir = 'DOWN'
        elif keys[pygame.K_LEFT]:
            current_dir = 'LEFT'
            
        player.set_direction(current_dir)

        # 3. Update Game State (Move entities, check collisions, pickup pellets)
        player.update()
        pellets.check_pickup(player.pos_x, player.pos_y)

        # 4. Render / Draw everything
        clear_screen(screen)
        draw_maze(screen)
        draw_pellets(screen, pellets)
        draw_pacman(screen, player)
        draw_hud(screen, pellets.score)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run_game()
