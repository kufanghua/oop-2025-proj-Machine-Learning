import pygame

from src.utils.constants import FONT_NAME, TILE_SIZE, MAP_SIZE_EASY, MAP_SIZE_NORMAL, MAP_SIZE_HARD

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/NotoSansTC-Black.ttf", TILE_SIZE)
        self.options = [
            (f"簡單 {MAP_SIZE_EASY}", "easy", MAP_SIZE_EASY),
            (f"普通 {MAP_SIZE_NORMAL}", "normal", MAP_SIZE_NORMAL),
            (f"困難 {MAP_SIZE_HARD}", "hard", MAP_SIZE_HARD),
        ]
        self.selected = 0
        self.option_rects = []

    def draw(self):
        self.screen.fill((50, 50, 80))
        title = self.font.render("oop_project-塔防遊戲 ", True, (255, 255, 255))
        self.screen.blit(title, (150, 30))
        title = self.font.render("難度選擇", True, (255, 255, 255))
        self.screen.blit(title, (300, 100))
        font_name = pygame.font.Font("assets/fonts/NotoSansTC-Black.ttf", TILE_SIZE-20)
        text1 = font_name.render("by12組 葉哲 張政洋 古芳華", True, (255, 255, 255))
        self.screen.blit(text1, (450, 550))
        self.option_rects = []
        mouse_pos = pygame.mouse.get_pos()
        for i, (label, _, _) in enumerate(self.options):
            rect_pos = (250, 200+ i * 100)
            text = self.font.render(label, True, (200, 200, 200))
            rect = text.get_rect(topleft=rect_pos)
            # 如果滑鼠在這個選項上，變亮藍色
            if rect.collidepoint(mouse_pos):
                color = (50, 180, 255)
                text = self.font.render(label, True, color)

            self.screen.blit(text, rect)
            self.option_rects.append(rect)
        pygame.display.flip()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected = i
                            _, difficulty, map_size = self.options[self.selected]
                            return difficulty, map_size
            clock.tick(30)

    def show_game_over(self, score):
        self.screen.fill((30, 10, 10))
        font_big = pygame.font.Font("assets/fonts/NotoSansTC-Black.ttf", TILE_SIZE+10)
        text1 = font_big.render("遊戲結束", True, (255, 80, 80))
        text2 = self.font.render(f"得分: {score}", True, (255, 255, 255))
        text3 = self.font.render("按任意鍵離開...", True, (180, 180, 180))
        self.screen.blit(text1, (350, 100))
        self.screen.blit(text2, (400, 200))
        self.screen.blit(text3, (320, 300))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False 