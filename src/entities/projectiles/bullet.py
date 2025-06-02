"""
子彈投射物類別 - 高速直線攻擊投射物
"""
import math
from .base_projectile import BaseProjectile
from ...utils.constants import ProjectileType


class Bullet(BaseProjectile):
    """子彈投射物 - 高速、精確、單體傷害"""
    
    def __init__(self, x, y, target, damage):
        super().__init__(x, y, target, damage, speed=400)  # 高速
        
        self.projectile_type = ProjectileType.BULLET
        
        # 子彈特殊屬性
        self.accuracy = 0.95  # 命中率
        self.critical_chance = 0.1  # 暴擊機率
        self.critical_multiplier = 1.5  # 暴擊倍數
        
        # 視覺屬性
        self.width = 6
        self.height = 6
        self.color = (255, 255, 100)  # 黃色
        
        # 穿透能力
        self.penetration = 1  # 可穿透敵人數量
        self.penetrated_enemies = set()  # 已穿透的敵人
        
        # 軌跡效果
        self.muzzle_flash = True
        self.tracer_effect = True
        
    def update(self, dt, enemies):
        """更新子彈狀態"""
        if not self.active:
            return
        
        # 高速子彈需要更頻繁的碰撞檢測
        steps = max(1, int(self.speed * dt / 10))  # 分步檢測
        step_dt = dt / steps
        
        for _ in range(steps):
            if not self.active:
                break
            
            # 更新位置
            self.x += self.velocity_x * step_dt
            self.y += self.velocity_y * step_dt
            
            # 檢查碰撞
            self.check_collision(enemies)
        
        # 更新生命週期
        self.lifetime += dt
        if self.lifetime >= self.max_lifetime:
            self.active = False
        
        # 檢查邊界
        self.check_bounds()
    
    def check_collision(self, enemies):
        """檢查碰撞(支持穿透)"""
        if not self.active:
            return
        
        for enemy in enemies:
            if (enemy.is_alive() and 
                enemy.id not in self.penetrated_enemies and 
                self.collides_with(enemy)):
                
                # 命中率檢查
                import random
                if random.random() > self.accuracy:
                    continue  # 未命中
                
                # 計算傷害
                final_damage = self.calculate_damage()
                
                # 造成傷害
                actual_damage = enemy.take_damage(final_damage, self.get_damage_type())
                
                # 記錄穿透
                self.penetrated_enemies.add(enemy.id)
                
                # 觸發命中效果
                self.on_hit_effect(enemy, actual_damage)
                
                # 檢查是否還能穿透
                if len(self.penetrated_enemies) >= self.penetration:
                    self.active = False
                    break
                else:
                    # 穿透後稍微減速
                    self.speed *= 0.9
                    self.damage = int(self.damage * 0.8)  # 穿透後傷害遞減
    
    def calculate_damage(self):
        """計算傷害(含暴擊)"""
        import random
        
        base_damage = self.damage
        
        # 暴擊檢查
        if random.random() < self.critical_chance:
            base_damage = int(base_damage * self.critical_multiplier)
            self.last_was_critical = True
        else:
            self.last_was_critical = False
        
        return base_damage
    
    def get_damage_type(self):
        """子彈造成物理傷害"""
        return "physical"
    
    def on_hit_effect(self, enemy, damage):
        """命中效果"""
        # 記錄命中信息
        self.last_hit_enemy = enemy
        self.last_hit_damage = damage
        
        # 如果是暴擊，可以添加特殊效果
        if getattr(self, 'last_was_critical', False):
            # 暴擊效果：短暫眩暈
            if hasattr(enemy, 'apply_stun'):
                enemy.apply_stun(0.1)  # 0.1秒眩暈
    
    def collides_with(self, enemy):
        """精確碰撞檢測"""
        # 使用圓形碰撞檢測（更適合子彈）
        bullet_center_x = self.x + self.width // 2
        bullet_center_y = self.y + self.height // 2
        enemy_center_x = enemy.x + enemy.width // 2
        enemy_center_y = enemy.y + enemy.height // 2
        
        distance = math.sqrt((bullet_center_x - enemy_center_x)**2 + 
                           (bullet_center_y - enemy_center_y)**2)
        
        collision_radius = (min(self.width, self.height) + min(enemy.width, enemy.height)) // 2
        
        return distance <= collision_radius
    
    def predict_target_position(self):
        """高精度目標預測"""
        if not self.target or not self.target.is_alive():
            return self.x, self.y
        
        # 考慮目標的加速度和轉向
        target_speed = getattr(self.target, 'speed', 0)
        if target_speed > 0:
            # 計算攔截點
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # 考慮相對速度
            if hasattr(self.target, 'velocity_x') and hasattr(self.target, 'velocity_y'):
                target_vx = self.target.velocity_x
                target_vy = self.target.velocity_y
                
                # 計算攔截時間
                a = target_vx*target_vx + target_vy*target_vy - self.speed*self.speed
                b = 2 * (dx*target_vx + dy*target_vy)
                c = dx*dx + dy*dy
                
                if a != 0:
                    discriminant = b*b - 4*a*c
                    if discriminant >= 0:
                        t1 = (-b + math.sqrt(discriminant)) / (2*a)
                        t2 = (-b - math.sqrt(discriminant)) / (2*a)
                        t = min(t1, t2) if t1 > 0 and t2 > 0 else max(t1, t2)
                        
                        if t > 0:
                            pred_x = self.target.x + target_vx * t
                            pred_y = self.target.y + target_vy * t
                            return pred_x, pred_y
        
        return self.target.x + self.target.width//2, self.target.y + self.target.height//2
    
    def get_render_info(self):
        """獲取渲染信息"""
        info = super().get_render_info()
        info.update({
            'muzzle_flash': self.muzzle_flash and self.lifetime < 0.05,
            'tracer_effect': self.tracer_effect,
            'penetration_count': len(self.penetrated_enemies),
            'max_penetration': self.penetration,
            'critical_hit': getattr(self, 'last_was_critical', False)
        })
        return info
    
    def get_stats(self):
        """獲取子彈統計信息"""
        stats = super().get_stats()
        stats.update({
            'accuracy': f"{self.accuracy*100:.1f}%",
            'critical_chance': f"{self.critical_chance*100:.1f}%",
            'critical_multiplier': f"{self.critical_multiplier}x",
            'penetration': f"{len(self.penetrated_enemies)}/{self.penetration}",
            'speed_current': f"{self.speed:.0f}"
        })
        return stats
