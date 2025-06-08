import pygame
import random
from src.entities.enemies.basic_enemy import BasicEnemy
from src.entities.enemies.fast_enemy import FastEnemy
from src.entities.enemies.tank_enemy import TankEnemy

class WaveManager:
    def __init__(self, game_manager, difficulty=None):
        self.game_manager = game_manager
        self.wave = 1
        self.spawn_timer = 0
        self.enemies_to_spawn = []
        self.wave_in_progress = False
        self.spawn_interval = 0.5  # seconds

        # 根據難度調整每波怪物基數
        if difficulty == "easy":
            self.enemies_per_wave = 5
        elif difficulty == "hard":
            self.enemies_per_wave = 12
        else:  # normal 或未指定
            self.enemies_per_wave = 8

    def update(self, dt):
        if not self.wave_in_progress:
            self.start_wave()
        if self.enemies_to_spawn:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                enemy_cls = self.enemies_to_spawn.pop(0)
                enemy = enemy_cls(self.game_manager.map_manager.path_tiles[0], self.game_manager)
                self.game_manager.add_enemy(enemy)
        else:
            # 本波怪已送完，等待全死才進下一波
            if len(self.game_manager.enemies) == 0:
                self.wave_in_progress = False
                self.wave += 1

    def start_wave(self):
        self.enemies_to_spawn = []
        num = self.enemies_per_wave + self.wave * 2
        for i in range(num):
            if self.wave < 3 or random.random() < 0.7:
                self.enemies_to_spawn.append(BasicEnemy)
            elif random.random() < 0.5:
                self.enemies_to_spawn.append(FastEnemy)
            else:
                self.enemies_to_spawn.append(TankEnemy)
        self.wave_in_progress = True