"""
輔助函數模組
包含各種實用的輔助函數
"""
import math
import pygame
from .constants import COLORS

def distance(point1, point2):
    """計算兩點之間的距離"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def normalize_vector(vector):
    """正規化向量"""
    length = math.sqrt(vector[0]**2 + vector[1]**2)
    if length == 0:
        return (0, 0)
    return (vector[0] / length, vector[1] / length)

def angle_between_points(point1, point2):
    """計算兩點之間的角度（弧度）"""
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

def rotate_point(point, center, angle):
    """繞中心點旋轉點"""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    
    # 將點移到原點
    x = point[0] - center[0]
    y = point[1] - center[1]
    
    # 旋轉
    new_x = x * cos_angle - y * sin_angle
    new_y = x * sin_angle + y * cos_angle
    
    # 移回原位置
    return (new_x + center[0], new_y + center[1])

def clamp(value, min_value, max_value):
    """限制數值在指定範圍內"""
    return max(min_value, min(value, max_value))

def lerp(start, end, t):
    """線性插值"""
    return start + (end - start) * clamp(t, 0, 1)

def point_in_circle(point, center, radius):
    """檢查點是否在圓內"""
    return distance(point, center) <= radius

def point_in_rect(point, rect):
    """檢查點是否在矩形內"""
    return (rect[0] <= point[0] <= rect[0] + rect[2] and 
            rect[1] <= point[1] <= rect[1] + rect[3])

def circle_rect_collision(center, radius, rect):
    """檢查圓和矩形是否碰撞"""
    # 找到矩形上最接近圓心的點
    closest_x = clamp(center[0], rect[0], rect[0] + rect[2])
    closest_y = clamp(center[1], rect[1], rect[1] + rect[3])
    
    # 計算圓心到最近點的距離
    return distance(center, (closest_x, closest_y)) <= radius

def get_path_direction(current_pos, target_pos):
    """獲取從當前位置到目標位置的方向向量"""
    dx = target_pos[0] - current_pos[0]
    dy = target_pos[1] - current_pos[1]
    return normalize_vector((dx, dy))

def find_closest_enemy(tower_pos, enemies, max_range):
    """找到塔射程內最近的敵人"""
    closest_enemy = None
    closest_distance = float('inf')
    
    for enemy in enemies:
        dist = distance(tower_pos, enemy.position)
        if dist <= max_range and dist < closest_distance:
            closest_distance = dist
            closest_enemy = enemy
    
    return closest_enemy

def find_strongest_enemy(tower_pos, enemies, max_range):
    """找到塔射程內血量最多的敵人"""
    strongest_enemy = None
    max_health = 0
    
    for enemy in enemies:
        dist = distance(tower_pos, enemy.position)
        if dist <= max_range and enemy.health > max_health:
            max_health = enemy.health
            strongest_enemy = enemy
    
    return strongest_enemy

def find_fastest_enemy(tower_pos, enemies, max_range):
    """找到塔射程內最快的敵人"""
    fastest_enemy = None
    max_speed = 0
    
    for enemy in enemies:
        dist = distance(tower_pos, enemy.position)
        if dist <= max_range and enemy.speed > max_speed:
            max_speed = enemy.speed
            fastest_enemy = enemy
    
    return fastest_enemy

def calculate_lead_target(shooter_pos, target_pos, target_velocity, projectile_speed):
    """計算提前量射擊位置"""
    # 簡化的提前量計算
    target_speed = math.sqrt(target_velocity[0]**2 + target_velocity[1]**2)
    if target_speed == 0:
        return target_pos
    
    dist_to_target = distance(shooter_pos, target_pos)
    time_to_target = dist_to_target / projectile_speed
    
    # 預測目標未來位置
    future_x = target_pos[0] + target_velocity[0] * time_to_target
    future_y = target_pos[1] + target_velocity[1] * time_to_target
    
    return (future_x, future_y)

def grid_to_pixel(grid_x, grid_y, tile_size):
    """將格子座標轉換為像素座標"""
    return (grid_x * tile_size, grid_y * tile_size)

def pixel_to_grid(pixel_x, pixel_y, tile_size):
    """將像素座標轉換為格子座標"""
    return (pixel_x // tile_size, pixel_y // tile_size)

def is_valid_build_position(pos, path, existing_towers, tile_size):
    """檢查位置是否可以建造塔"""
    # 檢查是否在路徑上
    for path_point in path:
        if distance(pos, path_point) < tile_size:
            return False
    
    # 檢查是否與現有塔重疊
    for tower in existing_towers:
        if distance(pos, tower.position) < tile_size:
            return False
    
    return True

def draw_health_bar(screen, pos, current_health, max_health, width=30, height=4):
    """繪製血條"""
    if max_health <= 0:
        return
    
    health_ratio = current_health / max_health
    
    # 背景（紅色）
    bg_rect = pygame.Rect(pos[0] - width//2, pos[1] - height//2, width, height)
    pygame.draw.rect(screen, COLORS['RED'], bg_rect)
    
    # 前景（綠色）
    if health_ratio > 0:
        fg_width = int(width * health_ratio)
        fg_rect = pygame.Rect(pos[0] - width//2, pos[1] - height//2, fg_width, height)
        
        # 根據血量比例改變顏色
        if health_ratio > 0.6:
            color = COLORS['GREEN']
        elif health_ratio > 0.3:
            color = COLORS['YELLOW']
        else:
            color = COLORS['RED']
        
        pygame.draw.rect(screen, color, fg_rect)
    
    # 邊框
    pygame.draw.rect(screen, COLORS['WHITE'], bg_rect, 1)

def draw_range_circle(screen, center, radius, color=COLORS['WHITE'], alpha=50):
    """繪製射程圓圈"""
    # 創建透明表面
    range_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(range_surface, (*color[:3], alpha), (radius, radius), radius)
    pygame.draw.circle(range_surface, color, (radius, radius), radius, 2)
    
    # 繪製到螢幕上
    screen.blit(range_surface, (center[0] - radius, center[1] - radius))

def format_number(number):
    """格式化數字顯示"""
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}K"
    else:
        return str(int(number))

def create_gradient_surface(width, height, start_color, end_color):
    """創建漸層表面"""
    surface = pygame.Surface((width, height))
    
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    return surface

def ease_in_out(t):
    """緩入緩出函數"""
    return t * t * (3 - 2 * t)

def ease_out_bounce(t):
    """彈跳緩出函數"""
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

def shake_screen(intensity, duration, current_time):
    """計算螢幕震動偏移"""
    if current_time > duration:
        return (0, 0)
    
    progress = current_time / duration
    shake_intensity = intensity * (1 - progress)
    
    import random
    offset_x = random.randint(-int(shake_intensity), int(shake_intensity))
    offset_y = random.randint(-int(shake_intensity), int(shake_intensity))
    
    return (offset_x, offset_y)
