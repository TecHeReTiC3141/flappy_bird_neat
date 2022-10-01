import pygame
from scripts.const import *
from classes.bird import Bird

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Flappy_bird')
background_img = pygame.transform.scale(pygame.image.load('sprites/background-day.png'), (DISP_WIDTH, DISP_HEIGHT))

bird = Bird(DISP_WIDTH // 2, DISP_HEIGHT // 2)
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    display.blit(background_img, (0, 0))
    bird.draw(display)

    pygame.display.update()
    bird.update()

    clock.tick(60)
