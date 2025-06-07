import pygame

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None, hp=1):
        super().__init__()
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.image = image if image else pygame.Surface((32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True

    def update(self, dt):
        """
        每幀自動呼叫，處理物件邏輯
        """
        pass

    def draw(self, surface):
        """
        畫出物件（僅本體，血條在子類覆寫）
        """
        surface.blit(self.image, self.rect.topleft)

    def take_damage(self, dmg):
        """
        受到傷害
        """
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            self.alive = False

    def kill(self):
        """
        從sprite group移除
        """
        super().kill()
        self.alive = False

    def is_alive(self):
        return self.alive
