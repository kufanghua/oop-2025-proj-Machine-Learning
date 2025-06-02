# src/entities/projectiles/cannon_ball.py
"""
加農砲投射物類別
"""

from .base_projectile import BaseProjectile
from ...utils.constants import ProjectileType

class CannonBall(BaseProjectile):
    """加農砲投射物"""
    
    def __init__(self, x, y, target_x, target_y, damage=25):
        super().__init__(x, y, target_x, target_y, ProjectileType.CANNON_BALL)
        self.damage = damage
        self._explosion_radius = 20  # 爆炸半徑
    
    def on_target_reached(self):
        """到達目標時產生爆炸效果"""
        # 這裡可以添加爆炸動畫或音效
        pass
    
    def get_special_effect(self):
        """獲取特殊效果：範圍傷害"""
        return {
            'type': 'area_damage',
            'radius': self._explosion_radius,
            'damage': self.damage
        }
    
    def apply_area_damage(self, enemies):
        """對範圍內的敵人造成傷害"""
        damaged_enemies = []
        for enemy in enemies:
            distance = self.distance_to(enemy)
            if distance <= self._explosion_radius:
                enemy.take_damage(self.damage)
                damaged_enemies.append(enemy)
        return damaged_enemies
