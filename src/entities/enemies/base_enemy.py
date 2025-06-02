# src/entities/enemies/base_enemy.py
"""
敵人的基礎類別
定義所有敵人的共同屬性和方法
"""

from abc import ABC, abstractmethod
from enum import Enum
import pygame
from ..base_entity import BaseEntity
from ...utils.constants import ENEMY_SETTINGS

class EnemyType(Enum):
    """敵人類型枚舉"""
    BASIC = "basic"
    FAST = "fast"
    TANK = "tank"

class BaseEnemy(BaseEntity, ABC):
    """敵人的基礎類別"""
    
    def __init__(self, path_points, enemy_type):
        # 從路徑的第一個點開始
        start_x, start_y = path_points[0] if path_points else (0, 0)
        super().__init__(start_x, start_y)
        
        self._enemy_type = enemy_type
        self._path_points = path_points
        self._current_path_index = 0
        
        # 從常數設定中獲取屬性
        settings = ENEMY_SETTINGS[enemy_type.value]
        self._max_health = settings['health']
        self._current_health = self._max_health
        self._speed = settings['speed']
        self._reward = settings['reward']
        self._color = settings['color']
        
        # 狀態屬性
        self._is_alive = True
        self._reached_end = False
        self._slow_effect = 1.0  # 減速效果倍數
        self._slow_duration = 0  # 減速持續時間
        
        # 視覺屬性
        self._size = 15
        
        # 移動相關
        self._target_point = None
        self._set_next_target()
    
    @property
    def enemy_type(self):
        """獲取敵人類型"""
        return self._enemy_type
    
    @property
    def current_health(self):
        """獲取當前血量"""
        return self._current_health
    
    @property
    def max_health(self):
        """獲取最大血量"""
        return self._max_health
    
    @property
    def speed(self):
        """獲取速度"""
        return self._speed * self._slow_effect
    
    @property
    def reward(self):
        """獲取擊殺獎勵"""
        return self._reward
    
    @property
    def is_alive(self):
        """檢查是否存活"""
        return self._is_alive
    
    @property
    def reached_end(self):
        """檢查是否到達終點"""
        return self._reached_end
    
    def _set_next_target(self):
        """設置下一個目標點"""
        if self._current_path_index < len(self._path_points):
            self._target_point = self._path_points[self._current_path_index]
        else:
            self._target_point = None
            self._reached_end = True
    
    def take_damage(self, damage):
        """受到傷害"""
        self._current_health -= damage
        if self._current_health <= 0:
            self._current_health = 0
            self._is_alive = False
    
    def apply_slow_effect(self, slow_factor, duration):
        """應用減速效果"""
        self._slow_effect = min(self._slow_effect, slow_factor)
        self._slow_duration = max(self._slow_duration, duration)
    
    def heal(self, amount):
        """治療"""
        self._current_health = min(self._current_health + amount, self._max_health)
    
    def get_health_percentage(self):
        """獲取血量百分比"""
        return self._current_health / self._max_health
    
    def move_towards_target(self, dt):
        """朝目標點移動"""
        if not self._target_point or not self._is_alive:
            return
        
        # 計算到目標點的距離
        dx = self._target_point[0] - self.x
        dy = self._target_point[1] - self.y
        distance = (dx*dx + dy*dy)**0.5
        
        if distance < 5:  # 到達目標點
            self._current_path_index += 1
            self._set_next_target()
        else:
            # 移動朝向目標點
            move_distance = self.speed * dt / 16.67  # 假設60FPS
            if distance > 0:
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance
    
    def update(self, dt):
        """更新敵人狀態"""
        if not self._is_alive:
            return
        
        # 更新減速效果
        if self._slow_duration > 0:
            self._slow_duration -= dt
            if self._slow_duration <= 0:
                self._slow_effect = 1.0
        
        # 移動
        self.move_towards_target(dt)
    
    def draw(self, screen):
        """繪製敵人"""
        if not self._is_alive:
            return
        
        # 繪製敵人本體
        pygame.draw.circle(screen, self._color, (int(self.x), int(self.y)), self._size)
        
        # 繪製血條
        self._draw_health_bar(screen)
        
        # 如果有減速效果，繪製冰霜效果
        if self._slow_effect < 1.0:
            pygame.draw.circle(screen, (173, 216, 230), 
                             (int(self.x), int(self.y)), self._size, 2)
    
    def _draw_health_bar(self, screen):
        """繪製血條"""
        bar_width = 30
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self._size - 10
        
        # 背景
        pygame.draw.rect(screen, (255, 0, 0), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # 血量
        health_width = bar_width * self.get_health_percentage()
        pygame.draw.rect(screen, (0, 255, 0), 
                        (bar_x, bar_y, health_width, bar_height))
    
    @abstractmethod
    def get_special_ability(self):
        """獲取特殊能力（抽象方法，由子類實現）"""
        pass
