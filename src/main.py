"""
Pac-Man Game: Entry Point & Main Game Loop.
Handles window setup, event polling (controls), and the primary render cycle.
"""
import pygame
from config import *
from entities.pacMan import PacMan
from game.pellets import PelletManager
from game.player_state import PlayerState
from game.difficulty import DifficultySelector
from game.ghost_manager import GhostManager
from ui.renderer import (clear_screen, draw_maze, draw_pacman, 
                        draw_pellets, draw_ghosts, draw_hud, 
                        draw_lives, draw_game_over)

# Initialize pygame modules
pygame.init()
pygame.font.init() # Wakes up the font engine on Windows
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

def show_difficulty_menu():
    """Simple pre-game menu to select difficulty"""
    diff_selector = DifficultySelector()
    
    running = True
    while running:
        clear_screen(screen)
        
        # Draw title
        title_font = pygame.font.SysFont('segoeuisemibold', 48)
        title = title_font.render("PAC-MAN", True, YELLOW)
        screen.blit(title, (WINDOW_WIDTH//2 - 100, 50))
        
        # Draw subtitle
        sub_font = pygame.font.SysFont('segoeuisemibold', 24)
        sub = sub_font.render("Select Difficulty:", True, WHITE)
        screen.blit(sub, (WINDOW_WIDTH//2 - 80, 120))
        
        # List difficulties
        for idx, diff_name in enumerate(diff_selector.get_available_difficulties()):
            y_pos = 180 + (idx * 50)
            text = sub_font.render(f"{idx+1}. {diff_name}", True, WHITE)
            screen.blit(text, (WINDOW_WIDTH//2 - 80, y_pos))
            
        # Instructions
        inst = sub_font.render("Press 1, 2, or 3 then ENTER to start", True, (200, 200, 200))
        screen.blit(inst, (WINDOW_WIDTH//2 - 140, 380))
        
        pygame.display.flip()
        
        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    diff_selector.current_difficulty = ['easy', 'normal', 'hard'][event.key - pygame.K_1]
                    return diff_selector.settings
                elif event.key == pygame.K_ESCAPE:
                    return None
                
        clock.tick(FPS)

def run_game():
    """Core game loop."""
    # Show difficulty menu (auto-skip if running headlessly on the server)
    import os
    if os.environ.get('SDL_VIDEODRIVER') == 'dummy':
        from game.difficulty import DIFFICULTY_SETTINGS
        diff_settings = DIFFICULTY_SETTINGS['normal'] # Auto-select normal for automated tests
    else:
        diff_selector = DifficultySelector()
        diff_settings = show_difficulty_menu()
        if diff_settings is None:
            return  # User pressed ESC to quit before starting
        
    running = True
    
    # Game entities and managers
    player = PacMan()
    pellets = PelletManager()
    state = PlayerState()
    ghosts = GhostManager(diff_settings)
    
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
            
        # Restart command when Game Over
        if state.game_over:
            if keys[pygame.K_SPACE]:
                state.restart_game()
                player.reset()
            running = False
            
        # Only allow movement if the player is alive 
        if not state.game_over:
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
            
            # Check ghost collisions - this is what makes you lose a life!
            if ghosts.check_player_overlap(player.pos_x, player.pos_y):
                state.lose_life()
                if state.game_over:
                    break  # End the loop, will show game over screen
                else:
                    player.reset()  # Respawn with remaining lives
            
            # Update ghost positions toward player
            ghosts.update(player.pos_x, player.pos_y)
            
            # Out-of-bounds death check (if he slips through the maze somehow)
            if not (0 <= player.pos_x <= WINDOW_WIDTH and 0 <= player.pos_y <= WINDOW_HEIGHT):
                state.lose_life()
                if state.game_over:
                    break
                else:
                    player.reset() # Respawn with remaining lives
            
            pellets.check_pickup(player.pos_x, player.pos_y)

        # 4. Render / Draw everything
        clear_screen(screen)
        draw_maze(screen)
        draw_pellets(screen, pellets)
        draw_ghosts(screen, ghosts.ghosts)  # Draw active ghosts
        if not state.game_over:
            draw_pacman(screen, player)
        draw_hud(screen, pellets.score)
        draw_lives(screen, state.lives)
        
        # Show GAME OVER overlay when dead
        if state.game_over:
            draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run_game()