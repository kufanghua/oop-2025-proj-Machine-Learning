import pygame
import os

class AudioManager:
    def __init__(self):
        self.sounds = {
            "shoot_cannon": pygame.mixer.Sound(os.path.join("assets", "sounds", "shoot_cannon.wav")),
            "shoot_machine": pygame.mixer.Sound(os.path.join("assets", "sounds", "shoot_machine.wav")),
            "shoot_freeze": pygame.mixer.Sound(os.path.join("assets", "sounds", "shoot_freeze.wav")),
            "enemy_die": pygame.mixer.Sound(os.path.join("assets", "sounds", "enemy_die.wav")),
            "tower_build": pygame.mixer.Sound(os.path.join("assets", "sounds", "tower_build.wav")),
            "upgrade": pygame.mixer.Sound(os.path.join("assets", "sounds", "upgrade.wav")),
        }

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
