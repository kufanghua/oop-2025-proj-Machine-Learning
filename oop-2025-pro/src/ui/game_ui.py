"""
遊戲使用者介面類別
處理遊戲中的UI顯示和互動
"""
import pygame
from ..utils.constants import COLORS, SCREEN_CONFIG, UI_CONFIG

class GameUI:
    """遊戲UI管理器"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # UI元素位置
        self.ui_panel_rect = pygame.Rect(
            screen_width - UI_CONFIG['panel_width'], 0,
            UI_CONFIG['panel_width'], screen_height
        )
        self.tower_buttons = []
        self._setup_tower_buttons()
        
        # 遊戲狀態顯示
        self.info_y = 20
        
    def _setup_tower_buttons(self):
        """設置塔的選擇按鈕"""
        button_width = 80
        button_height = 60
        margin = 10
        start_x = self.ui_panel_rect.x + margin
        start_y = 100
        
        tower_types = [
            {'name': 'Cannon', 'cost': 50, 'color': COLORS['RED']},
            {'name': 'Machine', 'cost': 75, 'color': COLORS['YELLOW']},
            {'name': 'Freeze', 'cost': 100, 'color': COLORS['BLUE']}
        ]
        
        for i, tower_info in enumerate(tower_types):
            y = start_y + i * (button_height + margin)
            button_rect = pygame.Rect(start_x, y, button_width, button_height)
            self.tower_buttons.append({
                'rect': button_rect,
                'tower_type': tower_info['name'].lower(),
                'cost': tower_info['cost'],
                'color': tower_info['color'],
                'name': tower_info['name']
            })
    
    def draw(self, screen, game_state):
        """繪製遊戲UI"""
        # 繪製UI面板背景
        pygame.draw.rect(screen, COLORS['DARK_GRAY'], self.ui_panel_rect)
        pygame.draw.rect(screen, COLORS['WHITE'], self.ui_panel_rect, 2)
        
        # 繪製遊戲資訊
        self._draw_game_info(screen, game_state)
        
        # 繪製塔選擇按鈕
        self._draw_tower_buttons(screen, game_state.get('money', 0))
        
        # 繪製選中的塔資訊
        if game_state.get('selected_tower'):
            self._draw_tower_info(screen, game_state['selected_tower'])
        
        # 繪製遊戲狀態消息
        if game_state.get('message'):
            self._draw_message(screen, game_state['message'])
    
    def _draw_game_info(self, screen, game_state):
        """繪製遊戲基本資訊"""
        x = self.ui_panel_rect.x + 10
        y = self.info_y
        line_height = 25
        
        # 生命值
        health_text = f"Health: {game_state.get('health', 100)}"
        health_surface = self.font_medium.render(health_text, True, COLORS['WHITE'])
        screen.blit(health_surface, (x, y))
        y += line_height
        
        # 金錢
        money_text = f"Money: ${game_state.get('money', 0)}"
        money_surface = self.font_medium.render(money_text, True, COLORS['WHITE'])
        screen.blit(money_surface, (x, y))
        y += line_height
        
        # 當前波次
        wave_text = f"Wave: {game_state.get('current_wave', 1)}"
        wave_surface = self.font_medium.render(wave_text, True, COLORS['WHITE'])
        screen.blit(wave_surface, (x, y))
        y += line_height
        
        # 敵人數量
        enemies_text = f"Enemies: {game_state.get('enemies_left', 0)}"
        enemies_surface = self.font_medium.render(enemies_text, True, COLORS['WHITE'])
        screen.blit(enemies_surface, (x, y))
    
    def _draw_tower_buttons(self, screen, money):
        """繪製塔選擇按鈕"""
        for button in self.tower_buttons:
            # 判斷是否可購買
            can_afford = money >= button['cost']
            button_color = button['color'] if can_afford else COLORS['GRAY']
            text_color = COLORS['WHITE'] if can_afford else COLORS['DARK_GRAY']
            
            # 繪製按鈕
            pygame.draw.rect(screen, button_color, button['rect'])
            pygame.draw.rect(screen, COLORS['WHITE'], button['rect'], 2)
            
            # 繪製塔名稱
            name_surface = self.font_small.render(button['name'], True, text_color)
            name_rect = name_surface.get_rect(center=(
                button['rect'].centerx,
                button['rect'].y + 15
            ))
            screen.blit(name_surface, name_rect)
            
            # 繪製價格
            cost_text = f"${button['cost']}"
            cost_surface = self.font_small.render(cost_text, True, text_color)
            cost_rect = cost_surface.get_rect(center=(
                button['rect'].centerx,
                button['rect'].y + 35
            ))
            screen.blit(cost_surface, cost_rect)
    
    def _draw_tower_info(self, screen, tower):
        """繪製選中塔的詳細資訊"""
        x = self.ui_panel_rect.x + 10
        y = 300
        line_height = 20
        
        # 標題
        title_surface = self.font_medium.render("Selected Tower:", True, COLORS['WHITE'])
        screen.blit(title_surface, (x, y))
        y += line_height + 10
        
        # 塔類型
        type_text = f"Type: {tower.get('type', 'Unknown')}"
        type_surface = self.font_small.render(type_text, True, COLORS['WHITE'])
        screen.blit(type_surface, (x, y))
        y += line_height
        
        # 等級
        level_text = f"Level: {tower.get('level', 1)}"
        level_surface = self.font_small.render(level_text, True, COLORS['WHITE'])
        screen.blit(level_surface, (x, y))
        y += line_height
        
        # 傷害
        damage_text = f"Damage: {tower.get('damage', 0)}"
        damage_surface = self.font_small.render(damage_text, True, COLORS['WHITE'])
        screen.blit(damage_surface, (x, y))
        y += line_height
        
        # 射程
        range_text = f"Range: {tower.get('range', 0)}"
        range_surface = self.font_small.render(range_text, True, COLORS['WHITE'])
        screen.blit(range_surface, (x, y))
        y += line_height
        
        # 升級按鈕
        upgrade_rect = pygame.Rect(x, y + 10, 100, 30)
        upgrade_color = COLORS['GREEN'] if tower.get('can_upgrade', False) else COLORS['GRAY']
        pygame.draw.rect(screen, upgrade_color, upgrade_rect)
        pygame.draw.rect(screen, COLORS['WHITE'], upgrade_rect, 2)
        
        upgrade_text = f"Upgrade ${tower.get('upgrade_cost', 0)}"
        upgrade_surface = self.font_small.render(upgrade_text, True, COLORS['WHITE'])
        upgrade_text_rect = upgrade_surface.get_rect(center=upgrade_rect.center)
        screen.blit(upgrade_surface, upgrade_text_rect)
        
        # 儲存升級按鈕rect供點擊檢測
        tower['upgrade_button_rect'] = upgrade_rect
    
    def _draw_message(self, screen, message):
        """繪製遊戲狀態消息"""
        message_surface = self.font_medium.render(message, True, COLORS['WHITE'])
        message_rect = message_surface.get_rect(center=(
            self.screen_width // 2,
            self.screen_height - 50
        ))
        
        # 背景
        bg_rect = message_rect.inflate(20, 10)
        pygame.draw.rect(screen, COLORS['BLACK'], bg_rect)
        pygame.draw.rect(screen, COLORS['WHITE'], bg_rect, 2)
        
        screen.blit(message_surface, message_rect)
    
    def handle_click(self, mouse_pos, game_state):
        """處理滑鼠點擊事件"""
        # 檢查塔選擇按鈕
        for button in self.tower_buttons:
            if button['rect'].collidepoint(mouse_pos):
                if game_state.get('money', 0) >= button['cost']:
                    return {
                        'action': 'select_tower_type',
                        'tower_type': button['tower_type'],
                        'cost': button['cost']
                    }
                else:
                    return {'action': 'insufficient_money'}
        
        # 檢查升級按鈕
        selected_tower = game_state.get('selected_tower')
        if selected_tower and 'upgrade_button_rect' in selected_tower:
            if selected_tower['upgrade_button_rect'].collidepoint(mouse_pos):
                if selected_tower.get('can_upgrade', False):
                    return {
                        'action': 'upgrade_tower',
                        'tower': selected_tower
                    }
        
        return None
    
    def get_ui_panel_rect(self):
        """獲取UI面板矩形區域"""
        return self.ui_panel_rect
