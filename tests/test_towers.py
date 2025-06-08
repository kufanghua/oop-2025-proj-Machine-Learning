import unittest
import pygame
from src.entities.towers.cannon_tower import CannonTower
from src.entities.towers.machine_tower import MachineTower
from src.entities.towers.freeze_tower import FreezeTower

class DummyGameManager:
    def __init__(self):
        self.enemies = []
        self.add_projectile_called = False
    def add_projectile(self, proj):
        self.add_projectile_called = True

class TestTowers(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.gm = DummyGameManager()

    def test_cannon_tower_shoot(self):
        tower = CannonTower(100, 100, self.gm)
        target = type("DummyEnemy", (), {"x":110,"y":110,"is_alive":lambda self:True})()
        self.gm.enemies = [target]
        tower.attack_cooldown = 0
        tower.update(0.2)
        self.assertTrue(self.gm.add_projectile_called)

    def test_machine_tower_shoot(self):
        tower = MachineTower(100, 100, self.gm)
        target = type("DummyEnemy", (), {"x":110,"y":110,"is_alive":lambda self:True})()
        self.gm.enemies = [target]
        tower.attack_cooldown = 0
        tower.update(0.2)
        self.assertTrue(self.gm.add_projectile_called)

    def test_freeze_tower_shoot(self):
        tower = FreezeTower(100, 100, self.gm)
        target = type("DummyEnemy", (), {"x":110,"y":110,"is_alive":lambda self:True})()
        self.gm.enemies = [target]
        tower.attack_cooldown = 0
        tower.update(0.2)
        self.assertTrue(self.gm.add_projectile_called)

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
