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
    max_level = 4
    upgrade_cost_base = 60
    upgrade_damage = 5
    upgrade_attack_speed = 0.12
    '''
    def __init__(self, x, y, game_manager):
        img_path = os.path.join("assets", "images", "towers", "freeze_tower.png")
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))  # 若格子是24x24
        super().__init__(x, y, game_manager)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
    '''
    def __init__(self, x, y, game_manager):
        self.level = 1
        super().__init__(x, y, game_manager)
        self.set_image()

    def set_image(self):
        if self.level == 1:
            imgname = "freeze_tower.png"
        elif self.level >= 2:
            imgname = "freeze_tower_lv2.png"
        img_path = os.path.join("assets", "images", "towers", imgname)
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def upgrade(self):
        if super().upgrade():
            self.set_image()  # 升級時自動換圖
            return True
        return False
    
        
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
