import pygame
from src.entities.projectiles.base_projectile import BaseProjectile

class Bullet(BaseProjectile):
    speed = 350
    piercing = False

    def __init__(self, x, y, target, damage, game_manager):
        super().__init__(x, y, target, damage, game_manager)
        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        
