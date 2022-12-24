import pygame
from utils import *

pygame.init()

# screen size
screen_width = 1200
screen_height = 800

# initialize screen window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Schelling's model")
screen.fill((255, 255, 255))


terminate = False

# create grid
test_grid = Grid(5, 5, 0.5, 0.2, 0.7, 0, screen, screen_width, screen_height)
test_grid.grid_init()

test = False

while not terminate:
    test_grid.draw()

    if test:
        test_grid.migration()
        test = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate = True

        if event.type == pygame.KEYDOWN:
            # if keydown event happened
            # than printing a string to output
            if event.key == pygame.K_SPACE:
                test = True

    pygame.display.flip()

