import sys
import os

# Add src to sys.path for easy imports
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import pygame
from src.game.game_manager import GameManager
from src.ui.menu import MainMenu
from src.utils.constants import TILE_SIZE, FPS

def main():
    pygame.init()
    # 預設小視窗顯示主選單
    dummy_screen = pygame.display.set_mode((400, 300))
    menu = MainMenu(dummy_screen)
    difficulty, map_size = menu.run()  # map_size = (rows, cols)
    rows, cols = map_size

    # 根據地圖格數動態設置視窗大小
    SCREEN_WIDTH = cols * TILE_SIZE
    SCREEN_HEIGHT = rows * TILE_SIZE

    # 以新尺寸重新建立遊戲主視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense OOP Project")
    clock = pygame.time.Clock()

    # 遊戲主迴圈
    game_manager = GameManager(screen, map_size=map_size, difficulty=difficulty)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # 每幀秒數
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