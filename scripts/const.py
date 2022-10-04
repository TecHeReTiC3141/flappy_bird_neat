import pygame
from random import *
from math import *
from pathlib import Path
import neat

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 800, 800
display = pygame.display.set_mode((10, 10))
GROUND_LEVEL = int(DISP_HEIGHT * .9)
LEVEL_FONT = pygame.font.Font(None, 50)
HOR_SPEED = 10

config_path = Path('config-feedforward.txt')
