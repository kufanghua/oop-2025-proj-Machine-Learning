"""
塔防遊戲主程式
NYCU OOP Final Project - Tower Defense Game
"""
import pygame
import sys
from src.game.game_manager import GameManager
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """主程式入口函數"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense - OOP Project")
    
    try:
        game_manager = GameManager()
        game_manager.run(screen)
    except Exception as e:
        print(f"遊戲執行錯誤: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
