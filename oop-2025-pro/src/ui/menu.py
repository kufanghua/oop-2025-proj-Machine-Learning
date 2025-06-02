"""
選單系統類別
處理主選單、暫停選單等介面
"""
import pygame
from ..utils.constants import COLORS, SCREEN_CONFIG

class Menu:
    """選單管理器"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.current_menu = 'main'  # main, pause, game_over, victory
        self.buttons = {}
        self._setup_menus()
        
    def _setup_menus(self):
        """設置各種選單的按鈕"""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        button_width = 200
        button_height = 50
        button_spacing = 70
        
        # 主選單按鈕
        self.buttons['main'] = [
            {
                'text': 'Start Game',
                'rect': pygame.Rect(center_x - button_width//2, center_y - button_spacing, 
                                  button_width, button_height),
                'action': 'start_game',
                'color': COLORS['GREEN']
            },
            {
                'text': 'Instructions',
                'rect': pygame.Rect(center_x - button_width//2, center_y, 
                                  button_width, button_height),
                'action': 'show_instructions',
                'color': COLORS['BLUE']
            },
            {
                'text': 'Quit',
                'rect': pygame.Rect(center_x - button_width//2, center_y + button_spacing, 
                                  button_width, button_height),
                'action': 'quit',
                'color': COLORS['RED']
            }
        ]
        
        # 暫停選單按鈕
        self.buttons['pause'] = [
            {
                'text': 'Resume',
                'rect': pygame.Rect(center_x - button_width//2, center_y - button_spacing, 
                                  button_width, button_height),
                'action': 'resume',
                'color': COLORS['GREEN']
            },
            {
                'text': 'Restart',
                'rect': pygame.Rect(center_x - button_width//2, center_y, 
                                  button_width, button_height),
                'action': 'restart',
                'color': COLORS['YELLOW']
            },
            {
                'text': 'Main Menu',
                'rect': pygame.Rect(center_x - button_width//2, center_y + button_spacing, 
                                  button_width, button_height),
                'action': 'main_menu',
                'color': COLORS['RED']
            }
        ]
        
        # 遊戲結束選單按鈕
        self.buttons['game_over'] = [
            {
                'text': 'Restart',
                'rect': pygame.Rect(center_x - button_width//2, center_y, 
                                  button_width, button_height),
                'action': 'restart',
                'color': COLORS['GREEN']
            },
            {
                'text': 'Main Menu',
                'rect': pygame.Rect(center_x - button_width//2, center_y + button_spacing, 
                                  button_width, button_height),
                'action': 'main_menu',
                'color': COLORS['RED']
            }
        ]
        
        # 勝利選單按鈕
        self.buttons['victory'] = [
            {
                'text': 'Play Again',
                'rect': pygame.Rect(center_x - button_width//2, center_y, 
                                  button_width, button_height),
                'action': 'restart',
                'color': COLORS['GREEN']
            },
            {
                'text': 'Main Menu',
                'rect': pygame.Rect(center_x - button_width//2, center_y + button_spacing, 
                                  button_width, button_height),
                'action': 'main_menu',
                'color': COLORS['BLUE']
            }
        ]
        
        # 說明畫面按鈕
        self.buttons['instructions'] = [
            {
                'text': 'Back',
                'rect': pygame.Rect(center_x - button_width//2, self.screen_height - 100, 
                                  button_width, button_height),
                'action': 'main_menu',
                'color': COLORS['GRAY']
            }
        ]
    
    def set_menu(self, menu_type):
        """設置當前選單類型"""
        self.current_menu = menu_type
    
    def draw(self, screen, **kwargs):
        """繪製當前選單"""
        # 半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(COLORS['BLACK'])
        screen.blit(overlay, (0, 0))
        
        if self.current_menu == 'main':
            self._draw_main_menu(screen)
        elif self.current_menu == 'pause':
            self._draw_pause_menu(screen)
        elif self.current_menu == 'game_over':
            self._draw_game_over_menu(screen, kwargs.get('final_wave', 0))
        elif self.current_menu == 'victory':
            self._draw_victory_menu(screen, kwargs.get('final_score', 0))
        elif self.current_menu == 'instructions':
            self._draw_instructions_menu(screen)
    
    def _draw_main_menu(self, screen):
        """繪製主選單"""
        # 標題
        title_surface = self.font_title.render("Tower Defense", True, COLORS['WHITE'])
        title_rect = title_surface.get_rect(center=(self.screen_width//2, 150))
        screen.blit(title_surface, title_rect)
        
        # 副標題
        subtitle_surface = self.font_medium.render("Defend Your Base!", True, COLORS['LIGHT_GRAY'])
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width//2, 200))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # 按鈕
        self._draw_buttons(screen, 'main')
    
    def _draw_pause_menu(self, screen):
        """繪製暫停選單"""
        title_surface = self.font_large.render("PAUSED", True, COLORS['WHITE'])
        title_rect = title_surface.get_rect(center=(self.screen_width//2, 200))
        screen.blit(title_surface, title_rect)
        
        self._draw_buttons(screen, 'pause')
    
    def _draw_game_over_menu(self, screen, final_wave):
        """繪製遊戲結束選單"""
        title_surface = self.font_large.render("GAME OVER", True, COLORS['RED'])
        title_rect = title_surface.get_rect(center=(self.screen_width//2, 200))
        screen.blit(title_surface, title_rect)
        
        wave_text = f"You survived {final_wave} waves"
        wave_surface = self.font_medium.render(wave_text, True, COLORS['WHITE'])
        wave_rect = wave_surface.get_rect(center=(self.screen_width//2, 250))
        screen.blit(wave_surface, wave_rect)
        
        self._draw_buttons(screen, 'game_over')
    
    def _draw_victory_menu(self, screen, final_score):
        """繪製勝利選單"""
        title_surface = self.font_large.render("VICTORY!", True, COLORS['GREEN'])
        title_rect = title_surface.get_rect(center=(self.screen_width//2, 200))
        screen.blit(title_surface, title_rect)
        
        score_text = f"Final Score: {final_score}"
        score_surface = self.font_medium.render(score_text, True, COLORS['WHITE'])
        score_rect = score_surface.get_rect(center=(self.screen_width//2, 250))
        screen.blit(score_surface, score_rect)
        
        self._draw_buttons(screen, 'victory')
    
    def _draw_instructions_menu(self, screen):
        """繪製說明選單"""
        title_surface = self.font_large.render("How to Play", True, COLORS['WHITE'])
        title_rect = title_surface.get_rect(center=(self.screen_width//2, 80))
        screen.blit(title_surface, title_rect)
        
        instructions = [
            "• Click on tower buttons to select a tower type",
            "• Click on the map to place towers",
            "• Towers automatically attack enemies in range",
            "• Click on towers to upgrade them",
            "• Prevent enemies from reaching your base",
            "• Earn money by defeating enemies",
            "",
            "Tower Types:",
            "• Cannon Tower: High damage, slow fire rate",
            "• Machine Tower: Fast fire rate, moderate damage", 
            "• Freeze Tower: Slows enemies, low damage",
            "",
            "• Press ESC to pause the game"
        ]
        
        y = 140
        for instruction in instructions:
            if instruction:  # 非空行
                color = COLORS['YELLOW'] if instruction.startswith("•") and "Tower" in instruction else COLORS['WHITE']
                text_surface = self.font_small.render(instruction, True, color)
                text_rect = text_surface.get_rect(center=(self.screen_width//2, y))
                screen.blit(text_surface, text_rect)
            y += 25
        
        self._draw_buttons(screen, 'instructions')
    
    def _draw_buttons(self, screen, menu_type):
        """繪製按鈕"""
        if menu_type not in self.buttons:
            return
            
        for button in self.buttons[menu_type]:
            # 繪製按鈕背景
            pygame.draw.rect(screen, button['color'], button['rect'])
            pygame.draw.rect(screen, COLORS['WHITE'], button['rect'], 3)
            
            # 繪製按鈕文字
            text_surface = self.font_medium.render(button['text'], True, COLORS['WHITE'])
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
    
    def handle_click(self, mouse_pos):
        """處理滑鼠點擊事件"""
        if self.current_menu not in self.buttons:
            return None
            
        for button in self.buttons[self.current_menu]:
            if button['rect'].collidepoint(mouse_pos):
                return button['action']
        
        return None
    
    def handle_key(self, key):
        """處理鍵盤事件"""
        if key == pygame.K_ESCAPE:
            if self.current_menu == 'pause':
                return 'resume'
            elif self.current_menu in ['main', 'instructions']:
                return 'quit'
        
        return None
