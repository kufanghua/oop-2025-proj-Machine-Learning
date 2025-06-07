import pygame
from src.utils.constants import TILE_SIZE, MAP_ROWS, MAP_COLS, PATH_TILES, TOWER_SPOTS, MAP_BG_COLOR

class MapManager:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.grid = [[0 for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]
        self.tower_spots = TOWER_SPOTS
        self.path_tiles = PATH_TILES

    def draw(self, surface):
        # 畫地圖底色
        surface.fill(MAP_BG_COLOR)
        # 畫格線
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                pygame.draw.rect(
                    surface, (200, 200, 200),
                    (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    1
                )
        # 畫路徑
        for (row, col) in self.path_tiles:
            pygame.draw.rect(
                surface, (180, 180, 100),
                (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
        # 畫可建塔格
        for (row, col) in self.tower_spots:
            pygame.draw.rect(
                surface, (100, 200, 100),
                (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

    def place_tower(self, pos, tower_type):
        col, row = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        if (row, col) in self.tower_spots:
            for tower in self.game_manager.towers:
                tcol = tower.rect.x // TILE_SIZE
                trow = tower.rect.y // TILE_SIZE
                if (trow, tcol) == (row, col):
                    return False  # 已有塔
            if self.game_manager.money >= tower_type.cost:
                tower = tower_type(col*TILE_SIZE+TILE_SIZE//2, row*TILE_SIZE+TILE_SIZE//2, self.game_manager)
                self.game_manager.add_tower(tower)
                return True
        return False

    def is_enemy_at_end(self, enemy):
        # 判斷敵人是否到地圖終點
        return enemy.get_map_grid_pos() == self.path_tiles[-1]
