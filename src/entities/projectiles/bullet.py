import pygame
from src.entities.projectiles.base_projectile import BaseProjectile

class Bullet(BaseProjectile):
    speed = 350
    piercing = False

    def __init__(self, x, y, target, damage, game_manager):
        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(image, (90, 90, 230), (5, 5), 5)
        super().__init__(x, y, target, damage, game_manager)
