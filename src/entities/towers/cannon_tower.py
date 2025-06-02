"""
砲塔類別
高傷害、慢攻速的塔，展示多型概念
"""
import pygame
from src.entities.towers.base_tower import BaseTower
from src.entities.projectiles.cannon_ball import CannonBall
from src.utils.constants import RED, BLACK

class CannonTower(BaseTower):
    """砲塔類別 - 高傷害，慢攻速"""
    
    def __init__(self, x, y):
        """初始化砲塔"""
        super().__init__(x, y, 'cannon')
    
    def _create_projectile(self):
        """
        創建砲彈（多型實作）
        
        Returns:
            CannonBall: 砲彈投射物
        """
        if self._target:
            return CannonBall(self._x, self._y, self._target, self._damage)
        return None
    
    def draw(self, screen):
        """繪製砲塔"""
        # 塔身
        pygame.draw.circle(screen, RED, (int(self._x), int(self._y)), 20)
        pygame.draw.circle(screen, BLACK, (int(self._x), int(self._y)), 20, 3)
        
        # 砲管方向指示
        if self._target:
            import math
            dx = self._target.x - self._x
            dy = self._target.y - self._y
            angle = math.atan2(dy, dx)
            end_x = self._x + math.cos(angle) * 25
            end_y = self._y + math.sin(angle) * 25
            pygame.draw.line(screen, BLACK, (self._x, self._y), (end_x, end_y), 5)
