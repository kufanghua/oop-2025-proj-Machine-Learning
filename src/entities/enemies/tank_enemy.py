import pygame
import os
from src.entities.enemies.base_enemy import BaseEnemy


class TankEnemy(BaseEnemy):
    name = "Tank Enemy"
    speed = 35
    hp_default = 90
    reward = 22

    def __init__(self, start_tile, game_manager):
        super().__init__(start_tile, game_manager)
        img_path = os.path.join("assets", "images", "enemies", "enemy_tank.png")
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))
        self.image = image
