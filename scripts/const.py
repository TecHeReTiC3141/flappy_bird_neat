import pygame
from random import *
from math import *

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 800, 800
display = pygame.display.set_mode((10, 10))
GROUND_LEVEL = int(DISP_HEIGHT * .9)
LEVEL_FONT = pygame.font.Font(None, 50)