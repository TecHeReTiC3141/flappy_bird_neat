import pygame
from math import *

class Bird:

    falling_momentum = .25
    speed = 10
    jump_strength = -speed * 3 / 4
    images = [
        pygame.transform.scale2x(pygame.image.load(f'sprites/redbird-{i}flap.png')) for i in ['down', 'mid', 'up']
    ]

    def __init__(self, x, y):
        for img in self.images:
            img.set_colorkey('black')
        self.rect = self.images[0].get_rect(center=(x, y))
        self.anim_tick = 0
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.acceleration = pygame.math.Vector2(0, self.falling_momentum)

    def update(self):
        self.anim_tick += 1
        self.rect.move_ip((0, self.velocity.y))
        self.velocity.y = min(self.velocity.y + self.acceleration.y, self.speed * .9)
        self.velocity.x = sqrt(self.speed ** 2 - self.velocity.y ** 2)

    def draw(self, surface: pygame.Surface):
        angle = degrees(acos(self.velocity.x / self.speed))
        if self.velocity.y > 0:
            angle = 360 - angle
        rotated_surf = pygame.transform.rotate(self.images[self.anim_tick % 6 // 2], angle)
        surface.blit(rotated_surf, self.rect)

    def jump(self):
        print('jump')
        self.velocity.y = self.jump_strength
        self.velocity.x = sqrt(self.speed ** 2 - self.velocity.y ** 2)