import unittest
import pygame
from src.game.game_manager import GameManager
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class DummyScreen:
    def fill(self, color): pass
    def blit(self, img, pos): pass

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gm = GameManager(self.screen)

    def test_add_tower(self):
        from src.entities.towers.cannon_tower import CannonTower
        tower = CannonTower(120, 120, self.gm)
        self.gm.add_tower(tower)
        self.assertIn(tower, self.gm.towers)

    def test_add_enemy(self):
        from src.entities.enemies.basic_enemy import BasicEnemy
        enemy = BasicEnemy((4,0), self.gm)
        self.gm.add_enemy(enemy)
        self.assertIn(enemy, self.gm.enemies)

    def test_add_projectile(self):
        from src.entities.projectiles.cannon_ball import CannonBall
        from src.entities.enemies.basic_enemy import BasicEnemy
        enemy = BasicEnemy((4,0), self.gm)
        proj = CannonBall(100,100,enemy,10,self.gm)
        self.gm.add_projectile(proj)
        self.assertIn(proj, self.gm.projectiles)

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
