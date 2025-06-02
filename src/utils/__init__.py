"""
工具模組
包含常數定義、輔助函數和動畫處理
"""

from .constants import *
from .helpers import *
from .animation import (
    Animation, TweenAnimation, Vector2DTween, SpriteAnimation,
    Particle, ParticleSystem, AnimationManager, EaseType,
    create_fade_in_animation, create_fade_out_animation,
    create_scale_animation, create_shake_animation
)

__all__ = [
    # Constants
    'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'FPS', 'TILE_SIZE',
    'COLORS', 'TOWER_COLORS', 'ENEMY_COLORS',
    'GAME_STATES', 'DIFFICULTY_LEVELS',
    
    # Helpers
    'calculate_distance', 'calculate_angle', 'normalize_vector',
    'clamp', 'lerp', 'point_in_rect', 'circle_collision',
    'load_image', 'load_sound', 'format_time', 'format_number',
    
    # Animation
    'Animation', 'TweenAnimation', 'Vector2DTween', 'SpriteAnimation',
    'Particle', 'ParticleSystem', 'AnimationManager', 'EaseType',
    'create_fade_in_animation', 'create_fade_out_animation',
    'create_scale_animation', 'create_shake_animation'
]
