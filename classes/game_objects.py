from classes.bird import Bird
from scripts.const import *


class GameObject:

    image: pygame.Surface

    def __init__(self, x, y, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True

    def update(self, speed):
        self.rect.move_ip(-speed, 0)

    def interact(self, player: Bird):
        return self.rect.colliderect(player.rect)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class UpperPipe(GameObject):
    image = pygame.transform.rotate(pygame.image.load('sprites/pipe-green.png').convert_alpha(), 180)


class LowerPipe(GameObject):
    image = pygame.image.load('sprites/pipe-green.png').convert_alpha()


class Pipe(GameObject):
    default_size = LowerPipe.image.get_size()

    def __init__(self, x, y, hole_y):
        hole_height = random.randint(80, 100)
        self.upper_pipe = UpperPipe(x, hole_y - self.default_size[1], *self.default_size)
        self.lower_pipe = LowerPipe(x, hole_y + hole_height, *self.default_size)

    def update(self, speed):
        self.upper_pipe.rect.update(speed)
        self.lower_pipe.rect.update(speed)
        if self.upper_pipe.rect.right <= 0:
            self.alive = False


class Ground(GameObject):

    image = pygame.image.load('sprites/base.png').convert_alpha()