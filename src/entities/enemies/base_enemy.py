import pygame
from src.entities.base_entity import BaseEntity
from src.utils.constants import TILE_SIZE  # 改為引入專案的 TILE_SIZE

class BaseEnemy(BaseEntity):
    name = "BaseEnemy"
    speed = 60  # pix/sec
    hp_default = 30
    reward = 10

    def __init__(self, start_tile, game_manager):
        x = start_tile[1] * TILE_SIZE + TILE_SIZE // 2
        y = start_tile[0] * TILE_SIZE + TILE_SIZE // 2
        image = pygame.Surface((TILE_SIZE - 6, TILE_SIZE - 6), pygame.SRCALPHA)
        pygame.draw.circle(
            image,
            (180, 80, 80),
            ((TILE_SIZE - 6) // 2, (TILE_SIZE - 6) // 2),
            (TILE_SIZE - 6) // 2
        )
        super().__init__(x, y, image, self.hp_default)
        self.game_manager = game_manager
        self.path = list(game_manager.map_manager.path_tiles) if hasattr(game_manager, "map_manager") else []
        self.target_idx = 0
        self.slow_timer = 0

    def update(self, dt):
        if self.slow_timer > 0:
            move_speed = self.speed * 0.4
            self.slow_timer -= dt
        else:
            move_speed = self.speed
        if self.target_idx >= len(self.path):
            return
        target_tile = self.path[self.target_idx]
        target_x = target_tile[1] * TILE_SIZE + TILE_SIZE // 2
        target_y = target_tile[0] * TILE_SIZE + TILE_SIZE // 2
        dx, dy = target_x - self.x, target_y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < move_speed * dt:
            self.x, self.y = target_x, target_y
            self.target_idx += 1
        else:
            self.x += dx / dist * move_speed * dt
            self.y += dy / dist * move_speed * dt
        self.rect.center = (self.x, self.y)

    def get_hp_percent(self):
        return self.hp / self.max_hp if self.max_hp > 0 else 0

    def draw(self, surface):
        # 畫敵人本體
        surface.blit(self.image, self.rect.topleft)
        # 血條座標與尺寸
        bar_width = self.rect.width
        bar_height = 7
        bar_x = self.rect.x
        bar_y = self.rect.y - 12

        # 血條底
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # 血條現值
        percent = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (220, 30, 30), (bar_x, bar_y, int(bar_width * percent), bar_height))

        # 顯示百分比數字
        font = pygame.font.SysFont("Arial", 12)
        percent_txt = font.render(f"{int(percent * 100)}%", True, (255, 255, 255))
        txt_rect = percent_txt.get_rect(center=(self.rect.centerx, bar_y + bar_height // 2))
        surface.blit(percent_txt, txt_rect)

    def take_damage(self, dmg):
        super().take_damage(dmg)
        if self.hp <= 0 and hasattr(self.game_manager, "earn_money"):
            self.game_manager.earn_money(self.reward)
            self.game_manager.add_score(self.reward)

    def slow(self, t):
        self.slow_timer = max(self.slow_timer, t)

    def get_map_grid_pos(self):
        return (int(self.y) // TILE_SIZE, int(self.x) // TILE_SIZE)