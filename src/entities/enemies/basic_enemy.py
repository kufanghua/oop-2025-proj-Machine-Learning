import pygame
from src.entities.enemies.base_enemy import BaseEnemy

class BasicEnemy(BaseEnemy):
    name = "Basic Enemy"
    speed = 60
    hp_default = 30
    reward = 10

    def __init__(self, start_tile, game_manager):
        super().__init__(start_tile, game_manager)
        self.image.fill((200, 60, 60), special_flags=pygame.BLEND_RGBA_ADD)
