import pygame
from src.entities.enemies.base_enemy import BaseEnemy

class TankEnemy(BaseEnemy):
    name = "Tank Enemy"
    speed = 35
    hp_default = 90
    reward = 22

    def __init__(self, start_tile, game_manager):
        super().__init__(start_tile, game_manager)
        self.image.fill((120, 120, 120), special_flags=pygame.BLEND_RGBA_ADD)
