from collections import deque
from classes.game_objects import *
from scripts.const import *


class Level:

    background_img = pygame.transform.scale(pygame.image.load('sprites/background-day.png'),
                                            (DISP_WIDTH, DISP_HEIGHT))

    def __init__(self):
        self.bird = Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2)
        self.pipes: deque[Pipe] = deque([])
        self.grounds = deque([Ground(0, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL),
                              Ground(DISP_WIDTH, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL)])
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.game_over = False

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        self.surface.blit(self.background_img, (0, 0))
        for pipe in self.pipes:
            pipe.draw(self.surface)
        for ground in self.grounds:
            ground.draw(self.surface)
        self.bird.draw(self.surface)
        if self.game_over:
            self.surface.blit(LEVEL_FONT.render("R", True, 'black'), (DISP_WIDTH // 2, DISP_HEIGHT // 4))
        self.surface.blit(LEVEL_FONT.render(f"DIST: {self.bird.dist // HOR_SPEED}", True, 'black'), (10, DISP_HEIGHT // 5))

        surface.blit(self.surface, (0, 0))

    def reload(self):
        self.bird = Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2)
        self.pipes: deque[Pipe] = deque([])
        self.grounds = deque([Ground(0, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL),
                              Ground(DISP_WIDTH, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL)])
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.game_over = False

    def game_cycle(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if not self.game_over and event.key == pygame.K_SPACE:
                    self.bird.jump()

                elif event.key == pygame.K_r and self.game_over:
                    self.reload()

        if not self.game_over:
            self.bird.update()

            for obj in self.grounds + self.pipes:
                obj.update(HOR_SPEED)
                if isinstance(obj, Pipe):
                    new_pipe, collided = obj.interact(self.bird)
                    if collided:
                        self.game_over = True
                        break
                    elif isinstance(new_pipe, Pipe):
                        self.pipes.append(new_pipe)
                else:
                    if obj.interact(self.bird):
                        self.game_over = True
                        break

            if self.grounds[0].rect.right <= 0:
                self.grounds[0].rect.left = DISP_WIDTH - 20
                self.grounds.append(self.grounds.popleft())

            if self.pipes and self.pipes[0].upper_pipe.rect.right <= 0:
                self.pipes.popleft()

            if self.bird.dist >= 150 and not self.pipes:
                self.pipes.append(Pipe(DISP_WIDTH + randint(20, 150), randint(DISP_HEIGHT // 4, DISP_HEIGHT // 2)))
