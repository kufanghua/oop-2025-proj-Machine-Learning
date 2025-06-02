"""
冰球投射物類別
具有冰凍效果的投射物
"""
import pygame
from .base_projectile import BaseProjectile
from ..utils.constants import PROJECTILE_CONFIG

class IceBall(BaseProjectile):
    """冰球投射物類別"""
    
    def __init__(self, start_pos, target_pos, damage=15):
        super().__init__(start_pos, target_pos, damage, PROJECTILE_CONFIG['ice_ball']['speed'])
        self.freeze_duration = PROJECTILE_CONFIG['ice_ball']['freeze_duration']
        self.slow_factor = PROJECTILE_CONFIG['ice_ball']['slow_factor']
        self.color = (173, 216, 230)  # 淺藍色
        self.trail_particles = []
        
    def update(self, dt):
        """更新冰球狀態"""
        super().update(dt)
        self._update_trail_effect(dt)
        
    def _update_trail_effect(self, dt):
        """更新冰霜軌跡效果"""
        # 添加新的軌跡粒子
        if len(self.trail_particles) < 8:
            particle = {
                'pos': list(self.position),
                'life': 0.3,
                'max_life': 0.3
            }
            self.trail_particles.append(particle)
        
        # 更新軌跡粒子
        for particle in self.trail_particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
    
    def draw(self, screen):
        """繪製冰球和軌跡效果"""
        # 繪製軌跡
        for particle in self.trail_particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*self.color, alpha)
            size = int(3 * (particle['life'] / particle['max_life']))
            if size > 0:
                try:
                    pygame.draw.circle(screen, color[:3], 
                                     (int(particle['pos'][0]), int(particle['pos'][1])), size)
                except:
                    pass
        
        # 繪製冰球本體
        pygame.draw.circle(screen, self.color, 
                         (int(self.position[0]), int(self.position[1])), 
                         self.radius)
        
        # 繪製內核
        inner_color = (135, 206, 250)  # 天空藍
        pygame.draw.circle(screen, inner_color,
                         (int(self.position[0]), int(self.position[1])),
                         self.radius - 2)
    
    def on_hit(self, enemy):
        """冰球命中敵人時的效果"""
        # 造成傷害
        enemy.take_damage(self.damage)
        # 施加冰凍效果
        enemy.apply_freeze(self.freeze_duration, self.slow_factor)
        return True
