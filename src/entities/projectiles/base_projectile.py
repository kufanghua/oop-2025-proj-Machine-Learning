
import pygame
from src.entities.base_entity import BaseEntity

class BaseProjectile(BaseEntity):
    speed = 320
    piercing = False

    def __init__(self, x, y, target, damage, game_manager):
        image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(image, (200, 200, 200), (6, 6), 6)
        super().__init__(x, y, image)
        self.target = target
        self.damage = damage
        self.game_manager = game_manager

    def update(self, dt):
        if not self.target or not self.target.is_alive():
            self.kill()
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < self.speed * dt:
            self.x, self.y = self.target.x, self.target.y
            self.rect.center = (self.x, self.y)
            self.on_hit(self.target)
            self.kill()
        else:
            self.x += dx / dist * self.speed * dt
            self.y += dy / dist * self.speed * dt
            self.rect.center = (self.x, self.y)

    def on_hit(self, target):
        target.take_damage(self.damage)
