"""
冰球投射物類別 - 具有減速和濺射效果的投射物
"""
import math
from .base_projectile import BaseProjectile
from ...utils.constants import ProjectileType


class IceBall(BaseProjectile):
    """冰球投射物 - 造成傷害並施加減速效果"""
    
    def __init__(self, x, y, target, damage, slow_effect=0.5, slow_duration=2.0, splash_radius=50):
        super().__init__(x, y, target, damage, speed=180)
        
        self.projectile_type = ProjectileType.ICE_BALL
        
        # 冰球特殊屬性
        self.slow_effect = slow_effect  # 減速效果(0.5 = 50%速度)
        self.slow_duration = slow_duration  # 減速持續時間
        self.splash_radius = splash_radius  # 濺射半徑
        
        # 視覺屬性
        self.width = 10
        self.height = 10
        self.color = (150, 200, 255)  # 冰藍色
        
        # 冰凍效果
        self.freeze_chance = 0.2  # 20%機率完全冰凍
        self.freeze_duration = 1.0  # 冰凍持續時間
        
        # 軌跡效果
        self.ice_trail = []  # 冰霜軌跡
        self.max_trail_length = 8
        
        # 碎裂效果
        self.shatter_damage_bonus = 1.3  # 對冰凍敵人額外傷害
        
    def update(self, dt, enemies):
        """更新冰球狀態"""
        if not self.active:
            return
        
        # 記錄冰霜軌跡
        self.ice_trail.append((self.x, self.y, self.lifetime))
        if len(self.ice_trail) > self.max_trail_length:
            self.ice_trail.pop(0)
        
        # 調用基類更新
        super().update(dt, enemies)
    
    def on_hit(self, enemy):
        """命中時處理冰凍效果和濺射"""
        hit_x = self.x
        hit_y = self.y
        
        if enemy:
            hit_x = enemy.x + enemy.width // 2
            hit_y = enemy.y + enemy.height // 2
        
        # 記錄冰爆位置
        self.ice_explosion_x = hit_x
        self.ice_explosion_y = hit_y
        
        # 對主要目標造成傷害和效果
        if enemy and enemy.is_alive():
            # 檢查目標是否已被冰凍
            damage_multiplier = 1.0
            if hasattr(enemy, 'is_frozen') and enemy.is_frozen:
                damage_multiplier = self.shatter_damage_bonus
            
            final_damage = int(self.damage * damage_multiplier)
            actual_damage = enemy.take_damage(final_damage, self.get_damage_type())
            
            # 應用冰凍效果
            self.apply_ice_effects(enemy)
            
            self.on_hit_effect(enemy, actual_damage)
        
        self.hit_target = True
        self.active = False
        
        # 返回冰霜濺射信息
        return self.create_ice_splash_info(hit_x, hit_y)
    
    def apply_ice_effects(self, enemy):
        """對敵人應用冰凍效果"""
        import random
        
        # 檢查冰凍機率
        if random.random() < self.freeze_chance:
            # 完全冰凍
            if hasattr(enemy, 'apply_freeze'):
                enemy.apply_freeze(self.freeze_duration)
        else:
            # 減速效果
            if hasattr(enemy, 'apply_slow_effect'):
                enemy.apply_slow_effect(self.slow_effect, self.slow_duration)
    
    def create_ice_splash_info(self, center_x, center_y):
        """創建冰霜濺射信息"""
        return {
            'type': 'ice_splash',
            'x': center_x,
            'y': center_y,
            'radius': self.splash_radius,
            'damage': int(self.damage * 0.4),  # 濺射傷害較低
            'damage_type': self.get_damage_type(),
            'slow_effect': self.slow_effect * 0.7,  # 濺射減速效果較弱
            'slow_duration': self.slow_duration * 0.5,
            'freeze_chance': self.freeze_chance * 0.3,  # 濺射冰凍機率較低
            'exclude_target': self.target
        }
    
    def apply_ice_splash(self, enemies, center_x, center_y):
        """對範圍內敵人造成冰霜濺射"""
        splash_info
