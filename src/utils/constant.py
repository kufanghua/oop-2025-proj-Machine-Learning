"""
遊戲常數定義
包含所有遊戲中使用的常數配置
"""

# 螢幕配置
SCREEN_CONFIG = {
    'width': 1200,
    'height': 800,
    'fps': 60,
    'title': 'Tower Defense Game'
}

# 顏色定義
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0),
    'PINK': (255, 192, 203),
    'BROWN': (139, 69, 19),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (211, 211, 211),
    'DARK_GRAY': (64, 64, 64),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255)
}

# UI配置
UI_CONFIG = {
    'panel_width': 200,
    'button_height': 40,
    'button_margin': 10,
    'info_panel_height': 100
}

# 地圖配置
MAP_CONFIG = {
    'tile_size': 40,
    'path_width': 35,
    'grid_color': COLORS['LIGHT_GRAY'],
    'path_color': COLORS['BROWN'],
    'buildable_color': COLORS['GREEN'],
    'non_buildable_color': COLORS['RED']
}

# 遊戲配置
GAME_CONFIG = {
    'starting_health': 100,
    'starting_money': 200,
    'base_enemy_reward': 10,
    'wave_delay': 3.0,  # 秒
    'enemy_spawn_interval': 1.0  # 秒
}

# 塔配置
TOWER_CONFIG = {
    'cannon': {
        'cost': 50,
        'damage': 40,
        'range': 120,
        'fire_rate': 1.0,  # 每秒攻擊次數
        'upgrade_cost_multiplier': 1.5,
        'max_level': 5,
        'projectile_speed': 300,
        'color': COLORS['RED']
    },
    'machine': {
        'cost': 75,
        'damage': 15,
        'range': 100,
        'fire_rate': 3.0,
        'upgrade_cost_multiplier': 1.4,
        'max_level': 5,
        'projectile_speed': 400,
        'color': COLORS['YELLOW']
    },
    'freeze': {
        'cost': 100,
        'damage': 10,
        'range': 90,
        'fire_rate': 1.5,
        'upgrade_cost_multiplier': 1.6,
        'max_level': 5,
        'projectile_speed': 250,
        'freeze_duration': 2.0,
        'slow_factor': 0.5,
        'color': COLORS['BLUE']
    }
}

# 敵人配置
ENEMY_CONFIG = {
    'basic': {
        'health': 50,
        'speed': 60,
        'reward': 10,
        'color': COLORS['RED'],
        'size': 15
    },
    'fast': {
        'health': 30,
        'speed': 100,
        'reward': 15,
        'color': COLORS['YELLOW'],
        'size': 12
    },
    'tank': {
        'health': 150,
        'speed': 30,
        'reward': 25,
        'color': COLORS['PURPLE'],
        'size': 20
    },
    'boss': {
        'health': 500,
        'speed': 40,
        'reward': 100,
        'color': COLORS['BLACK'],
        'size': 30
    }
}

# 投射物配置
PROJECTILE_CONFIG = {
    'cannon_ball': {
        'speed': 300,
        'color': COLORS['BLACK'],
        'size': 6,
        'explosion_radius': 0
    },
    'bullet': {
        'speed': 400,
        'color': COLORS['YELLOW'],
        'size': 4,
        'explosion_radius': 0
    },
    'ice_ball': {
        'speed': 250,
        'color': COLORS['CYAN'],
        'size': 5,
        'freeze_duration': 2.0,
        'slow_factor': 0.5,
        'explosion_radius': 0
    }
}

# 波次配置
WAVE_CONFIG = {
    'waves': [
        # 波次1-5: 基礎敵人
        {'enemies': [{'type': 'basic', 'count': 10}], 'delay': 1.0},
        {'enemies': [{'type': 'basic', 'count': 15}], 'delay': 0.8},
        {'enemies': [{'type': 'basic', 'count': 12, 'type': 'fast', 'count': 5}], 'delay': 0.8},
        {'enemies': [{'type': 'basic', 'count': 18, 'type': 'fast', 'count': 8}], 'delay': 0.7},
        {'enemies': [{'type': 'basic', 'count': 20, 'type': 'fast', 'count': 10, 'type': 'tank', 'count': 2}], 'delay': 0.7},
        
        # 波次6-10: 增加坦克敵人
        {'enemies': [{'type': 'basic', 'count': 25, 'type': 'fast', 'count': 12, 'type': 'tank', 'count': 5}], 'delay': 0.6},
        {'enemies': [{'type': 'basic', 'count': 30, 'type': 'fast', 'count': 15, 'type': 'tank', 'count': 8}], 'delay': 0.6},
        {'enemies': [{'type': 'basic', 'count': 35, 'type': 'fast', 'count': 18, 'type': 'tank', 'count': 10}], 'delay': 0.5},
        {'enemies': [{'type': 'basic', 'count': 40, 'type': 'fast', 'count': 20, 'type': 'tank', 'count': 12}], 'delay': 0.5},
        {'enemies': [{'type': 'basic', 'count': 45, 'type': 'fast', 'count': 22, 'type': 'tank', 'count': 15, 'type': 'boss', 'count': 1}], 'delay': 0.4}
    ],
    'difficulty_scaling': {
        'health_multiplier': 1.1,  # 每波敵人血量增加10%
        'speed_multiplier': 1.02,  # 每波敵人速度增加2%
        'reward_multiplier': 1.05  # 每波獎勵增加5%
    }
}

# 路徑配置
PATH_CONFIG = {
    'default_path': [
        (0, 200), (100, 200), (100, 400), (300, 400),
        (300, 200), (500, 200), (500, 600), (700, 600),
        (700, 300), (900, 300), (900, 500), (1000, 500)
    ],
    'waypoint_tolerance': 20,
    'path_smoothing': True
}

# 動畫配置
ANIMATION_CONFIG = {
    'explosion': {
        'duration': 0.5,
        'max_particles': 20,
        'colors': [COLORS['ORANGE'], COLORS['RED'], COLORS['YELLOW']]
    },
    'death': {
        'duration': 0.3,
        'fade_speed': 500
    },
    'upgrade': {
        'duration': 0.8,
        'glow_intensity': 100
    }
}

# 效果配置
EFFECTS_CONFIG = {
    'freeze': {
        'color': COLORS['CYAN'],
        'alpha': 128,
        'particle_count': 5
    },
    'poison': {
        'color': COLORS['GREEN'],
        'alpha': 100,
        'damage_per_second': 5
    },
    'burn': {
        'color': COLORS['ORANGE'],
        'alpha': 120,
        'damage_per_second': 8
    }
}

# 音效配置（如果需要音效）
SOUND_CONFIG = {
    'master_volume': 0.7,
    'sfx_volume': 0.8,
    'music_volume': 0.5,
    'sounds': {
        'tower_shoot': 'shoot.wav',
        'enemy_death': 'enemy_death.wav',
        'tower_upgrade': 'upgrade.wav',
        'wave_complete': 'wave_complete.wav',
        'game_over': 'game_over.wav'
    }
}
