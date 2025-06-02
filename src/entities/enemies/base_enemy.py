"""
敵人基礎類別
所有敵人的父類別
"""
import pygame
from src.entities.base_entity import BaseEntity
from src.utils.constants import RED, GREEN

class BaseEnemy(BaseEntity):
    """敵人的基礎類別"""
    
    def __init__(self, x, y, enemy_type):
        """
        初始化敵人
        
        Args:
            x (float): 起始X座標
            y (float): 起始Y座標
            enemy_type (str): 敵人類型
        """
        super().__init__(x, y)
        from src.utils.constants import ENEMY_STATS
        
        stats = ENEMY_STATS[enemy_type]
        self._max_hp = stats['hp']
        self._hp = stats['hp']
        self._speed = stats['speed']
        self._reward = stats['reward']
        
        self._path_index = 0
        self._slow_effect = 1.0
        self._slow_duration = 0
        self._enemy_type = enemy_type
    
    @property
    def hp(self):
        """獲取當前血量"""
        return self._hp
    
    @property
    def max_hp(self):
        """獲取最大血量"""
        return self._max_hp
    
    @property
    def reward(self):
        """獲取擊殺獎勵"""
        return self._reward
    
    @property
    def path_index(self):
        """獲取路徑索引"""
        return self._path_index
    
    def take_damage(self, damage):
        """
        受到傷害
        
        Args:
            damage (int): 傷害值
        """
        self._hp -= damage
        if self._hp <= 0:
            self._alive = False
    
    def apply_slow(self, slow_factor, duration):
        """
        應用減速效果
        
        Args:
            slow_factor (float): 減速倍率 (0.0-1.0)
            duration (float): 持續時間（秒）
        """
        self._slow_effect = min(self._slow_effect, slow_factor)
        self._slow_duration = max(self._slow_duration, duration)
    
    def move_along_path(self, path, dt):
        """
        沿路徑移動
        
        Args:
            path (list): 路徑點列表
            dt (float): 時間差（秒）
        """
        if self._path_index >= len(path) - 1:
            self._alive = False  # 到達終點
            return
        
        # 更新減速效果
        if self._slow_duration > 0:
            self._slow_duration -= dt
        else:
            self._slow_effect = 1.0
        
        # 計算移動
        current_speed = self._speed * self._slow_effect
        target = path[self._path_index + 1]
        
        dx = target[0] - self._x
        dy = target[1] - self._y
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance < 5:  # 接近路徑點
            self._path_index += 1
        else:
            # 移動向目標
            move_distance = current_speed * dt
            self.set_position(
                self._x + (dx / distance) * move_distance,
                self._y + (dy / distance) * move_distance
            )
    
    def update(self, dt):
        """更新敵人狀態"""
        pass
    
    def draw(self, screen):
        """繪製敵人和血條"""
        # 繪製敵人本體
        color = self._get_color()
        pygame.draw.circle(screen, color, (int(self._x), int(self._y)), 12)
        
        # 繪製血條
        self._draw_health_bar(screen)
    
    def _draw_health_bar(self, screen):
        """繪製血條"""
        bar_width = 30
        bar_height = 5
        bar_x = self._x - bar_width // 2
        bar_y = self._y - 20
        
        # 背景
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # 血量
        hp_ratio = max(0, self._hp / self._max_hp)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * hp_ratio, bar_height))
    
    @abstractmethod
    def _get_color(self):
        """獲取敵人顏色（子類別實作）"""
        pass
    
    @abstractmethod
    def get_special_ability(self):
        """獲取特殊能力（多型應用）"""
        pass
