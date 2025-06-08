import pygame
import os
from src.entities.enemies.base_enemy import BaseEnemy

class FastEnemy(BaseEnemy):
    name = "Fast Enemy"
    speed = 110
    hp_default = 20
    reward = 12

    def __init__(self, start_tile, game_manager):
        super().__init__(start_tile, game_manager)
        img_path = os.path.join("assets", "images", "enemies", "enemy_fast.png")
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))
        self.image = image
