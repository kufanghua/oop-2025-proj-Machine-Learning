"""
冰凍塔類別 - 具有減速效果的塔
"""
from .base_tower import BaseTower
from ..projectiles.ice_ball import IceBall
from ...utils.constants import TowerType, ProjectileType


class FreezeTower(BaseTower):
    """冰凍塔類別 - 造成傷害並減速敵人"""
    
    def __init__(self, x, y):
        # 冰凍塔屬性
        damage = 25
        attack_range = 100
        attack_speed = 1.2  # 攻擊較慢但有特殊效果
        cost = 200
        
        super().__init__(x, y, damage, attack_range, attack_speed, cost)
        
        self.tower_type = TowerType.FREEZE
        self.projectile_type = ProjectileType.ICE_BALL
        self.name = "冰凍塔"
        
        # 冰凍塔特殊屬性
        self.slow_effect = 0.5  # 減速效果 (50%速度)
        self.slow_duration = 2.0  # 減速持續時間(秒)
        self.splash_radius = 50  # 濺射範圍
        
    def create_projectile(self, target):
        """創建冰球投射物"""
        if target:
            return IceBall(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target,
                self.damage,
                self.slow_effect,
                self.slow_duration,
                self.splash_radius
            )
        return None
    
    def find_target(self, enemies):
        """優先攻擊最近的敵人(適合控場)"""
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            if enemy.is_alive():
                distance = self.calculate_distance(enemy)
                if distance <= self.attack_range and distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy
        
        return closest_enemy
    
    def attack(self, enemies, current_time):
        """冰凍塔攻擊"""
        if current_time - self.last_attack_time >= self.attack_speed:
            target = self.find_target(enemies)
            if target:
                self.last_attack_time = current_time
                projectile = self.create_projectile(target)
                if projectile:
                    return [projectile]
        return []
    
    def upgrade(self):
        """升級冰凍塔"""
        if self.level < self.max_level:
            self.level += 1
            
            # 升級效果
            self.damage = int(self.damage * 1.2)
            self.attack_range = int(self.attack_range * 1.15)
            self.attack_speed *= 0.85  # 攻擊間隔縮短
            self.slow_effect = max(0.1, self.slow_effect - 0.05)  # 減速效果增強
            self.slow_duration += 0.5  # 持續時間增加
            self.splash_radius = int(self.splash_radius * 1.1)
            self.cost = int(self.cost * 1.4)
            
            return True
        return False
    
    def get_stats(self):
        """獲取塔的詳細屬性"""
        stats = super().get_stats()
        stats.update({
            'slow_effect': f"{int((1-self.slow_effect)*100)}%",
            'slow_duration': f"{self.slow_duration}秒",
            'splash_radius': self.splash_radius,
            'special': "減速 + 濺射"
        })
        return stats
    
    def get_description(self):
        """獲取塔的描述"""
        return f"冰凍控制塔\n傷害: {self.damage}\n射程: {self.attack_range}\n減速: {int((1-self.slow_effect)*100)}%\n濺射: {self.splash_radius}"
    
    def get_effective_enemies(self, enemies):
        """獲取攻擊範圍內的敵人數量(用於AI評估)"""
        count = 0
        for enemy in enemies:
            if enemy.is_alive() and self.calculate_distance(enemy) <= self.attack_range:
                count += 1
        return count
