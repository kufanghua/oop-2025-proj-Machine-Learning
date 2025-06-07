import pygame
from src.entities.towers.base_tower import BaseTower
from src.entities.projectiles.ice_ball import IceBall
import os

class FreezeTower(BaseTower):
    name = "Freeze Tower"
    cost = 120
    range = 90
    attack_speed = 2.0
    damage = 5
    
    def __init__(self, x, y, game_manager):
        img_path = os.path.join("assets", "images", "towers", "freeze_tower.png")
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))  # 若格子是24x24
        super().__init__(x, y, game_manager)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        
    def shoot(self, target):
        ice_ball = IceBall(self.x, self.y, target, self.damage, self.game_manager)
        self.game_manager.add_projectile(ice_ball)
    '''
    def __init__(self, x, y, game_manager):
        image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(image, (100, 200, 255), (18, 18), 17)
        pygame.draw.rect(image, (60, 180, 255), (10, 26, 16, 6))
        super().__init__(x, y, game_manager)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
   '''       
