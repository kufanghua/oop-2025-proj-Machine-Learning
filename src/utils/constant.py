"""
遊戲常數定義
包含所有遊戲中使用的常數值
"""

# 螢幕設定
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# 遊戲設定
INITIAL_MONEY = 500
INITIAL_LIVES = 20
ENEMY_SPAWN_INTERVAL = 1.0  # 秒

# 塔設定
TOWER_COST = {
    'cannon': 100,
    'machine': 75,
    'freeze': 150
}

TOWER_STATS = {
    'cannon': {'damage': 100, 'range': 120, 'attack_speed': 0.5},
    'machine': {'damage': 25, 'range': 100, 'attack_speed': 3.0},
    'freeze': {'damage': 30, 'range': 90, 'attack_speed': 1.5}
}

# 敵人設定
ENEMY_STATS = {
    'basic': {'hp': 100, 'speed': 50, 'reward': 10},
    'fast': {'hp': 60, 'speed': 100, 'reward': 15},
    'tank': {'hp': 300, 'speed': 25, 'reward': 30}
}

# 路徑設定
DEFAULT_PATH = [
    (50, 100), (200, 100), (200, 300), (400, 300),
    (400, 150), (600, 150), (600, 400), (800, 400),
    (800, 200), (950, 200), (950, 600)
]

# UI設定
UI_HEIGHT = 50
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
