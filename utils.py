import random
import pygame


class Grid:
    def __init__(self, width, height, ratio, empty, thresh_a, thresh_b, screen, screen_width, screen_height):
        self.pad = 400
        self.width = width
        self.height = height
        self.size = width * height
        self.ratio = ratio
        self.empty = int(empty * width * height)
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.thresh_a = thresh_a
        self.thresh_b = thresh_b
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block = None
        self.top_pad = None
        self.left_pad = None

    def grid_init(self):
        """Initializes the grid w x h and fills it with group_a agents, group_b agents  and empty spaces at random.
        0 spaces will represent empty spaces
        1 spaces will represent group a agents
        2 spaces will represent group b agents
        """
        grid = [0] * self.size

        red = int((self.size - self.empty) * self.ratio / (self.ratio + 1))
        grey = self.size - self.empty - red

        for i in range(red):
            grid[i] = 1
        for i in range(red, red + grey):
            grid[i] = 2

        random.shuffle(grid)

        for t in range(self.size):
            i = t // self.width
            j = t % self.width
            if grid[t] == 0:
                self.grid[i][j] = Space((i, j))
            elif grid[t] == 1:
                self.grid[i][j] = Agent(1, (i, j), self.thresh_a, (130, 130, 130))
            else:
                self.grid[i][j] = Agent(2, (i, j), self.thresh_b, (185, 15, 15))

        self.block_calc()

    def print_grid(self):
        """prints the grid, for testing purposes."""
        for i in range(self.height):
            print(self.grid[i][:])

    def draw(self):
        self.draw_grid()
        self.draw_agents()
        pygame.draw.line(self.screen, (0, 0, 0), (self.screen_width - self.pad, 0),
                         (self.screen_width - self.pad, self.screen_height), 2)

    def draw_grid(self):
        self.screen.fill((245, 245, 245))

        for i in range(self.height + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (self.left_pad, i * self.block + self.top_pad),
                             (self.width * self.block + self.left_pad, i * self.block + self.top_pad), 1)
        for j in range(self.width + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (j * self.block + self.left_pad, self.top_pad),
                             (j * self.block + self.left_pad, self.height * self.block + self.top_pad), 1)

    def block_calc(self):
        """Calculates the block that will be used to create the grid."""
        if self.width > self.height:
            self.block = (self.screen_width - self.pad)/ self.width
        elif self.height > self.width:
            self.block = self.screen_height/ self.height
        else:
            self.block = self.screen_height/ self.height

        self.top_pad = (self.screen_height - self.height * self.block) / 2
        self.left_pad = (self.screen_width - self.pad - self.width * self.block) / 2

    def draw_agents(self):
        """Draws the agents in the grid"""
        for x in range(self.width):
            for y in range(self.height):
                a = self.grid[y][x]
                if isinstance(a, Agent):
                    pygame.draw.circle(self.screen, a.color,
                                     (x * self.block + self.block/2 + self.left_pad,
                                      y * self.block + self.block/2 + self.top_pad), self.block/2 - 1)


class Agent:
    """The agent belongs in one of the two groups  and has a specific position in the grid.
        The threshold value show the percentage of neighbors from all the neighbors around the agent (3 x 3 square )
        that belong  to the same group. Happiness is the current status of the agent depending on the neighbors if it
        is lower than the threshold the agent will change neighborhood. """

    def __init__(self, group, pos, threshold, color):
        self.group = group
        self.x = pos[0]
        self.y = pos[1]
        self.threshold = threshold
        self.happiness = None
        self.color = color

    def calc_happiness(self, width, height, grid):
        """percentage of neighbors that belong to the same group as the agent"""
        min_x = 0 if self.x == 0 else self.x - 1
        max_x = width if self.x == width else self.x + 1

        min_y = 0 if self.y == 0 else self.y - 1
        max_y = height if self.y == height else self.y + 1

        tot_neigh = 0
        same_group = 0

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                neigh = grid[i][j]
                if neigh != 0:
                    tot_neigh += 1
                    if neigh == self.group:
                        same_group += 1

        self.happiness = same_group / tot_neigh

    def __repr__(self):
        return str(self.group)


class Space:
    """It is the class that represents the empty space on which agents can move on."""

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.group_a = None
        self.group_b = None
        self.distance = None

    def cal_happiness(self, width, height, grid):
        """Calculates the percentage of each neighbor group around the empty space"""
        min_x = 0 if self.x == 0 else self.x - 1
        max_x = width if self.x == width else self.x + 1

        min_y = 0 if self.y == 0 else self.y - 1
        max_y = height if self.y == height else self.y + 1

        tot_neigh = 0
        group_a = 0
        group_b = 0

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                neigh = grid[i][j]
                if neigh == 1:
                    group_a += 1
                    tot_neigh += 1
                elif neigh == 2:
                    group_b += 1
                    tot_neigh += 1

        self.group_a = group_a
        self.group_b = group_b

    def calc_distance(self, agent_x, agent_y):
        """Calculates the distance from a specific agent"""
        self.distance = ((self.x - agent_x) ** 2 + (self.y - agent_y) ** 2) ** 0.5

    def __repr__(self):
        return "0"


