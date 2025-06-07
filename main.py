import sys
import os

# Add src to sys.path for easy imports
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import pygame
from src.game.game_manager import GameManager
from src.ui.menu import MainMenu
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense OOP Project")
    clock = pygame.time.Clock()

    # Main Menu
    menu = MainMenu(screen)
    menu.run()

    # Game Loop
    game_manager = GameManager(screen)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)
        game_manager.update(dt)
        game_manager.draw()
        pygame.display.flip()

        if game_manager.is_game_over():
            menu.show_game_over(game_manager.get_final_score())
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
