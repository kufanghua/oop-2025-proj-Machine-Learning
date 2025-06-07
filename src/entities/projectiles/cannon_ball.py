import pygame
from src.entities.projectiles.base_projectile import BaseProjectile

class CannonBall(BaseProjectile):
    speed = 180
    piercing = False
    splash_radius = 32

    def __init__(self, x, y, target, damage, game_manager):
        image = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(image, (180, 120, 80), (9, 9), 9)
        super().__init__(x, y, target, damage, game_manager)

    def on_hit(self, target):
        # 範圍傷害
        for enemy in self.game_manager.enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            if (dx*dx + dy*dy) ** 0.5 <= self.splash_radius:
                enemy.take_damage(self.damage)
