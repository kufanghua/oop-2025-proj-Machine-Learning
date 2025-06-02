"""
基礎敵人類別 - 最基本的敵人單位
"""
from .base_enemy import BaseEnemy
from ...utils.constants import EnemyType


class BasicEnemy(BaseEnemy):
    """基礎敵人 - 平衡的血量、速度和獎勵"""
    
    def __init__(self, path, wave_multiplier=1.0):
        # 基礎敵人屬性
        max_health = int(100 * wave_multiplier)
        speed = 60  # 像素/秒
        reward = int(10 * wave_multiplier)
        
        super().__init__(path, max_health, speed, reward)
        
        self.enemy_type = EnemyType.BASIC
        self.name = "基礎敵人"
        
        # 外觀屬性
        self.color = (255, 100, 100)  # 紅色
        self.width = 30
        self.height = 30
        
        # 基礎敵人特殊屬性
        self.armor = 0  # 無護甲
        self.magic_resistance = 0  # 無魔抗
        
    def take_damage(self, damage, damage_type="physical"):
        """承受傷害"""
        actual_damage = damage
        
        # 物理傷害計算(護甲減免)
        if damage_type == "physical":
            damage_reduction = self.armor / (self.armor + 100)
            actual_damage = damage * (1 - damage_reduction)
        # 魔法傷害計算(魔抗減免)
        elif damage_type == "magic":
            damage_reduction = self.magic_resistance / (self.magic_resistance + 100)
            actual_damage = damage * (1 - damage_reduction)
        
        # 確保至少造成1點傷害
        actual_damage = max(1, int(actual_damage))
        
        self.current_health -= actual_damage
        self.current_health = max(0, self.current_health)
        
        # 觸發受傷效果
        self.on_damaged(actual_damage)
        
        return actual_damage
    
    def on_damaged(self, damage):
        """受傷時的回調函數"""
        # 基礎敵人受到傷害時變色
        self.damage_flash_time = 0.2  # 受傷閃爍時間
        
    def update(self, dt):
        """更新敵人狀態"""
        super().update(dt)
        
        # 處理受傷閃爍效果
        if hasattr(self, 'damage_flash_time') and self.damage_flash_time > 0:
            self.damage_flash_time -= dt
    
    def get_render_color(self):
        """獲取渲染顏色(含受傷效果)"""
        if hasattr(self, 'damage_flash_time') and self.damage_flash_time > 0:
            # 受傷時閃白色
            return (255, 255, 255)
        return self.color
    
    def get_health_bar_color(self):
        """獲取血條顏色"""
        health_ratio = self.current_health / self.max_health
        if health_ratio > 0.6:
            return (0, 255, 0)  # 綠色
        elif health_ratio > 0.3:
            return (255, 255, 0)  # 黃色
        else:
            return (255, 0, 0)  # 紅色
    
    def on_death(self):
        """死亡時的回調函數"""
        # 基礎敵人死亡無特殊效果
        pass
    
    def get_stats(self):
        """獲取敵人統計信息"""
        return {
            'name': self.name,
            'type': self.enemy_type,
            'max_health': self.max_health,
            'current_health': self.current_health,
            'speed': self.speed,
            'reward': self.reward,
            'armor': self.armor,
            'magic_resistance': self.magic_resistance,
            'progress': f"{self.progress:.1%}"
        }
    
    def get_description(self):
        """獲取敵人描述"""
        return f"基礎敵人\n血量: {self.max_health}\n速度: {self.speed}\n獎勵: {self.reward}金幣"
    
    def clone(self, wave_multiplier=1.0):
        """複製敵人(用於波次生成)"""
        return BasicEnemy(self.path, wave_multiplier)
