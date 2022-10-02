from classes.level import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Flappy_bird')

level = Level()
clock = pygame.time.Clock()

while True:

    level.draw(display)

    level.game_cycle()
    pygame.display.update()

    clock.tick(60)
