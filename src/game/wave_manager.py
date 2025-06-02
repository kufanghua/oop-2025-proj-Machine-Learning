"""
波數管理
負責生成敵人、管理波次進度
"""
class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.enemies = []

    def update(self, dt):
        # 更新所有敵人狀態
        for enemy in self.enemies:
            enemy.update(dt)
        # 移除死亡敵人
        self.enemies = [e for e in self.enemies if e.alive]

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

    def spawn_wave(self):
        # 產生新一波敵人
        self.current_wave += 1
        # TODO: 根據波數決定生成敵人數量與類型
