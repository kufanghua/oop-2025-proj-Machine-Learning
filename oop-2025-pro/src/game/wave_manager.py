"""
波數管理模組
負責管理遊戲的波數系統、敵人生成時機和難度調整
"""

import random
from typing import List, Dict, Optional, Any
from enum import Enum
from ..entities.enemies.base_enemy import BaseEnemy
from ..utils.constants import WAVE_CONFIG


class WaveState(Enum):
    """波數狀態枚舉"""
    WAITING = "waiting"        # 等待開始
    SPAWNING = "spawning"      # 正在生成敵人
    ACTIVE = "active"          # 波數進行中
    COMPLETED = "completed"    # 波數完成
    PREPARING = "preparing"    # 準備下一波


class EnemySpawnInfo:
    """敵人生成資訊類別"""
    
    def __init__(self, enemy_type: str, count: int, spawn_interval: float, delay: float = 0):
        """
        初始化敵人生成資訊
        
        Args:
            enemy_type (str): 敵人類型
            count (int): 生成數量
            spawn_interval (float): 生成間隔（秒）
            delay (float): 延遲生成時間（秒）
        """
        self.enemy_type = enemy_type
        self.count = count
        self.spawn_interval = spawn_interval
        self.delay = delay
        self.spawned_count = 0
        self.last_spawn_time = 0
        self.start_time = 0


class Wave:
    """波數類別"""
    
    def __init__(self, wave_number: int, enemy_spawns: List[EnemySpawnInfo], 
                 preparation_time: float = 10.0, reward_multiplier: float = 1.0):
        """
        初始化波數
        
        Args:
            wave_number (int): 波數編號
            enemy_spawns (List[EnemySpawnInfo]): 敵人生成資訊列表
            preparation_time (float): 準備時間（秒）
            reward_multiplier (float): 獎勵倍數
        """
        self.wave_number = wave_number
        self.enemy_spawns = enemy_spawns
        self.preparation_time = preparation_time
        self.reward_multiplier = reward_multiplier
        self.state = WaveState.WAITING
        self.start_time = 0
    
    def get_total_enemies(self) -> int:
        """獲取總敵人數量"""
        return sum(spawn.count for spawn in self.enemy_spawns)
    
    def get_spawned_enemies(self) -> int:
        """獲取已生成敵人數量"""
        return sum(spawn.spawned_count for spawn in self.enemy_spawns)
    
    def is_spawn_complete(self) -> bool:
        """檢查是否完成生成所有敵人"""
        return self.get_spawned_enemies() >= self.get_total_enemies()


class WaveManager:
    """
    波數管理器類別
    負責控制遊戲波數的進程、敵人生成和難度調整
    """
    
    def __init__(self):
        """初始化波數管理器"""
        self.current_wave = 0
        self.waves: List[Wave] = []
        self.wave_state = WaveState.WAITING
        self.current_time = 0
        self.preparation_start_time = 0
        self.enemies_to_spawn: List[BaseEnemy] = []
        
        # 難度設定
        self.base_enemy_health_multiplier = 1.0
        self.base_enemy_speed_multiplier = 1.0
        self.base_enemy_reward_multiplier = 1.0
        
        # 自動開始設定
        self.auto_start_waves = WAVE_CONFIG.get('AUTO_START', True)
        self.wave_clear_bonus = WAVE_CONFIG.get('WAVE_CLEAR_BONUS', 50)
        
        # 生成波數數據
        self._generate_waves()
    
    def _generate_waves(self) -> None:
        """生成所有波數數據"""
        # 預設生成30波
        total_waves = WAVE_CONFIG.get('TOTAL_WAVES', 30)
        
        for wave_num in range(1, total_waves + 1):
            enemy_spawns = self._create_enemy_spawns_for_wave(wave_num)
            preparation_time = max(5.0, 15.0 - wave_num * 0.2)  # 準備時間遞減
            reward_multiplier = 1.0 + (wave_num - 1) * 0.1  # 獎勵遞增
            
            wave = Wave(wave_num, enemy_spawns, preparation_time, reward_multiplier)
            self.waves.append(wave)
    
    def _create_enemy_spawns_for_wave(self, wave_number: int) -> List[EnemySpawnInfo]:
        """
        為指定波數創建敵人生成資訊
        
        Args:
            wave_number (int): 波數編號
            
        Returns:
            List[EnemySpawnInfo]: 敵人生成資訊列表
        """
        spawns = []
        
        # 基礎敵人數量隨波數增加
        basic_count = min(5 + wave_number * 2, 25)
        fast_count = max(0, wave_number - 3) * 2
        tank_count = max(0, (wave_number - 5) // 2)
        
        # 生成間隔隨波數減少（敵人生成更快）
        basic_interval = max(0.8, 2.0 - wave_number * 0.05)
        fast_interval = max(0.6, 1.5 - wave_number * 0.03)
        tank_interval = max(1.2, 3.0 - wave_number * 0.08)
        
        # 基礎敵人
        if basic_count > 0:
            spawns.append(EnemySpawnInfo("basic", basic_count, basic_interval, 0))
        
        # 快速敵人（從第4波開始）
        if fast_count > 0 and wave_number >= 4:
            spawns.append(EnemySpawnInfo("fast", fast_count, fast_interval, 3.0))
        
        # 坦克敵人（從第6波開始）
        if tank_count > 0 and wave_number >= 6:
            spawns.append(EnemySpawnInfo("tank", tank_count, tank_interval, 8.0))
        
        # Boss波數（每10波一次）
        if wave_number % 10 == 0:
            boss_count = wave_number // 10
            spawns.append(EnemySpawnInfo("tank", boss_count * 2, 2.0, 10.0))
        
        # 特殊波數變化
        if wave_number % 5 == 0:  # 每5波增加混合敵人
            mixed_basic = basic_count // 2
            mixed_fast = fast_count // 2 if fast_count > 0 else 1
            
            spawns.append(EnemySpawnInfo("basic", mixed_basic, 0.5, 15.0))
            if wave_number >= 4:
                spawns.append(EnemySpawnInfo("fast", mixed_fast, 0.8, 15.5))
        
        return spawns
    
    def update(self, dt: float) -> None:
        """
        更新波數管理器
        
        Args:
            dt (float): 時間差值（秒）
        """
        self.current_time += dt
        
        if self.wave_state == WaveState.WAITING:
            # 等待開始第一波或手動開始
            pass
        
        elif self.wave_state == WaveState.PREPARING:
            # 準備階段
            if self.current_time - self.preparation_start_time >= self.get_current_wave().preparation_time:
                self._start_current_wave()
        
        elif self.wave_state == WaveState.SPAWNING or self.wave_state == WaveState.ACTIVE:
            # 生成敵人
            self._update_enemy_spawning(dt)
            
            # 檢查是否完成生成
            current_wave = self.get_current_wave()
            if current_wave and current_wave.is_spawn_complete():
                if self.wave_state == WaveState.SPAWNING:
                    self.wave_state = WaveState.ACTIVE
    
    def _update_enemy_spawning(self, dt: float) -> None:
        """更新敵人生成邏輯"""
        current_wave = self.get_current_wave()
        if not current_wave:
            return
        
        for spawn_info in current_wave.enemy_spawns:
            if spawn_info.spawned_count >= spawn_info.count:
                continue
            
            # 檢查延遲時間
            wave_elapsed_time = self.current_time - current_wave.start_time
            if wave_elapsed_time < spawn_info.delay:
                continue
            
            # 檢查生成間隔
            if spawn_info.start_time == 0:
                spawn_info.start_time = self.current_time
                spawn_info.last_spawn_time = self.current_time
            
            if self.current_time - spawn_info.last_spawn_time >= spawn_info.spawn_interval:
                # 生成敵人
                enemy = self._create_enemy(spawn_info.enemy_type, current_wave.wave_number)
                if enemy:
                    self.enemies_to_spawn.append(enemy)
                    spawn_info.spawned_count += 1
                    spawn_info.last_spawn_time = self.current_time
    
    def _create_enemy(self, enemy_type: str, wave_number: int) -> Optional[BaseEnemy]:
        """
        創建敵人實例
        
        Args:
            enemy_type (str): 敵人類型
            wave_number (int): 當前波數
            
        Returns:
            Optional[BaseEnemy]: 創建的敵人實例
        """
        try:
            from ..entities.enemies.basic_enemy import BasicEnemy
            from ..entities.enemies.fast_enemy import FastEnemy
            from ..entities.enemies.tank_enemy import TankEnemy
            
            enemy = None
            
            if enemy_type == "basic":
                enemy = BasicEnemy(0, 0)
            elif enemy_type == "fast":
                enemy = FastEnemy(0, 0)
            elif enemy_type == "tank":
                enemy = TankEnemy(0, 0)
            
            if enemy:
                # 根據波數調整敵人屬性
                self._scale_enemy_for_wave(enemy, wave_number)
                
            return enemy
            
        except ImportError:
            # 如果敵人類別還未實現，返回None
            return None
    
    def _scale_enemy_for_wave(self, enemy: BaseEnemy, wave_number: int) -> None:
        """
        根據波數調整敵人屬性
        
        Args:
            enemy (BaseEnemy): 要調整的敵人
            wave_number (int): 當前波數
        """
        # 生命值遞增（每波增加15%）
        health_multiplier = self.base_enemy_health_multiplier * (1 + (wave_number - 1) * 0.15)
        enemy.max_health = int(enemy.max_health * health_multiplier)
        enemy.health = enemy.max_health
        
        # 速度遞增（每波增加5%，但有上限）
        speed_multiplier = self.base_enemy_speed_multiplier * (1 + (wave_number - 1) * 0.05)
        speed_multiplier = min(speed_multiplier, 2.0)  # 最大2倍速度
        enemy.speed *= speed_multiplier
        
        # 獎勵遞增（每波增加10%）
        reward_multiplier = self.base_enemy_reward_multiplier * (1 + (wave_number - 1) * 0.10)
        enemy.reward = int(enemy.reward * reward_multiplier)
        enemy.score_value = int(enemy.score_value * reward_multiplier)
    
    def start_first_wave(self) -> bool:
        """
        開始第一波
        
        Returns:
            bool: 是否成功開始
        """
        if self.current_wave == 0 and self.waves:
            self.current_wave = 1
            if self.auto_start_waves:
                self._start_current_wave()
            else:
                self._prepare_current_wave()
            return True
        return False
    
    def start_next_wave(self) -> bool:
        """
        開始下一波
        
        Returns:
            bool: 是否成功開始下一波
        """
        if self.can_start_next_wave():
            self.current_wave += 1
            if self.auto_start_waves:
                self._start_current_wave()
            else:
                self._prepare_current_wave()
            return True
        return False
    
    def can_start_next_wave(self) -> bool:
        """檢查是否可以開始下一波"""
        return (self.wave_state in [WaveState.COMPLETED, WaveState.WAITING] and 
                self.current_wave < len(self.waves))
    
    def _prepare_current_wave(self) -> None:
        """準備當前波數"""
        self.wave_state = WaveState.PREPARING
        self.preparation_start_time = self.current_time
    
    def _start_current_wave(self) -> None:
        """開始當前波數"""
        current_wave = self.get_current_wave()
        if current_wave:
            current_wave.state = WaveState.SPAWNING
            current_wave.start_time = self.current_time
            self.wave_state = WaveState.SPAWNING
            
            # 重置生成資訊
            for spawn_info in current_wave.enemy_spawns:
                spawn_info.spawned_count = 0
                spawn_info.last_spawn_time = 0
                spawn_info.start_time = 0
    
    def complete_current_wave(self) -> int:
        """
        完成當前波數
        
        Returns:
            int: 波數完成獎勵金額
        """
        current_wave = self.get_current_wave()
        if current_wave:
            current_wave.state = WaveState.COMPLETED
            self.wave_state = WaveState.COMPLETED
            
            # 計算獎勵
            bonus = int(self.wave_clear_bonus * current_wave.reward_multiplier)
            return bonus
        return 0
    
    def spawn_enemies(self) -> List[BaseEnemy]:
        """
        獲取並清空待生成的敵人列表
        
        Returns:
            List[BaseEnemy]: 待生成的敵人列表
        """
        enemies = self.enemies_to_spawn.copy()
        self.enemies_to_spawn.clear()
        return enemies
    
    def get_current_wave(self) -> Optional[Wave]:
        """
        獲取當前波數物件
        
        Returns:
            Optional[Wave]: 當前波數物件，如果沒有則返回None
        """
        if 1 <= self.current_wave <= len(self.waves):
            return self.waves[self.current_wave - 1]
        return None
    
    def get_next_wave(self) -> Optional[Wave]:
        """
        獲取下一波數物件
        
        Returns:
            Optional[Wave]: 下一波數物件，如果沒有則返回None
        """
        if self.current_wave < len(self.waves):
            return self.waves[self.current_wave]
        return None
    
    def is_all_waves_completed(self) -> bool:
        """檢查是否完成所有波數"""
        return (self.current_wave >= len(self.waves) and 
                self.wave_state == WaveState.COMPLETED)
    
    def get_wave_progress(self) -> float:
        """
        獲取當前波數進度（0.0-1.0）
        
        Returns:
            float: 當前波數進度
        """
        current_wave = self.get_current_wave()
        if not current_wave:
            return 0.0
        
        total_enemies = current_wave.get_total_enemies()
        if total_enemies == 0:
            return 1.0
        
        spawned_enemies = current_wave.get_spawned_enemies()
        return min(spawned_enemies / total_enemies, 1.0)
    
    def get_preparation_time_left(self) -> float:
        """
        獲取準備階段剩餘時間
        
        Returns:
            float: 剩餘準備時間（秒）
        """
        if self.wave_state != WaveState.PREPARING:
            return 0.0
        
        current_wave = self.get_current_wave()
        if not current_wave:
            return 0.0
        
        elapsed = self.current_time - self.preparation_start_time
        return max(0.0, current_wave.preparation_time - elapsed)
    
    def get_wave_info(self) -> Dict[str, Any]:
        """
        獲取波數資訊
        
        Returns:
            Dict[str, Any]: 包含波數資訊的字典
        """
        current_wave = self.get_current_wave()
        next_wave = self.get_next_wave()
        
        return {
            'current_wave': self.current_wave,
            'total_waves': len(self.waves),
            'wave_state': self.wave_state.value,
            'wave_progress': self.get_wave_progress(),
            'preparation_time_left': self.get_preparation_time_left(),
            'current_wave_enemies': current_wave.get_total_enemies() if current_wave else 0,
            'current_wave_spawned': current_wave.get_spawned_enemies() if current_wave else 0,
            'next_wave_enemies': next_wave.get_total_enemies() if next_wave else 0,
            'can_start_next': self.can_start_next_wave(),
            'all_completed': self.is_all_waves_completed()
        }
    
    def force_start_wave(self) -> bool:
        """
        強制開始當前波數（跳過準備時間）
        
        Returns:
            bool: 是否成功強制開始
        """
        if self.wave_state == WaveState.PREPARING:
            self._start_current_wave()
            return True
        elif self.wave_state == WaveState.WAITING and self.can_start_next_wave():
            if self.current_wave == 0:
                return self.start_first_wave()
            else:
                return self.start_next_wave()
        return False
    
    def skip_to_wave(self, wave_number: int) -> bool:
        """
        跳轉到指定波數（調試用）
        
        Args:
            wave_number (int): 目標波數
            
        Returns:
            bool: 是否成功跳轉
        """
        if 1 <= wave_number <= len(self.waves):
            self.current_wave = wave_number
            self.wave_state = WaveState.WAITING
            self.enemies_to_spawn.clear()
            return True
        return False
