"""
遊戲管理器模組
負責管理整個遊戲的運行流程、狀態和各個子系統的協調
"""

import pygame
from enum import Enum
from typing import List, Optional
from .map_manager import MapManager
from .wave_manager import WaveManager
from ..entities.towers.base_tower import BaseTower
from ..entities.enemies.base_enemy import BaseEnemy
from ..entities.projectiles.base_projectile import BaseProjectile
from ..utils.constants import GAME_SETTINGS


class GameState(Enum):
    """遊戲狀態枚舉"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    WAVE_PREPARATION = "wave_preparation"
    VICTORY = "victory"


class GameManager:
    """
    遊戲管理器類別
    負責管理遊戲的主要運行邏輯、狀態轉換和各個子系統的協調
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        初始化遊戲管理器
        
        Args:
            screen_width (int): 螢幕寬度
            screen_height (int): 螢幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 遊戲狀態
        self.state = GameState.MENU
        self.is_running = True
        self.clock = pygame.time.Clock()
        
        # 遊戲資源
        self.player_health = GAME_SETTINGS['PLAYER_HEALTH']
        self.player_money = GAME_SETTINGS['INITIAL_MONEY']
        self.score = 0
        self.level = 1
        
        # 子系統
        self.map_manager = MapManager()
        self.wave_manager = WaveManager()
        
        # 遊戲物件列表
        self.towers: List[BaseTower] = []
        self.enemies: List[BaseEnemy] = []
        self.projectiles: List[BaseProjectile] = []
        
        # 選中的塔（用於建造和升級）
        self.selected_tower: Optional[BaseTower] = None
        self.selected_tower_type: Optional[str] = None
        
        # 遊戲計時器
        self.game_time = 0
        self.last_update_time = 0
        
    def update(self, dt: float) -> None:
        """
        更新遊戲邏輯
        
        Args:
            dt (float): 時間差值（秒）
        """
        if self.state != GameState.PLAYING:
            return
            
        self.game_time += dt
        
        # 更新波數管理器
        self.wave_manager.update(dt)
        
        # 生成新敵人
        new_enemies = self.wave_manager.spawn_enemies()
        for enemy in new_enemies:
            enemy.set_path(self.map_manager.get_path())
            self.enemies.append(enemy)
        
        # 更新敵人
        self._update_enemies(dt)
        
        # 更新塔
        self._update_towers(dt)
        
        # 更新投射物
        self._update_projectiles(dt)
        
        # 檢查遊戲結束條件
        self._check_game_over()
        
        # 檢查勝利條件
        self._check_victory()
    
    def _update_enemies(self, dt: float) -> None:
        """更新敵人狀態"""
        enemies_to_remove = []
        
        for enemy in self.enemies:
            enemy.update(dt)
            
            # 檢查敵人是否到達終點
            if enemy.reached_end():
                self.player_health -= enemy.damage_to_player
                enemies_to_remove.append(enemy)
            
            # 檢查敵人是否死亡
            elif enemy.is_dead():
                self.player_money += enemy.reward
                self.score += enemy.score_value
                enemies_to_remove.append(enemy)
        
        # 移除已死亡或到達終點的敵人
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
    
    def _update_towers(self, dt: float) -> None:
        """更新塔的狀態"""
        for tower in self.towers:
            tower.update(dt)
            
            # 塔尋找目標並射擊
            target = self._find_target_for_tower(tower)
            if target:
                projectile = tower.shoot(target)
                if projectile:
                    self.projectiles.append(projectile)
    
    def _update_projectiles(self, dt: float) -> None:
        """更新投射物狀態"""
        projectiles_to_remove = []
        
        for projectile in self.projectiles:
            projectile.update(dt)
            
            # 檢查投射物是否擊中目標或超出範圍
            if projectile.has_hit_target() or projectile.is_out_of_bounds():
                if projectile.has_hit_target():
                    # 處理傷害
                    target = projectile.get_target()
                    if target and target in self.enemies:
                        target.take_damage(projectile.damage)
                        # 處理特殊效果（如冰凍）
                        projectile.apply_effect(target)
                
                projectiles_to_remove.append(projectile)
        
        # 移除已擊中或超出範圍的投射物
        for projectile in projectiles_to_remove:
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)
    
    def _find_target_for_tower(self, tower: BaseTower) -> Optional[BaseEnemy]:
        """
        為塔尋找目標敵人
        
        Args:
            tower (BaseTower): 需要尋找目標的塔
            
        Returns:
            Optional[BaseEnemy]: 找到的目標敵人，如果沒有則返回None
        """
        targets_in_range = []
        
        for enemy in self.enemies:
            distance = tower.get_distance_to(enemy)
            if distance <= tower.attack_range:
                targets_in_range.append((enemy, distance))
        
        if not targets_in_range:
            return None
        
        # 根據塔的目標選擇策略選擇目標
        if tower.target_strategy == "closest":
            targets_in_range.sort(key=lambda x: x[1])
            return targets_in_range[0][0]
        elif tower.target_strategy == "strongest":
            targets_in_range.sort(key=lambda x: x[0].health, reverse=True)
            return targets_in_range[0][0]
        elif tower.target_strategy == "fastest":
            targets_in_range.sort(key=lambda x: x[0].speed, reverse=True)
            return targets_in_range[0][0]
        else:
            # 預設選擇最近的
            targets_in_range.sort(key=lambda x: x[1])
            return targets_in_range[0][0]
    
    def _check_game_over(self) -> None:
        """檢查遊戲是否結束"""
        if self.player_health <= 0:
            self.state = GameState.GAME_OVER
    
    def _check_victory(self) -> None:
        """檢查是否勝利"""
        if self.wave_manager.is_all_waves_completed() and len(self.enemies) == 0:
            self.state = GameState.VICTORY
    
    def place_tower(self, tower_type: str, x: int, y: int) -> bool:
        """
        放置塔
        
        Args:
            tower_type (str): 塔的類型
            x (int): X座標
            y (int): Y座標
            
        Returns:
            bool: 是否成功放置
        """
        from ..entities.towers.cannon_tower import CannonTower
        from ..entities.towers.machine_tower import MachineTower
        from ..entities.towers.freeze_tower import FreezeTower
        
        # 檢查位置是否可以放置塔
        if not self.map_manager.can_place_tower(x, y):
            return False
        
        # 檢查是否有足夠金錢
        tower_cost = self._get_tower_cost(tower_type)
        if self.player_money < tower_cost:
            return False
        
        # 創建塔
        tower = None
        if tower_type == "cannon":
            tower = CannonTower(x, y)
        elif tower_type == "machine":
            tower = MachineTower(x, y)
        elif tower_type == "freeze":
            tower = FreezeTower(x, y)
        
        if tower:
            self.towers.append(tower)
            self.player_money -= tower_cost
            self.map_manager.place_tower(x, y)
            return True
        
        return False
    
    def upgrade_tower(self, tower: BaseTower) -> bool:
        """
        升級塔
        
        Args:
            tower (BaseTower): 要升級的塔
            
        Returns:
            bool: 是否成功升級
        """
        if tower.level >= tower.max_level:
            return False
        
        upgrade_cost = tower.get_upgrade_cost()
        if self.player_money < upgrade_cost:
            return False
        
        self.player_money -= upgrade_cost
        tower.upgrade()
        return True
    
    def sell_tower(self, tower: BaseTower) -> bool:
        """
        出售塔
        
        Args:
            tower (BaseTower): 要出售的塔
            
        Returns:
            bool: 是否成功出售
        """
        if tower in self.towers:
            self.towers.remove(tower)
            self.player_money += tower.get_sell_value()
            self.map_manager.remove_tower(tower.x, tower.y)
            return True
        return False
    
    def _get_tower_cost(self, tower_type: str) -> int:
        """獲取塔的建造成本"""
        tower_costs = {
            "cannon": 100,
            "machine": 150,
            "freeze": 200
        }
        return tower_costs.get(tower_type, 0)
    
    def start_game(self) -> None:
        """開始遊戲"""
        self.state = GameState.PLAYING
        self.wave_manager.start_first_wave()
    
    def pause_game(self) -> None:
        """暫停遊戲"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
    
    def resume_game(self) -> None:
        """恢復遊戲"""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
    
    def restart_game(self) -> None:
        """重新開始遊戲"""
        self.__init__(self.screen_width, self.screen_height)
    
    def get_game_info(self) -> dict:
        """
        獲取遊戲資訊
        
        Returns:
            dict: 包含遊戲狀態資訊的字典
        """
        return {
            'health': self.player_health,
            'money': self.player_money,
            'score': self.score,
            'level': self.level,
            'wave': self.wave_manager.current_wave,
            'enemies_remaining': len(self.enemies),
            'state': self.state.value
        }
    
    def handle_click(self, x: int, y: int) -> None:
        """
        處理滑鼠點擊事件
        
        Args:
            x (int): 點擊的X座標
            y (int): 點擊的Y座標
        """
        # 檢查是否點擊了塔
        clicked_tower = None
        for tower in self.towers:
            if tower.contains_point(x, y):
                clicked_tower = tower
                break
        
        if clicked_tower:
            self.selected_tower = clicked_tower
        else:
            # 如果選中了要建造的塔類型，嘗試在點擊位置建造
            if self.selected_tower_type:
                if self.place_tower(self.selected_tower_type, x, y):
                    self.selected_tower_type = None
            else:
                self.selected_tower = None
    
    def select_tower_type(self, tower_type: str) -> None:
        """
        選擇要建造的塔類型
        
        Args:
            tower_type (str): 塔的類型
        """
        self.selected_tower_type = tower_type
        self.selected_tower = None
