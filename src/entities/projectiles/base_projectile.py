"""
投射物基礎類別 - 所有投射物的基類
"""
import math
from ...utils.constants import ProjectileType


class BaseProjectile:
    """投射物基礎類別"""
    
    def __init__(self, x, y, target, damage, speed=200):
        # 基本位置和目標
        self.x = float(x)
        self.y = float(y)
        self.start_x = x
        self.start_y = y
        self.target = target
        self.damage = damage
        self.speed = speed
        
        # 運動相關
        self.velocity_x = 0
        self.velocity_y = 0
        self.rotation = 0  # 旋轉角度
        
        # 狀態
        self.active = True
        self.hit_target = False
        
        # 視覺屬性
        self.width = 8
        self.height = 8
        self.color = (255, 255, 0)  # 默認黃色
        
        # 投射物類型
        self.projectile_type = ProjectileType.BASIC
        
        # 生命週期
        self.max_lifetime = 5.0  # 最大存在時間(秒)
        self.lifetime = 0
        
        # 計算初始方向
        if target:
            self.update_direction()
    
    def update_direction(self):
        """更新投射物飛行方向"""
        if self.target and self.target.is_alive():
            # 預測目標位置(提前量)
            target_x, target_y = self.predict_target_position()
            
            # 計算方向向量
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # 標準化方向向量
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * self.speed
                
                # 計算旋轉角度
                self.rotation = math.atan2(dy, dx)
    
    def predict_target_position(self):
        """預測目標未來位置"""
        if not self.target or not self.target.is_alive():
            return self.x, self.y
        
        # 簡單的線性預測
        target_speed = getattr(self.target, 'speed', 0)
        if target_speed > 0:
            # 計算到達目標需要的時間
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            time_to_target = distance / self.speed
            
            # 預測目標移動
            if hasattr(self.target, 'velocity_x') and hasattr(self.target, 'velocity_y'):
                pred_x = self.target.x + self.target.velocity_x * time_to_target
                pred_y = self.target.y + self.target.velocity_y * time_to_target
                return pred_x, pred_y
        
        return self.target.x + self.target.width//2, self.target.y + self.target.height//2
    
    def update(self, dt, enemies):
        """更新投射物狀態"""
        if not self.active:
            return
        
        # 更新生命週期
        self.lifetime += dt
        if self.lifetime >= self.max_lifetime:
            self.active = False
            return
        
        # 更新位置
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # 檢查碰撞
        self.check_collision(enemies)
        
        # 檢查邊界
        self.check_bounds()
    
    def check_collision(self, enemies):
        """檢查與敵人的碰撞"""
        if not self.active or self.hit_target:
            return
        
        for enemy in enemies:
            if enemy.is_alive() and self.collides_with(enemy):
                self.on_hit(enemy)
                break
    
    def collides_with(self, enemy):
        """檢查是否與敵人碰撞"""
        # 簡單的矩形碰撞檢測
        return (self.x < enemy.x + enemy.width and
                self.x + self.width > enemy.x and
                self.y < enemy.y + enemy.height and
                self.y + self.height > enemy.y)
    
    def on_hit(self, enemy):
        """命中敵人時的處理"""
        if enemy and enemy.is_alive():
            # 造成傷害
            actual_damage = enemy.take_damage(self.damage, self.get_damage_type())
            
            # 觸發命中效果
            self.on_hit_effect(enemy, actual_damage)
        
        # 標記為已命中
        self.hit_target = True
        self.active = False
    
    def get_damage_type(self):
        """獲取傷害類型"""
        return "physical"  # 默認物理傷害
    
    def on_hit_effect(self, enemy, damage):
        """命中效果(子類可重寫)"""
        pass
    
    def check_bounds(self):
        """檢查邊界(超出屏幕範圍則消失)"""
        # 假設遊戲區域大小，實際應該從配置獲取
        screen_width = 1200
        screen_height = 800
        
        if (self.x < -50 or self.x > screen_width + 50 or 
            self.y < -50 or self.y > screen_height + 50):
            self.active = False
    
    def get_distance_to_target(self):
        """獲取到目標的距離"""
        if not self.target or not self.target.is_alive():
            return float('inf')
        
        dx = self.target.x + self.target.width//2 - self.x
        dy = self.target.y + self.target.height//2 - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def is_active(self):
        """檢查投射物是否仍然活躍"""
        return self.active and not self.hit_target
    
    def get_render_info(self):
        """獲取渲染信息"""
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': self.color,
            'rotation': self.rotation
        }
    
    def get_stats(self):
        """獲取投射物統計信息"""
        return {
            'type': self.projectile_type,
            'damage': self.damage,
            'speed': self.speed,
            'lifetime': f"{self.lifetime:.1f}s",
            'active': self.active,
            'distance_traveled': self.get_distance_traveled()
        }
    
    def get_distance_traveled(self):
        """獲取已飛行距離"""
        dx = self.x - self.start_x
        dy = self.y - self.start_y
        return math.sqrt(dx*dx + dy*dy)
