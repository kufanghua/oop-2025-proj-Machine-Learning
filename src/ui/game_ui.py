import pygame
from src.utils.constants import FONT_NAME, SCREEN_WIDTH, SCREEN_HEIGHT, UI_BG_COLOR
from src.entities.towers.cannon_tower import CannonTower
from src.entities.towers.machine_tower import MachineTower
from src.entities.towers.freeze_tower import FreezeTower

TOWER_CLASSES = [
    (CannonTower, "加農砲塔"),
    (MachineTower, "機槍塔"),
    (FreezeTower, "冰凍塔")
]

class GameUI:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = pygame.font.SysFont(FONT_NAME, 22)
        self.tower_buttons = []
        self.selected_idx = None
        self.selected_tower = None  # 新增：記錄點擊地圖的塔
        self._init_tower_buttons()

    def _init_tower_buttons(self):
        for i, (tower_cls, label) in enumerate(TOWER_CLASSES):
            rect = pygame.Rect(20 + i * 80, 45, 70, 70)
            self.tower_buttons.append((rect, tower_cls, label))

    def update(self, dt):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, UI_BG_COLOR, (0, 0, SCREEN_WIDTH, 40))
        money_txt = self.font.render(f"金錢: {self.game_manager.money}", True, (0, 80, 0))
        life_txt = self.font.render(f"生命: {self.game_manager.life}", True, (180, 0, 0))
        score_txt = self.font.render(f"分數: {self.game_manager.score}", True, (0, 0, 180))
        surface.blit(money_txt, (10, 7))
        surface.blit(life_txt, (150, 7))
        surface.blit(score_txt, (280, 7))

        for i, (rect, tower_cls, label) in enumerate(self.tower_buttons):
            if self.game_manager.selected_tower_type == tower_cls:
                pygame.draw.rect(surface, (170, 200, 255), rect)
            else:
                pygame.draw.rect(surface, (220, 220, 220), rect)
            pygame.draw.rect(surface, (60, 60, 90), rect, 2)
            txt = pygame.font.SysFont(FONT_NAME, 18).render(label, True, (30, 30, 80))
            surface.blit(txt, (rect.x + 3, rect.y + 8))
            price = getattr(tower_cls, "cost", 100)
            price_txt = pygame.font.SysFont(FONT_NAME, 16).render(f"${price}", True, (80, 90, 20))
            surface.blit(price_txt, (rect.x + 6, rect.y + 40))

        if not self.game_manager.selected_tower_type:
            tip = self.font.render("請先點選上方塔種再蓋塔", True, (200, 40, 40))
            surface.blit(tip, (SCREEN_WIDTH//2 - tip.get_width()//2, 9))

        # --- 顯示攻擊範圍 ---
        if self.selected_tower:
            self.draw_tower_range(surface, self.selected_tower)
            self.draw_upgrade_panel(surface, self.selected_tower)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, tower_cls, _ in self.tower_buttons:
                if rect.collidepoint(pos):
                    self.game_manager.selected_tower_type = tower_cls
                    self.selected_tower = None
                    return True
            # 點擊地圖上的塔
            for tower in self.game_manager.towers:
                if tower.rect.collidepoint(pos):
                    self.selected_tower = tower
                    self.game_manager.selected_tower_type = None
                    return True
            # 點擊升級按鈕
            if self.selected_tower:
                upg_rect = pygame.Rect(SCREEN_WIDTH-230+40, 60+100, 140, 30)
                if upg_rect.collidepoint(pos) and self.selected_tower.can_upgrade():
                    if self.selected_tower.upgrade():
                        # 升級成功後可加音效等
                        pass
                    else:
                        # 金錢不足等提示
                        pass
                    return True  # 事件已處理
            self.selected_tower = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.selected_tower = None
        return False

    def handle_click(self, pos):
        # 不再需要，直接在 handle_event 檢查
        pass

    def draw_upgrade_panel(self, surface, tower):
        panel_rect = pygame.Rect(SCREEN_WIDTH-230, 60, 220, 140)
        pygame.draw.rect(surface, (250, 245, 220), panel_rect)
        pygame.draw.rect(surface, (80, 70, 60), panel_rect, 2)
        title = self.font.render("塔升級", True, (60, 50, 50))
        surface.blit(title, (panel_rect.x+60, panel_rect.y+10))

        info = [
            f"等級: {tower.level}/{tower.max_level}",
            f"攻擊力: {tower.damage}",
            f"射速: {tower.attack_speed:.2f} 秒/發"
        ]
        for i, text in enumerate(info):
            txt = pygame.font.SysFont(FONT_NAME, 18).render(text, True, (50, 50, 90))
            surface.blit(txt, (panel_rect.x+18, panel_rect.y+50+i*27))

        if tower.can_upgrade():
            upgrade_btn = pygame.Rect(panel_rect.x+40, panel_rect.y+100, 140, 30)
            pygame.draw.rect(surface, (100, 180, 90), upgrade_btn)
            pygame.draw.rect(surface, (60, 90, 50), upgrade_btn, 2)
            cost = tower.upgrade_cost()
            btn_txt = self.font.render(f"升級 (${cost})", True, (20, 40, 20))
            surface.blit(btn_txt, (upgrade_btn.x+16, upgrade_btn.y+4))
        else:
            txt = self.font.render("已達最高等級", True, (180, 60, 60))
            surface.blit(txt, (panel_rect.x+42, panel_rect.y+100))

    def draw_tower_range(self, surface, tower):
        # 畫出攻擊範圍圓圈
        # 假設 tower.x, tower.y 是中心座標，tower.range 是半徑
        # 若 tower.rect 是 pygame.Rect，可用中心 tower.rect.center
        color = (0, 160, 255, 60)  # 半透明藍
        # 處理 alpha: 建立一個臨時 surface
        temp_surface = pygame.Surface((tower.range*2, tower.range*2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, color, (tower.range, tower.range), tower.range)
        # rect.center 為中心座標
        cx, cy = tower.rect.center if hasattr(tower, "rect") else (tower.x, tower.y)
        surface.blit(temp_surface, (cx - tower.range, cy - tower.range))
        # 外框（可選）
        pygame.draw.circle(surface, (0, 120, 220), (cx, cy), tower.range, 2)
