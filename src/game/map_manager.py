"""
地圖管理
負責遊戲地圖的繪製、路徑規劃
"""
import pygame

class MapManager:
    def __init__(self):
        # 預設簡單路徑點，可依需求擴充
        self.path = [(50, 300), (200, 300), (400, 200), (600, 400), (750, 300)]

    def update(self, dt):
        # 地圖通常較少更新，預留擴充
        pass

    def draw(self, screen):
        # 畫地圖背景
        pygame.draw.rect(screen, (60, 100, 60), (0, 0, 800, 600))
        # 畫路徑
        if len(self.path) > 1:
            pygame.draw.lines(screen, (200, 200, 80), False, self.path, 12)
