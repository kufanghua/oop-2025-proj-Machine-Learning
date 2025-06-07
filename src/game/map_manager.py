import pygame
from src.utils.constants import TILE_SIZE, MAP_BG_COLOR

class MapManager:
    def __init__(self, game_manager, map_size=None, difficulty=None):
        self.game_manager = game_manager
        # 移除對 MAP_ROWS, MAP_COLS 的依賴，強制必須給 map_size
        if map_size is None:
            raise ValueError("map_size 必須指定 (rows, cols)")
        self.rows, self.cols = map_size
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.path_tiles = self.generate_path_tiles()
        self.tower_spots = self.generate_tower_spots()

    def generate_path_tiles(self):
        path = []
        if self.difficulty == "easy":
            # 兩個彎路徑
            row = self.rows - 1
            for col in range(0, self.cols // 2 + 1):
                path.append((row, col))

            # 2. 往上到頂部
            col = self.cols // 2
            for r in range(self.rows - 2, -1, -1):
                path.append((r, col))

            # 3. 右轉到最右上角
            row = 0
            for col in range(self.cols // 2 + 1, self.cols):
                path.append((row, col))

            # 4. 迴轉往下到最右下角（出口）
            col = self.cols - 1
            for r in range(1, self.rows):
                path.append((r, col))

            return path

        elif self.difficulty == "normal":
            # 較多彎與S型路徑
            row, col = 0, 0
            path.append((row, col))
            # 右
            for c in range(1, self.cols // 4 + 1):
                path.append((row, c))
            # 下
            for r in range(1, self.rows // 3 + 1):
                path.append((r, self.cols // 4))
            # 左
            for c in range(self.cols // 4 - 1, self.cols // 3 - 1, -1):
                path.append((self.rows // 3, c))
            # 下
            for r in range(self.rows // 3 + 1, 2 * self.rows // 3 + 1):
                path.append((r, self.cols // 3))
            # 右
            for c in range(self.cols // 3 + 1, 2 * self.cols // 3 + 1):
                path.append((2 * self.rows // 3, c))
            # 下 (S型)
            for r in range(2 * self.rows // 3 + 1, self.rows - 1):
                col_pos = 2 * self.cols // 3
                path.append((r, col_pos))
                if (r - 2 * self.rows // 3) % 2 == 1 and col_pos - 1 >= 0:
                    path.append((r, col_pos - 1))
            path.append((self.rows - 1, self.cols - 1))
            return path

        elif self.difficulty == "hard":
            # 更多彎與更複雜S型路徑
            path = []
            r, c = 0, 0
            path.append((r, c))
            # 右
            for ci in range(1, self.cols // 5 + 1):
                path.append((r, ci))
            # 下
            for ri in range(1, self.rows // 4 + 1):
                path.append((ri, self.cols // 5))
            # 左
            for ci in range(self.cols // 5 - 1, self.cols // 3 - 1, -1):
                path.append((self.rows // 4, ci))
            # 下
            for ri in range(self.rows // 4 + 1, 2 * self.rows // 5 + 1):
                path.append((ri, self.cols // 3))
            # 右
            for ci in range(self.cols // 3 + 1, 2 * self.cols // 3 + 1):
                path.append((2 * self.rows // 5, ci))
            # S型路徑
            direction = 1
            for ri in range(2 * self.rows // 5 + 1, 3 * self.rows // 5 + 1):
                col_start = 2 * self.cols // 3 if direction == 1 else 2 * self.cols // 3 - 3
                col_end = 2 * self.cols // 3 - 3 if direction == 1 else 2 * self.cols // 3
                step = 1 if direction == 1 else -1
                for ci in range(col_start, col_end + step, step):
                    if 0 <= ci < self.cols:
                        path.append((ri, ci))
                direction *= -1
            # 下
            for ri in range(3 * self.rows // 5 + 1, 3 * self.rows // 4 + 1):
                col_pos = 2 * self.cols // 3 - 3
                if 0 <= col_pos < self.cols:
                    path.append((ri, col_pos))
            # 再S型
            direction = 1
            for ri in range(3 * self.rows // 4 + 1, self.rows - 1):
                col_start = 2 * self.cols // 3 - 3 if direction == 1 else 2 * self.cols // 3
                col_end = 2 * self.cols // 3 if direction == 1 else 2 * self.cols // 3 - 3
                step = 1 if direction == 1 else -1
                for ci in range(col_start, col_end + step, step):
                    if 0 <= ci < self.cols:
                        path.append((ri, ci))
                direction *= -1
            path.append((self.rows - 1, self.cols - 1))
            return path

        # fallback: 直線路徑
        for row in range(self.rows):
            path.append((row, self.cols // 2))
        return path

    def generate_tower_spots(self):
        # 可依不同需求設計塔位分布
        spots = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.path_tiles and (row + col) % 1 == 0:
                    spots.append((row, col))
        return spots

    def draw(self, surface):
        # 畫地圖底色
        surface.fill(MAP_BG_COLOR)
        # 畫格線
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(
                    surface, (200, 200, 200),
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    1
                )
        # 畫路徑
        for (row, col) in self.path_tiles:
            pygame.draw.rect(
                surface, (180, 180, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
        # 畫可建塔格
        for (row, col) in self.tower_spots:
            pygame.draw.rect(
                surface, (100, 200, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
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
                tower = tower_type(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2, self.game_manager)
                self.game_manager.add_tower(tower)
                return True
        return False

    def is_enemy_at_end(self, enemy):
        # 判斷敵人是否到地圖終點
        return enemy.get_map_grid_pos() == self.path_tiles[-1]