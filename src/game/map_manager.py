import pygame
import os
from src.utils.constants import TILE_SIZE, MAP_BG_COLOR

class MapManager:
    def __init__(self, game_manager, map_size=None, difficulty=None):
        self.game_manager = game_manager
        if map_size is None:
            raise ValueError("map_size 必須指定 (rows, cols)")
        self.rows, self.cols = map_size
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.path_tiles = self.generate_path_tiles()
        self.tower_spots = self.generate_tower_spots()
        spot_img_path = os.path.join("assets", "images", "map", "tower_spot.png")
        self.tower_spot_img = pygame.image.load(spot_img_path).convert_alpha()
        self.tower_spot_img = pygame.transform.scale(self.tower_spot_img, (TILE_SIZE, TILE_SIZE))
    def generate_path_tiles(self):
        path = []
        if self.difficulty == "easy":
            #右
            row = self.rows //2
            for col in range(0, self.cols // 4 + 1):
                path.append((row, col))
            #上
            col = self.cols // 4
            for r in range(self.rows //2, 2, -1):
                path.append((r, col))
            #右
            row = 2
            for col in range(self.cols // 4 , self.cols//2-1):
                path.append((row, col))
            #下
            col = self.cols//2-1
            for r in range(2, self.rows-2):
                path.append((r, col))
            #右
            row = self.rows-2
            for col in range(self.cols//2-1 , (self.cols // 4)*3-1):
                path.append((row, col))
            #上
            col = (self.cols // 4)*3-1
            for r in range(self.rows-2, self.rows//2, -1):
                path.append((r, col))
            #右
            row = self.rows//2
            for col in range((self.cols // 4)*3-1 , self.cols):
                path.append((row, col))
            return path

        elif self.difficulty == "normal":
            #右
            row = self.rows //2
            for col in range(0, self.cols // 4 -1):
                path.append((row, col))
            #下
            col = self.cols // 4 -1
            for r in range(self.rows //2, self.rows-1):
                path.append((r, col))
            #上
            col = self.cols // 4 
            for r in range(self.rows-2, 3, -1):
                path.append((r, col))
            #右
            row = 3
            for col in range(self.cols // 4 , self.cols // 2):
                path.append((row, col))
            #下
            col = self.cols // 2
            for r in range(3, self.rows//2 + 1):
                path.append((r, col))
            #左
            row = self.rows//2 + 1
            for col in range(self.cols //2 , self.cols // 4+2,-1):
                path.append((row, col))
            #下
            col = self.cols // 4+2
            for r in range(self.rows//2 + 1, self.rows-2):
                path.append((r, col))
            #右
            row = self.rows-2
            for col in range(self.cols // 4+2, self.cols//4*3-1):
                path.append((row, col))
            #上
            col = self.cols//4*3-1
            for r in range(self.rows-2, self.rows//3, -1):
                path.append((r, col))
            #右
            row = self.rows//3
            for col in range(self.cols//4*3-1, self.cols):
                path.append((row, col))
            #下
            col = self.cols-1
            for r in range(self.rows//3, self.rows):
                path.append((r, col))
            return path

        elif self.difficulty == "hard":
            path = []
            r, c = 0, 0
            path.append((r, c))
            for ci in range(1, self.cols // 5 + 1):
                path.append((r, ci))
            for ri in range(1, self.rows // 4 + 1):
                path.append((ri, self.cols // 5))
            for ci in range(self.cols // 5 - 1, self.cols // 3 - 1, -1):
                path.append((self.rows // 4, ci))
            for ri in range(self.rows // 4 + 1, 2 * self.rows // 5 + 1):
                path.append((ri, self.cols // 3))
            for ci in range(self.cols // 3 + 1, 2 * self.cols // 3 + 1):
                path.append((2 * self.rows // 5, ci))
            direction = 1
            for ri in range(2 * self.rows // 5 + 1, 3 * self.rows // 5 + 1):
                col_start = 2 * self.cols // 3 if direction == 1 else 2 * self.cols // 3 - 3
                col_end = 2 * self.cols // 3 - 3 if direction == 1 else 2 * self.cols // 3
                step = 1 if direction == 1 else -1
                for ci in range(col_start, col_end + step, step):
                    if 0 <= ci < self.cols:
                        path.append((ri, ci))
                direction *= -1
            for ri in range(3 * self.rows // 5 + 1, 3 * self.rows // 4 + 1):
                col_pos = 2 * self.cols // 3 - 3
                if 0 <= col_pos < self.cols:
                    path.append((ri, col_pos))
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

        for row in range(self.rows):
            path.append((row, self.cols // 2))
        return path

    def generate_tower_spots(self):
        spots = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.path_tiles and (row + col) % 1 == 0:
                    spots.append((row, col))
        return spots

    def draw_castle(self, surface, x, y, size):
        # 主體
        body_rect = pygame.Rect(x + size * 0.15, y + size * 0.4, size * 0.7, size * 0.5)
        pygame.draw.rect(surface, (180, 180, 200), body_rect)

        # 左右塔樓
        tower_w, tower_h = size * 0.18, size * 0.7
        left_tower = pygame.Rect(x, y + size * 0.15, tower_w, tower_h)
        right_tower = pygame.Rect(x + size - tower_w, y + size * 0.15, tower_w, tower_h)
        pygame.draw.rect(surface, (150, 150, 180), left_tower)
        pygame.draw.rect(surface, (150, 150, 180), right_tower)

        # 塔尖
        pygame.draw.polygon(surface, (120, 120, 160), [
            (x + tower_w/2, y),
            (x, y + size * 0.15),
            (x + tower_w, y + size * 0.15)
        ])
        pygame.draw.polygon(surface, (120, 120, 160), [
            (x + size - tower_w/2, y),
            (x + size - tower_w, y + size * 0.15),
            (x + size, y + size * 0.15)
        ])

        # 門
        door_rect = pygame.Rect(x + size * 0.45, y + size * 0.7, size * 0.1, size * 0.2)
        pygame.draw.rect(surface, (100, 100, 120), door_rect)
        # 門圓弧
        pygame.draw.ellipse(surface, (100, 100, 120), (x + size * 0.45, y + size * 0.78, size * 0.1, size * 0.08))

    def draw(self, surface):
        surface.fill(MAP_BG_COLOR)
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(
                    surface, (200, 200, 200),
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    1
                )
        for (row, col) in self.path_tiles:
            pygame.draw.rect(
                surface, (180, 180, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
        for (row, col) in self.tower_spots:
            #pygame.draw.rect(
             #   surface, (100, 200, 100),
            surface.blit(
                self.tower_spot_img,
                (col * TILE_SIZE, row * TILE_SIZE)#, TILE_SIZE, TILE_SIZE)
            )
        # 畫城堡
        if self.path_tiles:
            end_row, end_col = self.path_tiles[-1]
            self.draw_castle(surface, end_col * TILE_SIZE, end_row * TILE_SIZE, TILE_SIZE)

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
        return enemy.get_map_grid_pos() == self.path_tiles[-1]