"""
塔基礎類別
所有塔的父類別，展示繼承概念
"""
import time
from src.entities.base_entity import BaseEntity

class BaseTower(BaseEntity):
    """塔的基礎類別"""
    
    def __init__(self, x, y, tower_type):
        """
        初始化塔
        
        Args:
            x (float): X座標
            y (float): Y座標  
            tower_type (str): 塔類型
        """
        super().__init__(x, y)
        from src.utils.constants import TOWER_STATS, TOWER_COST
        
        stats = TOWER_STATS[tower_type]
        self._damage = stats['damage']
        self._range = stats['range']
        self._attack_speed = stats['attack_speed']
        self._cost = TOWER_COST[tower_type]
        
        self._target = None
        self._last_attack_time = 0
        self._tower_type = tower_type
    
    @property
    def range(self):
        """獲取射程"""
        return self._range
    
    @property
    def cost(self):
        """獲取建造成本"""
        return self._cost
    
    @property
    def target(self):
        """獲取目標"""
        return self._target
    
    def find_target(self, enemies):
        """
        尋找射程內的敵人目標
        
        Args:
            enemies (list): 敵人列表
        """
        self._target = None
        min_distance = float('inf')
        
        for enemy in enemies:
            if enemy.alive:
                distance = self.distance_to(enemy)
                if distance <= self._range and distance < min_distance:
                    self._target = enemy
                    min_distance = distance
    
    def can_attack(self):
        """檢查是否可以攻擊"""
        current_time = time.time()
        return (current_time - self._last_attack_time) >= (1.0 / self._attack_speed)
    
    def attack(self):
        """
        攻擊目標
        
        Returns:
            Projectile: 產生的投射物，如果無法攻擊則返回None
        """
        if self._target and self._target.alive and self.can_attack():
            self._last_attack_time = time.time()
            return self._create_projectile()
        return None
    
    @abstractmethod
    def _create_projectile(self):
        """
        創建投射物（多型應用點）
        子類別必須實作此方法
        
        Returns:
            Projectile: 對應的投射物
        """
        pass
    
    def update(self, dt):
        """更新塔狀態"""
        # 基礎塔類別的更新邏輯
        pass
    
    @abstractmethod
    def draw(self, screen):
        """繪製塔（子類別實作具體樣式）"""
        pass
