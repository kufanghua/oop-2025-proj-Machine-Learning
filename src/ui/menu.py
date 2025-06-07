import pygame
from src.utils.constants import FONT_NAME, SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, 40)
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.running = False
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill(BG_COLOR)
        title = self.font.render("塔防遊戲 OOP Project", True, (30, 30, 130))
        msg = pygame.font.SysFont(FONT_NAME, 28).render("按 Enter 或 Space 開始遊戲", True, (60, 60, 60))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        self.screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 250))

    def show_game_over(self, score):
        font = pygame.font.SysFont(FONT_NAME, 38)
        over_txt = font.render("遊戲結束", True, (180, 0, 0))
        score_txt = pygame.font.SysFont(FONT_NAME, 28).render(f"最終分數: {score}", True, (30, 30, 30))
        restart_txt = pygame.font.SysFont(FONT_NAME, 24).render("關閉視窗以結束", True, (60, 60, 60))
        self.screen.fill((245, 230, 220))
        self.screen.blit(over_txt, (SCREEN_WIDTH//2 - over_txt.get_width()//2, 140))
        self.screen.blit(score_txt, (SCREEN_WIDTH//2 - score_txt.get_width()//2, 220))
        self.screen.blit(restart_txt, (SCREEN_WIDTH//2 - restart_txt.get_width()//2, 280))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            pygame.time.wait(50)
