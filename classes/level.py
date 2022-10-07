from collections import deque
from classes.game_objects import *
from scripts.const import *


class Level:

    background_img = pygame.transform.scale(pygame.image.load('sprites/background-day.png'),
                                            (DISP_WIDTH, DISP_HEIGHT))

    def __init__(self, genomes: list, config: neat.config.Config, cur_gen):
        self.birds: list[Bird] = [Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2, g, config) for _, g in genomes]
        self.pipes: deque[Pipe] = deque([Pipe(DISP_WIDTH + randint(20, 150),
                                              randint(DISP_HEIGHT // 4, DISP_HEIGHT // 2))])
        self.grounds = deque([Ground(0, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL),
                              Ground(DISP_WIDTH, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL)])
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.game_over = False
        self.genomes = genomes
        self.config = config
        self.pipes_passed = 0
        self.gen = cur_gen

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        self.surface.blit(self.background_img, (0, 0))

        for obj in self.pipes + self.grounds:
            obj.draw(self.surface)

        for bird in self.birds:
            if bird.alive:
                bird.draw(self.surface)

        self.surface.blit(LEVEL_FONT.render(f"Pipes passed: {self.pipes_passed}", True, 'black'),
                          (10, 30))
        self.surface.blit(LEVEL_FONT.render(f"GEN: {self.gen}", True, 'black'),
                          (10, 60))
        self.surface.blit(LEVEL_FONT.render(f"Birds left: {len([i for i in self.birds if i.alive])}",
                                            True, 'black'),
                          (10, 90))
        # self.surface.blit(LEVEL_FONT.render(f"DIST: {self.bird.fit // HOR_SPEED}", True, 'black'), (10, DISP_HEIGHT // 5))

        surface.blit(self.surface, (0, 0))

    def reload(self):
        self.birds: list[Bird] = [Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2, g, self.config)
                                  for _, g in self.genomes]
        self.pipes: deque[Pipe] = deque([])
        self.grounds = deque([Ground(0, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL),
                              Ground(DISP_WIDTH, GROUND_LEVEL, DISP_WIDTH, DISP_HEIGHT - GROUND_LEVEL)])
        self.surface = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.game_over = False

    def game_cycle(self) -> bool:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            # if event.type == pygame.KEYDOWN:
            #     if not self.game_over and event.key == pygame.K_SPACE:
            #         self.bird.jump()
            #
            #     elif event.key == pygame.K_r and self.game_over:
            #         self.reload()
        birds_alive = False

        for obj in self.grounds + self.pipes:
            obj.update(HOR_SPEED)

        for bird in self.birds:
            if not bird.alive:
                continue
            birds_alive = True
            bird.update()

            if bird.rect.y < 0:
                bird.alive = False
                bird.g.fitness -= 1
                continue

            for obj in self.grounds + self.pipes:
                if isinstance(obj, Pipe):
                    if obj.upper_pipe.rect.right < bird.rect.centerx:
                        continue
                    new_pipe, collided = obj.interact(bird)
                    if collided:
                        bird.alive = False
                        bird.g.fitness -= 1
                        break
                    elif isinstance(new_pipe, Pipe):
                        self.pipes.append(new_pipe)
                else:
                    if obj.interact(bird):
                        bird.alive = False
                        bird.g.fitness -= 1
                        break

            for obj in self.pipes:
                if obj.upper_pipe.rect.right >= bird.rect.centerx:
                    output = bird.net.activate((bird.rect.centery,
                                                abs(obj.upper_pipe.rect.bottom - bird.rect.y),
                                                abs(obj.lower_pipe.rect.top - bird.rect.bottom),
                                                ))
                    if output[0] >= THRESHOLD:
                        bird.jump()
                    break

        if self.grounds[0].rect.right <= 0:
            self.grounds[0].rect.left = DISP_WIDTH - 20
            self.grounds.append(self.grounds.popleft())

        if self.pipes and self.pipes[0].upper_pipe.rect.right <= 0:
            self.pipes.popleft()
            self.pipes_passed += 1

        return birds_alive