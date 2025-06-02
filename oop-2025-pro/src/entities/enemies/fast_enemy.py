"""
快速敵人類別 - 速度快但血量較低
"""
from .base_enemy import BaseEnemy
from ...utils.constants import EnemyType


class FastEnemy(BaseEnemy):
    """快速敵人 - 高速度、低血量、中等獎勵"""
    
    def __init__(self, path, wave_multiplier=1.0):
        # 快速敵人屬性
        max_health = int(60 * wave_multiplier)  # 較低血量
        speed = 120  # 高速度
        reward = int(15 * wave_multiplier)  # 較高獎勵
        
        super().__init__(path, max_health, speed, reward)
        
        self.enemy_type = EnemyType.FAST
        self.name = "快速敵人"
        
        # 外觀屬性
        self.color = (100, 255, 100)  # 綠色
        self.width = 25
        self.height = 25
        
        # 快速敵人特殊屬性
        self.armor = 0  # 無護甲
        self.magic_resistance = 10  # 少量魔抗
        self.dodge_chance = 0.15  # 15%閃避機率
        self.base_speed = speed  # 記錄基礎速度
        
        # 衝刺技能
        self.sprint_cooldown = 3.0  # 衝刺冷卻時間
        self.sprint_duration = 1.0  # 衝刺持續時間
        self.sprint_speed_multiplier = 2.0  # 衝刺速度倍數
        self.last_sprint_time = 0
        self.is_sprinting = False
        self.sprint_end_time = 0
        
    def take_damage(self, damage, damage_type="physical"):
        """承受傷害(含閃避機制)"""
        import random
        
        # 閃避檢查
        if random.random() < self.dodge_chance:
            self.on_dodge()
            return 0
        
        actual_damage = damage
        
        # 魔法傷害減免
        if damage_type == "magic":
            damage_reduction = self.magic_resistance / (self.magic_resistance + 100)
            actual_damage = damage * (1 - damage_reduction)
        
        actual_damage = max(1, int(actual_damage))
        
        self.current_health -= actual_damage
        self.current_health = max(0, self.current_health)
        
        self.on_damaged(actual_damage)
        
        return actual_damage
    
    def on_dodge(self):
        """閃避成功時的回調"""
        # 可以加入視覺效果或音效
        pass
    
    def on_damaged(self, damage):
        """受傷時觸發衝刺"""
        super().on_damaged(damage)
        
        # 受到傷害時嘗試衝刺
        current_time = getattr(self, '_current_time', 0)
        if (current_time - self.last_sprint_time >= self.sprint_cooldown and 
            not self.is_sprinting):
            self.start_sprint(current_time)
    
    def start_sprint(self, current_time):
        """開始衝刺"""
        self.is_sprinting = True
        self.sprint_end_time = current_time + self.sprint_duration
        self.last_sprint_time = current_time
        self.speed = self.base_speed * self.sprint_speed_multiplier
    
    def update(self, dt):
        """更新敵人狀態"""
        super().update(dt)
        
        # 更新當前時間(用於衝刺計算)
        if not hasattr(self, '_current_time'):
            self._current_time = 0
        self._current_time += dt
        
        # 檢查衝刺結束
        if self.is_sprinting and self._current_time >= self.sprint_end_time:
            self.end_sprint()
        
        # 處理受傷閃爍效果
        if hasattr(self, 'damage_flash_time') and self.damage_flash_time > 0:
            self.damage_flash_time -= dt
    
    def end_sprint(self):
        """結束衝刺"""
        self.is_sprinting = False
        self.speed = self.base_speed
    
    def apply_slow_effect(self, slow_factor, duration):
        """應用減速效果(快速敵人抗性較高)"""
        # 減速抗性
        resistance = 0.3  # 30%減速抗性
        actual_slow = slow_factor + (1 - slow_factor) * resistance
        actual_duration = duration * (1 - resistance)
        
        super().apply_slow_effect(actual_slow, actual_duration)
    
    def get_render_color(self):
        """獲取渲染顏色"""
        if self.is_sprinting:
            # 衝刺時發光效果
            return (150, 255, 150)
        elif hasattr(self, 'damage_flash_time') and self.damage_flash_time > 0:
            return (255, 255, 255)
        return self.color
    
    def get_stats(self):
        """獲取敵人統計信息"""
        stats = super().get_stats()
        stats.update({
            'dodge_chance': f"{self.dodge_chance*100:.1f}%",
            'sprint_ready': self._current_time - self.last_sprint_time >= self.sprint_cooldown,
            'is_sprinting': self.is_sprinting,
            'magic_resistance': self.magic_resistance
        })
        return stats
    
    def get_description(self):
        """獲取敵人描述"""
        return f"快速敵人\n血量: {self.max_health}\n速度: {self.base_speed}\n閃避: {self.dodge_chance*100:.0f}%\n獎勵: {self.reward}金幣"
    
    def clone(self, wave_multiplier=1.0):
        """複製敵人"""
        return FastEnemy(self.path, wave_multiplier)
