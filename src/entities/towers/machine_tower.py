import pygame
from src.entities.towers.base_tower import BaseTower
from src.entities.projectiles.bullet import Bullet
import os
class MachineTower(BaseTower):
    name = "Machine Tower"
    cost = 80
    range = 90
    attack_speed = 0.5
    damage = 8
    max_level = 5
    upgrade_cost_base = 120
    upgrade_damage = 4
    upgrade_attack_speed = 0.05
    '''
    def __init__(self, x, y, game_manager):
        image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(image, (80, 120, 180), (18, 18), 16)
        pygame.draw.rect(image, (30, 30, 60), (13, 25, 10, 7))
        super().__init__(x, y, game_manager)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
   
    def __init__(self, x, y, game_manager):
        img_path = os.path.join("assets", "images", "towers", "machine_tower.png")
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
            imgname = "machine_tower.png"
        elif self.level >= 2:
            imgname = "machine_tower_lv2.png"
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
        bullet = Bullet(self.x, self.y, target, self.damage, self.game_manager)
        self.game_manager.add_projectile(bullet)
        self.game_manager.audio_manager.play("shoot_machine")
