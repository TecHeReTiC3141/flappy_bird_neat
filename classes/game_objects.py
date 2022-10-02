from classes.bird import Bird
from scripts.const import *


class GameObject:

    image: pygame.Surface

    def __init__(self, x, y, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed):
        self.rect.move_ip(-speed, 0)

    def interact(self, player: Bird) -> bool:
        if self.rect.colliderect(player.rect):
            offset = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            over = self.mask.overlap_area(player.mask, offset)
            print(over)
            return over > 0
        return False

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class UpperPipe(GameObject):
    image = pygame.transform.scale2x(pygame.transform.rotate(pygame.image.load('sprites/pipe-green.png').convert_alpha(), 180))


class LowerPipe(GameObject):
    image = pygame.transform.scale2x(pygame.image.load('sprites/pipe-green.png')).convert_alpha()


class Pipe(GameObject):
    default_size = LowerPipe.image.get_size()

    def __init__(self, x, hole_y):
        hole_height = randint(180, 225)
        self.passed = False
        self.upper_pipe = UpperPipe(x, hole_y - self.default_size[1], *self.default_size)
        self.lower_pipe = LowerPipe(x, hole_y + hole_height, *self.default_size)

    def update(self, speed):
        self.upper_pipe.update(speed)
        self.lower_pipe.update(speed)
        if self.upper_pipe.rect.right <= 0:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        self.upper_pipe.draw(surface)
        self.lower_pipe.draw(surface)

    def interact(self, player: Bird) -> tuple['Pipe', bool]:
        new_pipe: Pipe = None
        if not self.passed and player.rect.centerx >= self.upper_pipe.rect.centerx:
            self.passed = True
            new_pipe = Pipe(DISP_WIDTH + randint(50, 150), randint(DISP_HEIGHT // 3, DISP_HEIGHT // 2))
        return (new_pipe, self.upper_pipe.interact(player)
                or self.lower_pipe.interact(player))


class Ground(GameObject):

    image = pygame.image.load('sprites/base.png').convert_alpha()
