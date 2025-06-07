import pygame
from src.game.map_manager import MapManager
from src.game.wave_manager import WaveManager
from src.entities.towers.base_tower import BaseTower
from src.entities.enemies.base_enemy import BaseEnemy
from src.entities.projectiles.base_projectile import BaseProjectile
from src.ui.game_ui import GameUI
from src.utils.constants import INIT_MONEY, INIT_LIFE, BG_COLOR

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.entities = pygame.sprite.LayeredUpdates()
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.map_manager = MapManager(self)
        self.wave_manager = WaveManager(self)
        self.ui = GameUI(self)
        self.money = INIT_MONEY
        self.life = INIT_LIFE
        self.score = 0
        self.selected_tower_type = None
        self.game_over = False

    def handle_event(self, event):
        if self.ui.handle_event(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                pos = pygame.mouse.get_pos()
                if self.selected_tower_type:
                    placed = self.map_manager.place_tower(pos, self.selected_tower_type)
                    if placed:
                        self.money -= self.selected_tower_type.cost
                        self.selected_tower_type = None
                else:
                    self.ui.handle_click(pos)
            elif event.button == 3:  # right click
                self.selected_tower_type = None

    def update(self, dt):
        if self.game_over:
            return
        self.wave_manager.update(dt)
        self.entities.update(dt)
        self.check_collisions()
        self.ui.update(dt)
        if self.life <= 0:
            self.game_over = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.map_manager.draw(self.screen)
        self.entities.draw(self.screen)
        self.ui.draw(self.screen)

        # 畫所有敵人（這裡會顯示血條和百分比）
        for enemy in self.enemies:
            enemy.draw(self.screen)
        # 畫所有塔
        for tower in self.towers:
            tower.draw(self.screen)
        # ...畫UI等其他畫面

    def check_collisions(self):
        # 投射物擊中敵人
        for projectile in self.projectiles:
            hits = pygame.sprite.spritecollide(projectile, self.enemies, False)
            for enemy in hits:
                projectile.on_hit(enemy)
                if not projectile.piercing:
                    projectile.kill()
        # 敵人到達終點
        for enemy in self.enemies:
            if self.map_manager.is_enemy_at_end(enemy):
                self.life -= 1
                enemy.kill()

    def add_tower(self, tower: BaseTower):
        self.towers.add(tower)
        self.entities.add(tower)

    def add_enemy(self, enemy: BaseEnemy):
        self.enemies.add(enemy)
        self.entities.add(enemy)

    def add_projectile(self, projectile: BaseProjectile):
        self.projectiles.add(projectile)
        self.entities.add(projectile)

    def earn_money(self, amount):
        self.money += amount

    def add_score(self, val):
        self.score += val

    def is_game_over(self):
        return self.game_over

    def get_final_score(self):
        return self.score
