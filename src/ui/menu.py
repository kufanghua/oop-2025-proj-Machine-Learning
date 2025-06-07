import pygame
from src.utils.constants import FONT_NAME, BG_COLOR

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, 36)
        self.small_font = pygame.font.SysFont(FONT_NAME, 28)
        self.bg_color = BG_COLOR
        # 難度、地圖大小選項
        self.difficulties = ["easy", "normal", "hard"]
        # 你可以根據遊戲需求自訂每個難度的預設地圖大小
        self.map_sizes = {
            "easy": (20, 30),
            "normal": (24, 36),
            "hard": (30, 45)
        }
        self.selected_index = 0

    def draw(self):
        self.screen.fill(self.bg_color)
        title = self.font.render("Tower Defense", True, (60, 60, 120))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 40))

        tip = self.small_font.render("請選擇難度（上下鍵切換，Enter確認）", True, (70, 70, 70))
        self.screen.blit(tip, (self.screen.get_width() // 2 - tip.get_width() // 2, 110))

        for idx, diff in enumerate(self.difficulties):
            color = (40, 120, 40) if idx == self.selected_index else (120, 120, 120)
            diff_text = f"{diff.upper()}  地圖:{self.map_sizes[diff][0]}x{self.map_sizes[diff][1]}"
            surf = self.font.render(diff_text, True, color)
            x = self.screen.get_width() // 2 - surf.get_width() // 2
            y = 170 + idx * 60
            self.screen.blit(surf, (x, y))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.difficulties)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.difficulties)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        selecting = False
            self.draw()
            clock.tick(30)
        diff = self.difficulties[self.selected_index]
        return diff, self.map_sizes[diff]

    def show_game_over(self, score):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(FONT_NAME, 48)
        small_font = pygame.font.SysFont(FONT_NAME, 28)
        over_text = font.render("GAME OVER", True, (200, 40, 40))
        score_text = small_font.render(f"最終分數: {score}", True, (40, 40, 40))
        restart_text = small_font.render("按任意鍵退出...", True, (60, 60, 60))

        self.screen.fill((255, 230, 230))
        self.screen.blit(over_text, (self.screen.get_width() // 2 - over_text.get_width() // 2, 110))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, 200))
        self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, 260))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            clock.tick(15)