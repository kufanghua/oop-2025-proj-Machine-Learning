import pygame
from src.entities.towers.base_tower import BaseTower
from src.entities.projectiles.cannon_ball import CannonBall

class CannonTower(BaseTower):
    name = "Cannon Tower"
    cost = 100
    range = 120
    attack_speed = 1.5
    damage = 40

    def __init__(self, x, y, game_manager):
        image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(image, (170, 80, 80), (20, 20), 18)
        pygame.draw.rect(image, (70, 50, 50), (12, 30, 16, 8))
        super().__init__(x, y, game_manager)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self, target):
        ball = CannonBall(self.x, self.y, target, self.damage, self.game_manager)
        self.game_manager.add_projectile(ball)
