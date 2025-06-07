import pygame
from src.entities.enemies.base_enemy import BaseEnemy

class FastEnemy(BaseEnemy):
    name = "Fast Enemy"
    speed = 110
    hp_default = 20
    reward = 12

    def __init__(self, start_tile, game_manager):
        super().__init__(start_tile, game_manager)
        self.image.fill((60, 200, 220), special_flags=pygame.BLEND_RGBA_ADD)
