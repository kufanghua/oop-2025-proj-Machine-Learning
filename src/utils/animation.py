"""
動畫處理模組 - 負責處理遊戲中的動畫效果
包含補間動畫、粒子效果、精靈動畫等功能
"""

import pygame
import math
from typing import List, Tuple, Callable, Optional
from enum import Enum


class EaseType(Enum):
    """緩動類型枚舉"""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"


class Animation:
    """基礎動畫類別"""
    
    def __init__(self, 
                 duration: float, 
                 ease_type: EaseType = EaseType.LINEAR,
                 loop: bool = False,
                 reverse: bool = False):
        self.duration = duration
        self.ease_type = ease_type
        self.loop = loop
        self.reverse = reverse
        self.current_time = 0.0
        self.is_finished = False
        self.is_playing = False
        self.callbacks = []
        
    def start(self):
        """開始播放動畫"""
        self.is_playing = True
        self.is_finished = False
        self.current_time = 0.0
        
    def stop(self):
        """停止動畫"""
        self.is_playing = False
        
    def reset(self):
        """重置動畫"""
        self.current_time = 0.0
        self.is_finished = False
        
    def update(self, dt: float):
        """更新動畫狀態"""
        if not self.is_playing or self.is_finished:
            return
            
        self.current_time += dt
        
        if self.current_time >= self.duration:
            if self.loop:
                self.current_time = 0.0
            else:
                self.current_time = self.duration
                self.is_finished = True
                self.is_playing = False
                self._trigger_callbacks()
                
    def get_progress(self) -> float:
        """獲取動畫進度 (0.0 - 1.0)"""
        if self.duration == 0:
            return 1.0
        progress = min(self.current_time / self.duration, 1.0)
        
        if self.reverse:
            progress = 1.0 - progress
            
        return self._apply_easing(progress)
    
    def _apply_easing(self, t: float) -> float:
        """應用緩動函數"""
        if self.ease_type == EaseType.LINEAR:
            return t
        elif self.ease_type == EaseType.EASE_IN:
            return t * t
        elif self.ease_type == EaseType.EASE_OUT:
            return 1 - (1 - t) * (1 - t)
        elif self.ease_type == EaseType.EASE_IN_OUT:
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) * (1 - t)
        elif self.ease_type == EaseType.BOUNCE:
            if t < 1/2.75:
                return 7.5625 * t * t
            elif t < 2/2.75:
                t -= 1.5/2.75
                return 7.5625 * t * t + 0.75
            elif t < 2.5/2.75:
                t -= 2.25/2.75
                return 7.5625 * t * t + 0.9375
            else:
                t -= 2.625/2.75
                return 7.5625 * t * t + 0.984375
        elif self.ease_type == EaseType.ELASTIC:
            if t == 0 or t == 1:
                return t
            return -(2**(10*(t-1))) * math.sin((t-1-0.1/4)*(2*math.pi)/0.1)
        else:
            return t
    
    def add_callback(self, callback: Callable):
        """添加動畫完成回調"""
        self.callbacks.append(callback)
        
    def _trigger_callbacks(self):
        """觸發完成回調"""
        for callback in self.callbacks:
            callback()


class TweenAnimation(Animation):
    """補間動畫類別"""
    
    def __init__(self, 
                 start_value: float, 
                 end_value: float,
                 duration: float,
                 ease_type: EaseType = EaseType.LINEAR,
                 loop: bool = False,
                 reverse: bool = False):
        super().__init__(duration, ease_type, loop, reverse)
        self.start_value = start_value
        self.end_value = end_value
        
    def get_current_value(self) -> float:
        """獲取當前動畫值"""
        progress = self.get_progress()
        return self.start_value + (self.end_value - self.start_value) * progress


class Vector2DTween(Animation):
    """2D向量補間動畫"""
    
    def __init__(self,
                 start_pos: Tuple[float, float],
                 end_pos: Tuple[float, float],
                 duration: float,
                 ease_type: EaseType = EaseType.LINEAR):
        super().__init__(duration, ease_type)
        self.start_pos = start_pos
        self.end_pos = end_pos
        
    def get_current_position(self) -> Tuple[float, float]:
        """獲取當前位置"""
        progress = self.get_progress()
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        return (x, y)


class SpriteAnimation:
    """精靈動畫類別 - 用於播放精靈圖序列"""
    
    def __init__(self, frames: List[pygame.Surface], frame_duration: float, loop: bool = True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.frame_timer = 0.0
        self.is_playing = True
        self.is_finished = False
        
    def update(self, dt: float):
        """更新動畫幀"""
        if not self.is_playing or self.is_finished:
            return
            
        self.frame_timer += dt
        
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.is_finished = True
                    self.is_playing = False
                    
    def get_current_frame(self) -> pygame.Surface:
        """獲取當前幀"""
        if self.frames:
            return self.frames[self.current_frame]
        return None
    
    def restart(self):
        """重新開始動畫"""
        self.current_frame = 0
        self.frame_timer = 0.0
        self.is_playing = True
        self.is_finished = False


class Particle:
    """粒子類別"""
    
    def __init__(self, 
                 x: float, y: float,
                 velocity_x: float, velocity_y: float,
                 life_time: float,
                 color: Tuple[int, int, int],
                 size: float = 2.0):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life_time = life_time
        self.max_life_time = life_time
        self.color = color
        self.size = size
        self.alpha = 255
        
    def update(self, dt: float):
        """更新粒子狀態"""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.life_time -= dt
        
        # 根據生命週期調整透明度
        if self.max_life_time > 0:
            self.alpha = int(255 * (self.life_time / self.max_life_time))
            
    def is_alive(self) -> bool:
        """檢查粒子是否存活"""
        return self.life_time > 0
        
    def draw(self, screen: pygame.Surface):
        """繪製粒子"""
        if self.is_alive():
            # 創建帶透明度的表面
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, max(0, self.alpha))
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (self.size, self.size), self.size)
            screen.blit(particle_surface, (self.x - self.size, self.y - self.size))


class ParticleSystem:
    """粒子系統"""
    
    def __init__(self):
        self.particles: List[Particle] = []
        
    def emit_explosion(self, x: float, y: float, count: int = 20, color: Tuple[int, int, int] = (255, 255, 0)):
        """發射爆炸粒子效果"""
        for _ in range(count):
            angle = math.random() * 2 * math.pi
            speed = 50 + math.random() * 100
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            life_time = 0.5 + math.random() * 1.0
            
            particle = Particle(x, y, velocity_x, velocity_y, life_time, color)
            self.particles.append(particle)
            
    def emit_trail(self, x: float, y: float, direction: Tuple[float, float], 
                   color: Tuple[int, int, int] = (255, 255, 255)):
        """發射軌跡粒子效果"""
        # 在運動方向的反方向發射粒子
        angle_variation = 0.5
        base_angle = math.atan2(-direction[1], -direction[0])
        
        for _ in range(5):
            angle = base_angle + (math.random() - 0.5) * angle_variation
            speed = 20 + math.random() * 30
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            life_time = 0.2 + math.random() * 0.3
            
            particle = Particle(x, y, velocity_x, velocity_y, life_time, color, 1.5)
            self.particles.append(particle)
            
    def update(self, dt: float):
        """更新所有粒子"""
        # 更新粒子並移除死亡的粒子
        self.particles = [p for p in self.particles if p.is_alive()]
        
        for particle in self.particles:
            particle.update(dt)
            
    def draw(self, screen: pygame.Surface):
        """繪製所有粒子"""
        for particle in self.particles:
            particle.draw(screen)
            
    def clear(self):
        """清除所有粒子"""
        self.particles.clear()


class AnimationManager:
    """動畫管理器 - 管理所有動畫的播放"""
    
    def __init__(self):
        self.animations: List[Animation] = []
        self.particle_system = ParticleSystem()
        
    def add_animation(self, animation: Animation):
        """添加動畫"""
        self.animations.append(animation)
        animation.start()
        
    def create_tween(self, start_value: float, end_value: float, duration: float,
                    ease_type: EaseType = EaseType.LINEAR) -> TweenAnimation:
        """創建補間動畫"""
        tween = TweenAnimation(start_value, end_value, duration, ease_type)
        self.add_animation(tween)
        return tween
        
    def create_move_animation(self, start_pos: Tuple[float, float], 
                            end_pos: Tuple[float, float], 
                            duration: float,
                            ease_type: EaseType = EaseType.LINEAR) -> Vector2DTween:
        """創建移動動畫"""
        move_anim = Vector2DTween(start_pos, end_pos, duration, ease_type)
        self.add_animation(move_anim)
        return move_anim
        
    def update(self, dt: float):
        """更新所有動畫"""
        # 更新動畫並移除完成的動畫
        active_animations = []
        for animation in self.animations:
            animation.update(dt)
            if not animation.is_finished:
                active_animations.append(animation)
        self.animations = active_animations
        
        # 更新粒子系統
        self.particle_system.update(dt)
        
    def draw_particles(self, screen: pygame.Surface):
        """繪製粒子效果"""
        self.particle_system.draw(screen)
        
    def emit_explosion(self, x: float, y: float, count: int = 20, 
                      color: Tuple[int, int, int] = (255, 255, 0)):
        """發射爆炸效果"""
        self.particle_system.emit_explosion(x, y, count, color)
        
    def emit_trail(self, x: float, y: float, direction: Tuple[float, float],
                  color: Tuple[int, int, int] = (255, 255, 255)):
        """發射軌跡效果"""
        self.particle_system.emit_trail(x, y, direction, color)
        
    def clear_all(self):
        """清除所有動畫和粒子"""
        self.animations.clear()
        self.particle_system.clear()


# 便捷函數
def create_fade_in_animation(duration: float) -> TweenAnimation:
    """創建淡入動畫"""
    return TweenAnimation(0.0, 1.0, duration, EaseType.EASE_OUT)


def create_fade_out_animation(duration: float) -> TweenAnimation:
    """創建淡出動畫"""
    return TweenAnimation(1.0, 0.0, duration, EaseType.EASE_IN)


def create_scale_animation(start_scale: float, end_scale: float, 
                          duration: float) -> TweenAnimation:
    """創建縮放動畫"""
    return TweenAnimation(start_scale, end_scale, duration, EaseType.BOUNCE)


def create_shake_animation(intensity: float, duration: float) -> List[TweenAnimation]:
    """創建震動動畫"""
    shake_x = TweenAnimation(-intensity, intensity, duration / 4, EaseType.LINEAR, loop=True, reverse=True)
    shake_y = TweenAnimation(-intensity, intensity, duration / 3, EaseType.LINEAR, loop=True, reverse=True)
    return [shake_x, shake_y]
