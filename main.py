# main.py - 主程式入口
import pygame
import sys
from game.game_manager import GameManager
from utils.constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense Game")
    clock = pygame.time.Clock()
    
    game_manager = GameManager()
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # 轉換為秒
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)
        
        game_manager.update(dt)
        game_manager.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# utils/constants.py - 遊戲常數
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 遊戲設定
TOWER_COST = {
    'cannon': 100,
    'machine': 75,
    'freeze': 150
}

# entities/base_entity.py - 基礎實體類別
from abc import ABC, abstractmethod
import pygame
import math

class BaseEntity(ABC):
    """所有遊戲實體的基礎類別 - 展示封裝概念"""
    
    def __init__(self, x, y, image_path=None):
        self._x = x
        self._y = y
        self._alive = True
        
        if image_path:
            self._image = pygame.image.load(image_path)
            self._rect = self._image.get_rect()
            self._rect.center = (x, y)
        else:
            self._image = None
            self._rect = pygame.Rect(x-10, y-10, 20, 20)
    
    @property
    def position(self):
        """位置屬性 - 封裝內部座標"""
        return (self._x, self._y)
    
    @property
    def alive(self):
        """存活狀態屬性"""
        return self._alive
    
    @property
    def rect(self):
        """碰撞矩形屬性"""
        return self._rect
    
    def distance_to(self, other):
        """計算與另一個實體的距離"""
        dx = self._x - other._x
        dy = self._y - other._y
        return math.sqrt(dx*dx + dy*dy)
    
    @abstractmethod
    def update(self, dt):
        """更新方法 - 子類別必須實作"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """繪製方法 - 子類別必須實作"""
        pass

# entities/tower.py - 塔類別系統
import pygame
from entities.base_entity import BaseEntity
from entities.projectile import CannonBall, Bullet, IceBall
from utils.constants import *

class Tower(BaseEntity):
    """塔的基礎類別 - 展示繼承概念"""
    
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self._damage = 0
        self._range = 0
        self._attack_speed = 0  # 每秒攻擊次數
        self._last_attack_time = 0
        self._target = None
        self._cost = 0
    
    @property
    def range(self):
        return self._range
    
    @property
    def cost(self):
        return self._cost
    
    def find_target(self, enemies):
        """尋找範圍內的敵人"""
        self._target = None
        min_distance = float('inf')
        
        for enemy in enemies:
            if enemy.alive:
                distance = self.distance_to(enemy)
                if distance <= self._range and distance < min_distance:
                    self._target = enemy
                    min_distance = distance
    
    def can_attack(self, current_time):
        """檢查是否可以攻擊"""
        return (current_time - self._last_attack_time) >= (1.0 / self._attack_speed)
    
    def attack(self, current_time):
        """攻擊目標 - 返回投射物"""
        if self._target and self._target.alive and self.can_attack(current_time):
            self._last_attack_time = current_time
            return self.create_projectile()
        return None
    
    @abstractmethod
    def create_projectile(self):
        """創建投射物 - 多型的應用點"""
        pass
    
    def update(self, dt):
        """更新塔的狀態"""
        pass
    
    def draw(self, screen):
        """繪製塔"""
        if self._image:
            screen.blit(self._image, self._rect)
        else:
            pygame.draw.circle(screen, BLUE, (int(self._x), int(self._y)), 15)
        
        # 繪製射程範圍（當選中時）
        # pygame.draw.circle(screen, (255, 255, 255, 50), (int(self._x), int(self._y)), int(self._range), 2)

class CannonTower(Tower):
    """砲塔 - 高傷害，慢攻速"""
    
    def __init__(self, x, y):
        super().__init__(x, y, None)  # 暫時不使用圖片
        self._damage = 100
        self._range = 120
        self._attack_speed = 0.5  # 每秒0.5次攻擊
        self._cost = TOWER_COST['cannon']
    
    def create_projectile(self):
        """創建砲彈 - 多型實作"""
        if self._target:
            return CannonBall(self._x, self._y, self._target, self._damage)
        return None
    
    def draw(self, screen):
        """砲塔的特殊繪製"""
        pygame.draw.circle(screen, RED, (int(self._x), int(self._y)), 20)
        pygame.draw.circle(screen, BLACK, (int(self._x), int(self._y)), 20, 3)

class MachineTower(Tower):
    """機槍塔 - 快攻速，低傷害"""
    
    def __init__(self, x, y):
        super().__init__(x, y, None)
        self._damage = 25
        self._range = 100
        self._attack_speed = 3.0  # 每秒3次攻擊
        self._cost = TOWER_COST['machine']
    
    def create_projectile(self):
        """創建子彈 - 多型實作"""
        if self._target:
            return Bullet(self._x, self._y, self._target, self._damage)
        return None
    
    def draw(self, screen):
        """機槍塔的特殊繪製"""
        pygame.draw.rect(screen, GREEN, (int(self._x-15), int(self._y-15), 30, 30))
        pygame.draw.rect(screen, BLACK, (int(self._x-15), int(self._y-15), 30, 30), 3)

class FreezeTower(Tower):
    """冰凍塔 - 減速效果"""
    
    def __init__(self, x, y):
        super().__init__(x, y, None)
        self._damage = 30
        self._range = 90
        self._attack_speed = 1.5  # 每秒1.5次攻擊
        self._cost = TOWER_COST['freeze']
    
    def create_projectile(self):
        """創建冰球 - 多型實作"""
        if self._target:
            return IceBall(self._x, self._y, self._target, self._damage)
        return None
    
    def draw(self, screen):
        """冰凍塔的特殊繪製"""
        pygame.draw.circle(screen, (0, 200, 255), (int(self._x), int(self._y)), 18)
        pygame.draw.circle(screen, BLACK, (int(self._x), int(self._y)), 18, 3)

# entities/enemy.py - 敵人類別系統
import pygame
from entities.base_entity import BaseEntity
from utils.constants import *

class Enemy(BaseEntity):
    """敵人的基礎類別"""
    
    def __init__(self, x, y, image_path=None):
        super().__init__(x, y, image_path)
        self._hp = 0
        self._max_hp = 0
        self._speed = 0
        self._path_index = 0
        self._reward = 0
        self._slow_effect = 1.0  # 減速效果倍率
        self._slow_duration = 0  # 減速持續時間
    
    @property
    def hp(self):
        return self._hp
    
    @property
    def max_hp(self):
        return self._max_hp
    
    @property
    def reward(self):
        return self._reward
    
    def take_damage(self, damage):
        """受到傷害"""
        self._hp -= damage
        if self._hp <= 0:
            self._alive = False
    
    def apply_slow(self, slow_factor, duration):
        """應用減速效果"""
        self._slow_effect = min(self._slow_effect, slow_factor)
        self._slow_duration = max(self._slow_duration, duration)
    
    def move_along_path(self, path, dt):
        """沿路徑移動"""
        if self._path_index >= len(path) - 1:
            self._alive = False  # 到達終點
            return
        
        # 更新減速效果
        if self._slow_duration > 0:
            self._slow_duration -= dt
        else:
            self._slow_effect = 1.0
        
        # 計算移動
        current_speed = self._speed * self._slow_effect
        target = path[self._path_index + 1]
        
        dx = target[0] - self._x
        dy = target[1] - self._y
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance < 5:  # 接近路徑點
            self._path_index += 1
        else:
            # 移動向目標
            move_distance = current_speed * dt
            self._x += (dx / distance) * move_distance
            self._y += (dy / distance) * move_distance
            self._rect.center = (self._x, self._y)
    
    @abstractmethod
    def get_special_ability(self):
        """獲取特殊能力 - 多型應用"""
        pass
    
    def update(self, dt):
        """更新敵人狀態"""
        pass
    
    def draw(self, screen):
        """繪製敵人和血條"""
        if self._image:
            screen.blit(self._image, self._rect)
        else:
            color = self.get_color()
            pygame.draw.circle(screen, color, (int(self._x), int(self._y)), 12)
        
        # 繪製血條
        bar_width = 30
        bar_height = 5
        bar_x = self._x - bar_width // 2
        bar_y = self._y - 20
        
        # 背景
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # 血量
        hp_ratio = self._hp / self._max_hp
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * hp_ratio, bar_height))
    
    @abstractmethod
    def get_color(self):
        """獲取敵人顏色"""
        pass

class BasicEnemy(Enemy):
    """基礎敵人"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self._hp = 100
        self._max_hp = 100
        self._speed = 50  # 像素/秒
        self._reward = 10
    
    def get_special_ability(self):
        return None  # 無特殊能力
    
    def get_color(self):
        return (255, 100, 100)  # 淺紅色

class FastEnemy(Enemy):
    """快速敵人"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self._hp = 60
        self._max_hp = 60
        self._speed = 100  # 像素/秒
        self._reward = 15
    
    def get_special_ability(self):
        return "speed_boost"
    
    def get_color(self):
        return (255, 255, 100)  # 黃色

class TankEnemy(Enemy):
    """坦克敵人"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self._hp = 300
        self._max_hp = 300
        self._speed = 25  # 像素/秒
        self._reward = 30
    
    def get_special_ability(self):
        return "high_defense"
    
    def get_color(self):
        return (100, 100, 100)  # 灰色
    
    def take_damage(self, damage):
        """坦克有護甲，減少傷害"""
        reduced_damage = damage * 0.7  # 減少30%傷害
        super().take_damage(reduced_damage)

# entities/projectile.py - 投射物系統
import pygame
import math
from entities.base_entity import BaseEntity

class Projectile(BaseEntity):
    """投射物基礎類別"""
    
    def __init__(self, x, y, target, damage):
        super().__init__(x, y)
        self._target = target
        self._damage = damage
        self._speed = 200  # 像素/秒
        
        # 計算方向
        if target:
            dx = target._x - x
            dy = target._y - y
            distance = math.sqrt(dx*dx + dy*dy)
            self._dx = dx / distance if distance > 0 else 0
            self._dy = dy / distance if distance > 0 else 0
        else:
            self._dx = self._dy = 0
    
    def update(self, dt):
        """更新投射物位置"""
        self._x += self._dx * self._speed * dt
        self._y += self._dy * self._speed * dt
        self._rect.center = (self._x, self._y)
        
        # 檢查是否擊中目標或超出螢幕
        if self._target and self._target.alive:
            if self.distance_to(self._target) < 15:
                self.hit_target()
        
        # 超出螢幕範圍就消失
        if (self._x < -10 or self._x > 1034 or 
            self._y < -10 or self._y > 778):
            self._alive = False
    
    @abstractmethod
    def hit_target(self):
        """擊中目標的效果"""
        pass
    
    def draw(self, screen):
        """繪製投射物"""
        color = self.get_color()
        pygame.draw.circle(screen, color, (int(self._x), int(self._y)), self.get_size())
    
    @abstractmethod
    def get_color(self):
        pass
    
    @abstractmethod
    def get_size(self):
        pass

class CannonBall(Projectile):
    """砲彈"""
    
    def __init__(self, x, y, target, damage):
        super().__init__(x, y, target, damage)
        self._speed = 150
    
    def hit_target(self):
        """砲彈擊中效果"""
        if self._target:
            self._target.take_damage(self._damage)
            self._alive = False
    
    def get_color(self):
        return (100, 100, 100)  # 灰色
    
    def get_size(self):
        return 6

class Bullet(Projectile):
    """子彈"""
    
    def __init__(self, x, y, target, damage):
        super().__init__(x, y, target, damage)
        self._speed = 300
    
    def hit_target(self):
        """子彈擊中效果"""
        if self._target:
            self._target.take_damage(self._damage)
            self._alive = False
    
    def get_color(self):
        return (255, 255, 0)  # 黃色
    
    def get_size(self):
        return 3

class IceBall(Projectile):
    """冰球"""
    
    def __init__(self, x, y, target, damage):
        super().__init__(x, y, target, damage)
        self._speed = 180
    
    def hit_target(self):
        """冰球擊中效果 - 造成傷害並減速"""
        if self._target:
            self._target.take_damage(self._damage)
            self._target.apply_slow(0.5, 2.0)  # 減速50%，持續2秒
            self._alive = False
    
    def get_color(self):
        return (0, 200, 255)  # 冰藍色
    
    def get_size(self):
        return 5
