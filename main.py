import pygame
from utils import *

pygame.init()

screen_width = 1200
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Schelling's model")
screen.fill((255, 255, 255))


terminate = False

test_grid = Grid(21, 33, 1, 0.3, 0.2, 0.3, screen, screen_width, screen_height)
test_grid.grid_init()

pygame.display.flip()

while not terminate:
    test_grid.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate = True

    pygame.display.flip()

