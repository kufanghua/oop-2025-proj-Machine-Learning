import unittest
import pygame
from src.entities.enemies.basic_enemy import BasicEnemy
from src.entities.enemies.fast_enemy import FastEnemy
from src.entities.enemies.tank_enemy import TankEnemy

class DummyGameManager:
    def __init__(self):
        self.map_manager = type("DummyMapManager", (), {"path_tiles":[(0,0),(0,1),(0,2)]})()
        self.money = 0
        self.score = 0
    def earn_money(self, val): self.money += val
    def add_score(self, val): self.score += val

class TestEnemies(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.gm = DummyGameManager()

    def test_basic_enemy_hp(self):
        e = BasicEnemy((0,0), self.gm)
        hp = e.hp
        e.take_damage(5)
        self.assertEqual(e.hp, hp-5)

    def test_fast_enemy_move(self):
        e = FastEnemy((0,0), self.gm)
        e.update(0.5)
        self.assertNotEqual((e.x, e.y), (0,0))

    def test_tank_enemy_reward(self):
        e = TankEnemy((0,0), self.gm)
        e.take_damage(999)
        self.assertGreater(self.gm.money, 0)
        self.assertGreater(self.gm.score, 0)

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
