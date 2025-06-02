"""
炮彈投射物類別 - 具有濺射傷害的投射物
"""
import math
from .base_projectile import BaseProjectile
from ...utils.constants import ProjectileType


class CannonBall(BaseProjectile):
    """炮彈投射物 - 爆炸濺射傷害"""
    
    def __init__(self, x, y, target, damage, splash_radius=60):
        super().__init__(x, y, target, damage, speed=150)
        
        self.projectile_type = ProjectileType.CANNON_BALL
        
        # 炮彈特殊屬性
        self.splash_radius = splash_radius
        self.splash_damage_ratio = 0.6  # 濺射傷害為直接傷害的60%
        
        # 視覺屬性
        self.width = 12
        self.height = 12
        self.color = (64, 64, 64)  # 深灰色
        
        # 軌跡效果
        self.trail_positions = []  # 軌跡點
        self.max_trail_length = 5
        
        # 爆炸效果
        self.explosion_duration = 0.3
        self.explosion_radius_growth = 100  # 爆炸半徑增長速度
        
    def update(self, dt, enemies):
        """更新炮彈狀態"""
        if not self.active:
            return
        
        # 記錄軌跡
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        # 調用基類更新
        super().update(dt, enemies)
    
    def on_hit(self, enemy):
        """命中時處理濺射傷害"""
        hit_x = self.x
        hit_y = self.y
        
        if enemy:
            # 以被命中的敵人為中心
            hit_x = enemy.x + enemy.width // 2
            hit_y = enemy.y + enemy.height // 2
        
        # 記錄爆炸位置
        self.explosion_x = hit_x
        self.explosion_y = hit_y
        
        # 對目標造成全額傷害
        if enemy and enemy.is_alive():
            actual_damage = enemy.take_damage(self.damage, self.get_damage_type())
            self.on_hit_effect(enemy, actual_damage)
        
        self.hit_target = True
        self.active = False
        
        # 返回濺射信息供遊戲管理器處理
        return self.create_splash_damage_info(hit_x, hit_y)
    
    def create_splash_damage_info(self, center_x, center_y):
        """創建濺射傷害信息"""
        return {
            'type': 'splash',
            'x': center_x,
            'y': center_y,
            'radius': self.splash_radius,
            'damage': int(self.damage * self.splash_damage_ratio),
            'damage_type': self.get_damage_type(),
            'exclude_target': self.target  # 排除主要目標(避免雙重傷害)
        }
    
    def check_collision(self, enemies):
        """檢查碰撞(炮彈可以擊中任何敵人)"""
        if not self.active or self.hit_target:
            return
        
        closest_enemy = None
        closest_distance = float('inf')
        
        # 找到最近的敵人
        for enemy in enemies:
            if enemy.is_alive() and self.collides_with(enemy):
                distance = self.get_distance_to_enemy(enemy)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy
        
        if closest_enemy:
            splash_info = self.on_hit(closest_enemy)
            return splash_info
    
    def get_distance_to_enemy(self, enemy):
        """獲取到敵人的距離"""
        enemy_center_x = enemy.x + enemy.width // 2
        enemy_center_y = enemy.y + enemy.height // 2
        dx = enemy_center_x - self.x
        dy = enemy_center_y - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def get_damage_type(self):
        """炮彈造成物理傷害"""
        return "physical"
    
    def on_hit_effect(self, enemy, damage):
        """命中效果 - 震退效果"""
        if hasattr(enemy, 'apply_knockback'):
            # 計算震退方向
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                knockback_force = 30
                knockback_x = (dx / distance) * knockback_force
                knockback_y = (dy / distance) * knockback_force
                enemy.apply_knockback(knockback_x, knockback_y, 0.2)
    
    def apply_splash_damage(self, enemies, center_x, center_y):
        """對範圍內敵人造成濺射傷害"""
        splash_damage = int(self.damage * self.splash_damage_ratio)
        affected_enemies = []
        
        for enemy in enemies:
            if enemy == self.target or not enemy.is_alive():
                continue  # 跳過主要目標和死亡敵人
            
            # 計算距離
            enemy_center_x = enemy.x + enemy.width // 2
            enemy_center_y = enemy.y + enemy.height // 2
            distance = math.sqrt((enemy_center_x - center_x)**2 + (enemy_center_y - center_y)**2)
            
            if distance <= self.splash_radius:
                # 根據距離計算傷害衰減
                damage_multiplier = 1.0 - (distance / self.splash_radius) * 0.5
                final_damage = int(splash_damage * damage_multiplier)
                
                if final_damage > 0:
                    actual_damage = enemy.take_damage(final_damage, self.get_damage_type())
                    affected_enemies.append((enemy, actual_damage))
        
        return affected_enemies
    
    def get_render_info(self):
        """獲取渲染信息(包含軌跡)"""
        info = super().get_render_info()
        info.update({
            'trail_positions': self.trail_positions.copy(),
            'splash_radius': self.splash_radius,
            'has_explosion': hasattr(self, 'explosion_x')
        })
        
        if hasattr(self, 'explosion_x'):
            info.update({
                'explosion_x': self.explosion_x,
                'explosion_y': self.explosion_y,
                'explosion_radius': self.splash_radius
            })
        
        return info
    
    def get_stats(self):
        """獲取炮彈統計信息"""
        stats = super().get_stats()
        stats.update({
            'splash_radius': self.splash_radius,
            'splash_damage': int(self.damage * self.splash_damage_ratio),
            'trail_length': len(self.trail_positions)
        })
        return stats
