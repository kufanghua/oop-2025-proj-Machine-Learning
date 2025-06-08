import pygame
import os
from src.entities.towers.base_tower import BaseTower
from src.entities.projectiles.cannon_ball import CannonBall

class CannonTower(BaseTower):
    name = "Cannon Tower"
    cost = 200
    range = 120
    attack_speed = 1.5
    damage = 30
    max_level = 5
    upgrade_cost_base = 100
    upgrade_damage = 15
    upgrade_attack_speed = 0.1
    '''
    def __init__(self, x, y, game_manager):
        image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(image, (170, 80, 80), (20, 20), 18)
        pygame.draw.rect(image, (70, 50, 50), (12, 30, 16, 8))
        super().__init__(x, y, game_manager)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
    
    def __init__(self, x, y, game_manager):
        img_path = os.path.join("assets", "images", "towers", "cannon_tower.png")
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.scale(image, (24, 24))
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
            imgname = "cannon_tower.png"
        elif self.level >= 2:
            imgname = "cannon_tower_lv2.png"
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
        ball = CannonBall(self.x, self.y, target, self.damage, self.game_manager)
        self.game_manager.add_projectile(ball)
        self.game_manager.audio_manager.play("shoot_cannon")
