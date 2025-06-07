import pygame
from src.entities.projectiles.base_projectile import BaseProjectile

class IceBall(BaseProjectile):
    cost = 20  # 可依需求調整

    def __init__(self, x, y, target, damage, game_manager):
        super().__init__(x, y, target, damage, game_manager)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (180, 220, 255), (8, 8), 8)
        pygame.draw.circle(self.image, (100, 180, 255), (8, 8), 5)
        self.slow_effect = 0.5  # 被擊中敵人減速比例
        self.slow_time = 1.5    # 減速持續秒數

    def hit(self, enemy):
        enemy.take_damage(self.damage)
        if hasattr(enemy, "slow"):
            enemy.slow(self.slow_effect, self.slow_time)
        self.kill()
