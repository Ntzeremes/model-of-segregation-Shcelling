import pygame
from utils import *

pygame.init()

# screen size
screen_width = 800
screen_height = 800

# initialize screen window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Schelling's model")
screen.fill((255, 255, 255))


terminate = False

# create grid
test_grid = Grid(30, 30, 0.5, 0.15, 0.3, 0.3, screen, screen_width, screen_height)
test_grid.grid_init()
print(test_grid.calculate_metrics())

test = False

while not terminate:
    test_grid.draw()

    if test:
        test_grid.migration()
        print(test_grid.calculate_metrics())
        test = False
        print()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate = True

        if event.type == pygame.KEYDOWN:
            # if keydown event happened
            # than printing a string to output
            if event.key == pygame.K_SPACE:
                test = True

    pygame.display.flip()

