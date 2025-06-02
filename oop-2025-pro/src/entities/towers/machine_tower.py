"""
機槍塔類別 - 高射速、低傷害的塔
"""
from .base_tower import BaseTower
from ..projectiles.bullet import Bullet
from ...utils.constants import TowerType, ProjectileType


class MachineTower(BaseTower):
    """機槍塔類別 - 射速快但傷害較低"""
    
    def __init__(self, x, y):
        # 機槍塔屬性
        damage = 15
        attack_range = 120
        attack_speed = 0.3  # 攻擊間隔短 = 射速快
        cost = 150
        
        super().__init__(x, y, damage, attack_range, attack_speed, cost)
        
        self.tower_type = TowerType.MACHINE
        self.projectile_type = ProjectileType.BULLET
        self.name = "機槍塔"
        
        # 機槍塔特殊屬性
        self.burst_count = 3  # 連發子彈數
        self.burst_delay = 0.1  # 連發間隔
        self.current_burst = 0
        self.last_burst_time = 0
        
    def create_projectile(self, target):
        """創建子彈投射物"""
        if target:
            return Bullet(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target,
                self.damage
            )
        return None
    
    def attack(self, enemies, current_time):
        """機槍塔的連發攻擊"""
        projectiles = []
        
        # 檢查是否在連發模式中
        if self.current_burst > 0:
            if current_time - self.last_burst_time >= self.burst_delay:
                target = self.find_target(enemies)
                if target:
                    projectile = self.create_projectile(target)
                    if projectile:
                        projectiles.append(projectile)
                
                self.current_burst -= 1
                self.last_burst_time = current_time
        else:
            # 正常攻擊冷卻檢查
            if current_time - self.last_attack_time >= self.attack_speed:
                target = self.find_target(enemies)
                if target:
                    # 開始連發
                    self.current_burst = self.burst_count - 1  # 第一發立即射出
                    self.last_burst_time = current_time
                    self.last_attack_time = current_time
                    
                    projectile = self.create_projectile(target)
                    if projectile:
                        projectiles.append(projectile)
        
        return projectiles
    
    def upgrade(self):
        """升級機槍塔"""
        if self.level < self.max_level:
            self.level += 1
            
            # 升級效果
            self.damage = int(self.damage * 1.3)
            self.attack_range = int(self.attack_range * 1.1)
            self.attack_speed *= 0.9  # 攻擊間隔縮短
            self.burst_count += 1  # 增加連發數
            self.cost = int(self.cost * 1.5)
            
            return True
        return False
    
    def get_stats(self):
        """獲取塔的詳細屬性"""
        stats = super().get_stats()
        stats.update({
            'burst_count': self.burst_count,
            'burst_delay': self.burst_delay,
            'dps': round(self.damage * self.burst_count / self.attack_speed, 1)
        })
        return stats
    
    def get_description(self):
        """獲取塔的描述"""
        return f"高射速機槍塔\n傷害: {self.damage}\n射程: {self.attack_range}\n連發: {self.burst_count}發"
