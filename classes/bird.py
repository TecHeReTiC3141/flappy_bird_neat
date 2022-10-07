from scripts.const import *


class Bird:

    falling_momentum = .25
    speed = 8
    jump_strength = -speed * 3 / 4
    images = [
        pygame.transform.scale2x(pygame.image.load(f'sprites/redbird-{i}flap.png').convert_alpha())
        for i in ['down', 'mid', 'up']
    ]

    def __init__(self, x, y, genome: neat.DefaultGenome, config):
        # for img in self.images:
        #     img.set_alpha(128)
        self.rect = self.images[0].get_rect(center=(x, y))
        self.anim_tick = 0
        self.g = genome
        self.g.fitness = 0
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.alive = True
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.acceleration = pygame.math.Vector2(0, self.falling_momentum)
        self.mask = pygame.mask.from_surface(self.images[0])

    def update(self):
        self.anim_tick += 1
        self.g.fitness += .1
        self.rect.move_ip((0, self.velocity.y))
        self.velocity.y = min(self.velocity.y + self.acceleration.y, self.speed * .9)
        self.velocity.x = sqrt(self.speed ** 2 - self.velocity.y ** 2)

    def draw(self, surface: pygame.Surface):
        angle = degrees(acos(self.velocity.x / self.speed))
        if self.velocity.y > 0:
            angle = 360 - angle
        rotated_surf = pygame.transform.rotate(self.images[self.anim_tick % 6 // 2
        if self.velocity.y <= self.speed // 4 else 0], angle)
        self.mask = pygame.mask.from_surface(rotated_surf)
        surface.blit(rotated_surf, self.rect)

    def jump(self):
        self.velocity.y = self.jump_strength
        self.velocity.x = sqrt(self.speed ** 2 - self.velocity.y ** 2)
