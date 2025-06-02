"""
基礎實體類別
所有遊戲物件的父類別，展示封裝概念
"""
from abc import ABC, abstractmethod
import pygame
import math

class BaseEntity(ABC):
    """所有遊戲實體的基礎類別"""
    
    def __init__(self, x, y):
        """
        初始化基礎實體
        
        Args:
            x (float): X座標
            y (float): Y座標
        """
        self._x = x
        self._y = y
        self._alive = True
        self._rect = pygame.Rect(x-10, y-10, 20, 20)
    
    @property
    def position(self):
        """獲取位置座標"""
        return (self._x, self._y)
    
    @property
    def x(self):
        """獲取X座標"""
        return self._x
    
    @property
    def y(self):
        """獲取Y座標"""
        return self._y
    
    @property
    def alive(self):
        """獲取存活狀態"""
        return self._alive
    
    @property
    def rect(self):
        """獲取碰撞矩形"""
        return self._rect
    
    def distance_to(self, other):
        """
        計算與另一個實體的距離
        
        Args:
            other (BaseEntity): 另一個實體
            
        Returns:
            float: 距離值
        """
        dx = self._x - other._x
        dy = self._y - other._y
        return math.sqrt(dx*dx + dy*dy)
    
    def set_position(self, x, y):
        """
        設定位置
        
        Args:
            x (float): 新的X座標
            y (float): 新的Y座標
        """
        self._x = x
        self._y = y
        self._rect.center = (int(x), int(y))
    
    def destroy(self):
        """銷毀實體"""
        self._alive = False
    
    @abstractmethod
    def update(self, dt):
        """
        更新實體狀態（子類別必須實作）
        
        Args:
            dt (float): 時間差（秒）
        """
        pass
    
    @abstractmethod
    def draw(self, screen):
        """
        繪製實體（子類別必須實作）
        
        Args:
            screen (pygame.Surface): 繪製表面
        """
        pass
