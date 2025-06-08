import pygame
import os
from src.entities.enemies.base_enemy import BaseEnemy

class BasicEnemy(BaseEnemy):
    name = "Basic Enemy"
    base_speed = 60      # 覆寫父類
    base_hp = 30         # 覆寫父類
    reward = 10

    def __init__(self, start_tile, game_manager):
        super().__init__(start_tile, game_manager)
        img_path = os.path.join("assets", "images", "enemies", "enemy_basic.png")
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))
        self.image = image