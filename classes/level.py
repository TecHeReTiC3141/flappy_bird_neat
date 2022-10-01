from collections import deque
from classes.game_objects import *
from scripts.const import *


class Level:

    background_img = pygame.transform.scale(pygame.image.load('sprites/background-day.png'), (DISP_WIDTH, DISP_HEIGHT))

    def __init__(self):
        self.bird = Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2)
        self.pipes: deque[Pipe] = deque([])
        self.grounds = deque([Ground(0, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL),
                              Ground(DISP_WIDTH, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL)])
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.surface.set_colorkey('black')

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        self.surface.blit(self.background_img, (0, 0))
        for pipe in self.pipes:
            pipe.draw(self.surface)
        for ground in self.grounds:
            ground.draw(self.surface)
        self.bird.draw(self.surface)
        surface.blit(self.surface, (0, 0))

    def reload(self):
        self.bird = Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2)
        self.pipes: deque[Pipe] = deque([])
        self.grounds = deque([Ground(0, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL),
                              Ground(DISP_WIDTH, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL)])
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.surface.set_colorkey('black')

    def game_cycle(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

        self.bird.update()
        for obj in self.grounds + self.pipes:
            obj.update(self.bird.velocity.x)
            if obj.interact(self.bird):
                self.reload()
        if self.grounds[0].rect.right <= 0:
            self.grounds[0].rect.left = DISP_WIDTH - 20
            self.grounds.append(self.grounds.popleft())