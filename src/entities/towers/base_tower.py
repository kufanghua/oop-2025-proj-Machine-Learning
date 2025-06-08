import pygame
from src.entities.base_entity import BaseEntity
from src.utils.constants import TILE_SIZE

class BaseTower(BaseEntity):
    name = "BaseTower"
    cost = 50
    range = 100
    attack_speed = 1.0  # seconds
    damage = 10
    max_level = 5
    upgrade_cost_base = 40
    upgrade_damage = 8
    upgrade_attack_speed = 0.12  # 每級攻速提升（秒變短）

    def __init__(self, x, y, game_manager):
        image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(image, (120, 120, 120), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2)
        super().__init__(x, y, image)
        self.game_manager = game_manager
        self.attack_cooldown = 0
        self.level = 1

    def update(self, dt):
        self.attack_cooldown -= dt
        if self.attack_cooldown <= 0:
            target = self.find_target()
            if target:
                self.shoot(target)
                self.attack_cooldown = self.attack_speed

    def find_target(self):
        for enemy in self.game_manager.enemies:
            if self.distance_to(enemy) <= self.range:
                return enemy
        return None

    def shoot(self, target):
        pass  # 子類覆寫

    def distance_to(self, entity):
        dx = self.x - entity.x
        dy = self.y - entity.y
        return (dx*dx + dy*dy) ** 0.5

    def can_upgrade(self):
        return self.level < self.max_level

    def upgrade_cost(self):
        return self.upgrade_cost_base * self.level  # 可依需求調整

    def upgrade(self):
        if self.can_upgrade() and self.game_manager.money >= self.upgrade_cost():
            self.game_manager.money -= self.upgrade_cost()
            self.level += 1
            self.damage += self.upgrade_damage
            self.attack_speed = max(0.1, self.attack_speed - self.upgrade_attack_speed)
            self.game_manager.audio_manager.play("upgrade")
            # 可增加升級動畫或音效
            return True
        return False
