"""
地圖管理模組
負責管理遊戲地圖、路徑、可建造區域等地圖相關功能
"""

import pygame
from typing import List, Tuple, Optional
from enum import Enum
from ..utils.constants import MAP_SETTINGS


class TileType(Enum):
    """地圖格子類型枚舉"""
    EMPTY = 0          # 空地（可建造）
    PATH = 1           # 路徑
    TOWER = 2          # 已放置塔
    BLOCKED = 3        # 阻擋區域（不可建造）
    START = 4          # 起始點
    END = 5            # 終點


class MapManager:
    """
    地圖管理器類別
    負責管理遊戲地圖的佈局、路徑規劃和可建造區域判定
    """
    
    def __init__(self, map_data: Optional[List[List[int]]] = None):
        """
        初始化地圖管理器
        
        Args:
            map_data (Optional[List[List[int]]]): 地圖數據，如果為None則使用預設地圖
        """
        self.tile_size = MAP_SETTINGS['TILE_SIZE']
        self.map_width = MAP_SETTINGS['MAP_WIDTH']
        self.map_height = MAP_SETTINGS['MAP_HEIGHT']
        
        # 初始化地圖
        if map_data:
            self.map_data = map_data
        else:
            self.map_data = self._create_default_map()
        
        # 路徑相關
        self.path_points = self._calculate_path()
        self.start_point = self._find_start_point()
        self.end_point = self._find_end_point()
        
        # 地圖表面（用於渲染）
        self.map_surface = None
        self._create_map_surface()
    
    def _create_default_map(self) -> List[List[int]]:
        """
        創建預設地圖
        
        Returns:
            List[List[int]]: 地圖數據
        """
        # 創建一個簡單的S型路徑地圖
        map_data = [[TileType.EMPTY.value for _ in range(self.map_width)] 
                   for _ in range(self.map_height)]
        
        # 設置起始點（左上角）
        map_data[2][0] = TileType.START.value
        
        # 設置路徑 - 創建一個S型路徑
        path_coords = [
            # 第一段：向右
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
            # 轉彎向下
            (3, 7), (4, 7), (5, 7), (6, 7),
            # 第二段：向左
            (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1),
            # 轉彎向下
            (7, 1), (8, 1), (9, 1), (10, 1),
            # 第三段：向右到終點
            (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9)
        ]
        
        # 設置路徑
        for y, x in path_coords:
            if 0 <= y < self.map_height and 0 <= x < self.map_width:
                map_data[y][x] = TileType.PATH.value
        
        # 設置終點
        map_data[10][9] = TileType.END.value
        
        return map_data
    
    def _calculate_path(self) -> List[Tuple[int, int]]:
        """
        計算完整路徑點座標
        
        Returns:
            List[Tuple[int, int]]: 路徑點列表（像素座標）
        """
        path_points = []
        
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = TileType(self.map_data[y][x])
                if tile_type in [TileType.PATH, TileType.START, TileType.END]:
                    # 轉換為像素座標（格子中心）
                    pixel_x = x * self.tile_size + self.tile_size // 2
                    pixel_y = y * self.tile_size + self.tile_size // 2
                    path_points.append((pixel_x, pixel_y))
        
        # 排序路徑點以確保順序正確
        return self._sort_path_points(path_points)
    
    def _sort_path_points(self, points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        排序路徑點以確保正確的順序
        
        Args:
            points (List[Tuple[int, int]]): 未排序的路徑點
            
        Returns:
            List[Tuple[int, int]]: 排序後的路徑點
        """
        if not points:
            return []
        
        # 找到起始點
        start_tile = self._find_start_point()
        if not start_tile:
            return points
        
        start_pixel = (start_tile[0] * self.tile_size + self.tile_size // 2,
                      start_tile[1] * self.tile_size + self.tile_size // 2)
        
        sorted_points = [start_pixel]
        remaining_points = [p for p in points if p != start_pixel]
        
        # 使用貪婪算法找到最短路徑順序
        current_point = start_pixel
        while remaining_points:
            # 找到距離當前點最近的點
            closest_point = min(remaining_points, 
                               key=lambda p: self._distance(current_point, p))
            sorted_points.append(closest_point)
            remaining_points.remove(closest_point)
            current_point = closest_point
        
        return sorted_points
    
    def _distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """計算兩點間的距離"""
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    
    def _find_start_point(self) -> Optional[Tuple[int, int]]:
        """
        找到起始點的格子座標
        
        Returns:
            Optional[Tuple[int, int]]: 起始點座標 (x, y)，如果沒找到則返回None
        """
        for y in range(self.map_height):
            for x in range(self.map_width):
                if TileType(self.map_data[y][x]) == TileType.START:
                    return (x, y)
        return None
    
    def _find_end_point(self) -> Optional[Tuple[int, int]]:
        """
        找到終點的格子座標
        
        Returns:
            Optional[Tuple[int, int]]: 終點座標 (x, y)，如果沒找到則返回None
        """
        for y in range(self.map_height):
            for x in range(self.map_width):
                if TileType(self.map_data[y][x]) == TileType.END:
                    return (x, y)
        return None
    
    def _create_map_surface(self) -> None:
        """創建地圖渲染表面"""
        self.map_surface = pygame.Surface((
            self.map_width * self.tile_size,
            self.map_height * self.tile_size
        ))
        
        # 顏色定義
        colors = {
            TileType.EMPTY: (34, 139, 34),      # 森林綠（可建造區域）
            TileType.PATH: (139, 126, 102),     # 沙棕色（路徑）
            TileType.TOWER: (128, 128, 128),    # 灰色（已放置塔）
            TileType.BLOCKED: (105, 105, 105),  # 深灰色（阻擋區域）
            TileType.START: (0, 255, 0),        # 綠色（起始點）
            TileType.END: (255, 0, 0)           # 紅色（終點）
        }
        
        # 繪製地圖
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = TileType(self.map_data[y][x])
                color = colors.get(tile_type, (0, 0, 0))
                
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                
                pygame.draw.rect(self.map_surface, color, rect)
                pygame.draw.rect(self.map_surface, (0, 0, 0), rect, 1)  # 邊框
    
    def can_place_tower(self, pixel_x: int, pixel_y: int) -> bool:
        """
        檢查指定像素座標是否可以放置塔
        
        Args:
            pixel_x (int): 像素X座標
            pixel_y (int): 像素Y座標
            
        Returns:
            bool: 是否可以放置塔
        """
        # 轉換為格子座標
        grid_x = pixel_x // self.tile_size
        grid_y = pixel_y // self.tile_size
        
        # 檢查邊界
        if (grid_x < 0 or grid_x >= self.map_width or 
            grid_y < 0 or grid_y >= self.map_height):
            return False
        
        # 檢查格子類型
        tile_type = TileType(self.map_data[grid_y][grid_x])
        return tile_type == TileType.EMPTY
    
    def place_tower(self, pixel_x: int, pixel_y: int) -> bool:
        """
        在指定位置放置塔
        
        Args:
            pixel_x (int): 像素X座標
            pixel_y (int): 像素Y座標
            
        Returns:
            bool: 是否成功放置
        """
        if not self.can_place_tower(pixel_x, pixel_y):
            return False
        
        # 轉換為格子座標
        grid_x = pixel_x // self.tile_size
        grid_y = pixel_y // self.tile_size
        
        # 設置為塔的位置
        self.map_data[grid_y][grid_x] = TileType.TOWER.value
        
        # 更新地圖表面
        self._update_tile_surface(grid_x, grid_y)
        
        return True
    
    def remove_tower(self, pixel_x: int, pixel_y: int) -> bool:
        """
        移除指定位置的塔
        
        Args:
            pixel_x (int): 像素X座標
            pixel_y (int): 像素Y座標
            
        Returns:
            bool: 是否成功移除
        """
        # 轉換為格子座標
        grid_x = pixel_x // self.tile_size
        grid_y = pixel_y // self.tile_size
        
        # 檢查邊界
        if (grid_x < 0 or grid_x >= self.map_width or 
            grid_y < 0 or grid_y >= self.map_height):
            return False
        
        # 檢查是否是塔的位置
        if TileType(self.map_data[grid_y][grid_x]) != TileType.TOWER:
            return False
        
        # 設置為空地
        self.map_data[grid_y][grid_x] = TileType.EMPTY.value
        
        # 更新地圖表面
        self._update_tile_surface(grid_x, grid_y)
        
        return True
    
    def _update_tile_surface(self, grid_x: int, grid_y: int) -> None:
        """
        更新指定格子的渲染表面
        
        Args:
            grid_x (int): 格子X座標
            grid_y (int): 格子Y座標
        """
        colors = {
            TileType.EMPTY: (34, 139, 34),
            TileType.PATH: (139, 126, 102),
            TileType.TOWER: (128, 128, 128),
            TileType.BLOCKED: (105, 105, 105),
            TileType.START: (0, 255, 0),
            TileType.END: (255, 0, 0)
        }
        
        tile_type = TileType(self.map_data[grid_y][grid_x])
        color = colors.get(tile_type, (0, 0, 0))
        
        rect = pygame.Rect(
            grid_x * self.tile_size,
            grid_y * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        
        pygame.draw.rect(self.map_surface, color, rect)
        pygame.draw.rect(self.map_surface, (0, 0, 0), rect, 1)
    
    def get_path(self) -> List[Tuple[int, int]]:
        """
        獲取路徑點列表
        
        Returns:
            List[Tuple[int, int]]: 路徑點列表（像素座標）
        """
        return self.path_points.copy()
    
    def get_spawn_point(self) -> Tuple[int, int]:
        """
        獲取敵人生成點
        
        Returns:
            Tuple[int, int]: 生成點座標（像素座標）
        """
        if self.path_points:
            return self.path_points[0]
        return (0, 0)
    
    def get_end_point_pixel(self) -> Tuple[int, int]:
        """
        獲取終點的像素座標
        
        Returns:
            Tuple[int, int]: 終點座標（像素座標）
        """
        if self.path_points:
            return self.path_points[-1]
        return (0, 0)
    
    def pixel_to_grid(self, pixel_x: int, pixel_y: int) -> Tuple[int, int]:
        """
        將像素座標轉換為格子座標
        
        Args:
            pixel_x (int): 像素X座標
            pixel_y (int): 像素Y座標
            
        Returns:
            Tuple[int, int]: 格子座標 (x, y)
        """
        return (pixel_x // self.tile_size, pixel_y // self.tile_size)
    
    def grid_to_pixel(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        將格子座標轉換為像素座標（格子中心）
        
        Args:
            grid_x (int): 格子X座標
            grid_y
