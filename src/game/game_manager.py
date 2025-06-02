"""
遊戲管理器
統籌遊戲流程與主要邏輯
"""
import pygame
from src.game.map_manager import MapManager
from src.game.wave_manager import WaveManager

class GameManager:
    def __init__(self):
        self.map_manager = MapManager()
        self.wave_manager = WaveManager()
        self.running = True

    def run(self, screen):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000.0  # delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # 可擴充事件處理（例如選單、放置塔等）

            # 更新邏輯
            self.wave_manager.update(dt)
            self.map_manager.update(dt)

            # 繪製畫面
            screen.fill((32, 32, 32))
            self.map_manager.draw(screen)
            self.wave_manager.draw(screen)
            pygame.display.flip()
