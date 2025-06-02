"""
坦克敵人類別 - 高血量高護甲但速度慢
"""
from .base_enemy import BaseEnemy
from ...utils.constants import EnemyType


class TankEnemy(BaseEnemy):
    """坦克敵人 - 高血量、高護甲、低速度、高獎勵"""
    
    def __init__(self, path, wave_multiplier=1.0):
        # 坦克敵人屬性
        max_health = int(300 * wave_multiplier)  # 高血量
        speed = 30  # 低速度
        reward = int(25 * wave_multiplier)  # 高獎勵
        
        super().__init__(path, max_health, speed, reward)
        
        self.enemy_type = EnemyType.TANK
        self.name = "坦克敵人"
        
        # 外觀屬性
        self.color = (100, 100, 255)  # 藍色
        self.width = 40
        self.height = 40
        
        # 坦克敵人特殊屬性
        self.armor = 50  # 高護甲
        self.magic_resistance = 30  # 中等魔抗
        self.damage_threshold = 20  # 傷害閾值(低於此值的攻擊傷害減半)
        
        # 重生機制
        self.can_regenerate = True
        self.regeneration_rate = max_health * 0.02  # 每秒回復2%最大血量
        self.regeneration_delay = 3.0  # 未受傷3秒後開始回血
        self.last_damage_time = 0
        
        # 死亡爆炸
        self.explosion_damage = int(50 * wave_multiplier)
        self.explosion_radius = 60
        
    def take_damage(self, damage, damage_type="physical"):
        """承受傷害(含護甲和傷害閾值)"""
        self.last_damage_time = getattr(self, '_current_time', 0)
        
        actual_damage = damage
        
        # 傷害閾值機制
        if damage < self.damage_threshold:
            actual_damage = damage * 0.5
        
        # 護甲減免
        if damage_type == "physical":
            damage_reduction = self.armor / (self.armor + 100)
            actual_damage = actual_damage * (1 - damage_reduction)
        # 魔抗減免
        elif damage_type == "magic":
            damage_reduction = self.magic_resistance / (self.magic_resistance + 100)
            actual_damage = actual_damage * (1 - damage_reduction)
        
        # 確保至少造成1點傷害
        actual_damage = max(1, int(actual_damage))
        
        self.current_health -= actual_damage
        self.current_health = max(0, self.current_health)
        
        self.on_damaged(actual_damage)
        
        return actual_damage
    
    def update(self, dt):
        """更新敵人狀態"""
        super().update(dt)
        
        # 更新當前時間
        if not hasattr(self, '_current_time'):
            self._current_time = 0
        self._current_time += dt
        
        # 血量回復機制
        if (self.can_regenerate and 
            self.is_alive() and 
            self.current_health < self.max_health and
            self._current_time - self.last_damage_time >= self.regeneration_delay):
            
            heal_amount = self.regeneration_rate * dt
            self.current_health = min(self.max_health, self.current_health + heal_amount)
        
        # 處理受傷閃爍效果
        if hasattr(self, 'damage_flash_time') and self.damage_flash_time > 0:
            self.damage_flash_time -= dt
    
    def on_death(self):
        """死亡時爆炸"""
        # 返回爆炸信息供遊戲管理器處理
        return {
            'type': 'explosion',
            'x': self.x + self.width // 2,
            'y': self.y + self.height // 2,
            'damage': self.explosion_damage,
            'radius': self.explosion_radius,
            'damage_type': 'magic'
        }
    
    def apply_slow_effect(self, slow_factor, duration):
        """應用減速效果(坦克敵人有減速抗性)"""
        # 減速抗性
        resistance = 0.5  # 50%減速抗性
        actual_slow = slow_factor + (1 - slow_factor) * resistance
        actual_duration = duration * (1 - resistance)
        
        super().apply_slow_effect(actual_slow, actual_duration)
    
    def get_render_color(self):
        """獲取渲染顏色"""
        if hasattr(self, 'damage_flash_time') and self.damage_flash_time > 0:
            return (255, 255, 255)
        
        # 根據血量變色
        health_ratio = self.current_health / self.max_health
        if health_ratio < 0.3:
            # 低血量時變紅
            return (150, 100, 200)
        return self.color
    
    def get_health_bar_color(self):
        """獲取血條顏色"""
        health_ratio = self.current_health / self.max_health
        if health_ratio > 0.7:
            return (0, 255, 0)  # 綠色
        elif health_ratio > 0.4:
            return (255, 255, 0)  # 黃色
        elif health_ratio > 0.2:
            return (255, 150, 0)  # 橙色
        else:
            return (255, 0, 0)  # 紅色
    
    def get_armor_display(self):
        """獲取護甲顯示信息"""
        physical_reduction = int(self.armor / (self.armor + 100) * 100)
        magic_reduction = int(self.magic_resistance / (self.magic_resistance + 100) * 100)
        return f"物理減傷: {physical_reduction}% | 魔法減傷: {magic_reduction}%"
    
    def get_stats(self):
        """獲取敵人統計信息"""
        stats = super().get_stats()
        stats.update({
            'armor': self.armor,
            'magic_resistance': self.magic_resistance,
            'damage_threshold': self.damage_threshold,
            'regeneration': f"{self.regeneration_rate:.1f}/秒",
            'explosion_damage': self.explosion_damage,
            'is_regenerating': (self._current_time - self.last_damage_time >= self.regeneration_delay 
                              and self.current_health < self.max_health)
        })
        return stats
    
    def get_description(self):
        """獲取敵人描述"""
        return f"重裝坦克\n血量: {self.max_health}\n護甲: {self.armor}\n速度: {self.speed}\n死亡爆炸: {self.explosion_damage}\n獎勵: {self.reward}金幣"
    
    def clone(self, wave_multiplier=1.0):
        """複製敵人"""
        return TankEnemy(self.path, wave_multiplier)
