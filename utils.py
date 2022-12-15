import random
import pygame


class Grid:
    """The class that creates the grid and agents inside it

    parameters
    ******************************
    horizontal_spaces  : int
        The number of horizontal_spaces in the grid.
    vertical_spaces  : int
        The number of vertical_spaces  in the grid.
    ratio :  float
            the ration of  gray agents to red agents.
    empty : float
            the percentage of empty spaces in the grid.
    thresh_a : float
            the min percentage of same neighbours around red agents for them to stay in the same place.
    thresh_b : float
            the min percentage of same neighbours around grey agents for them to stay in the same place.
    """

    def __init__(self, horizontal_spaces, vertical_spaces, ratio,
                 empty, thresh_a, thresh_b, screen, screen_width, screen_height):
        self.right_pad = 400
        self.horizontal_spaces = horizontal_spaces
        self.vertical_spaces = vertical_spaces
        self.total_spaces = horizontal_spaces * vertical_spaces  # number of possible spaces inside grid
        self.ratio = ratio
        self.empty_spaces = int(empty * horizontal_spaces * vertical_spaces)
        self.grid = [[None for _ in range(self.horizontal_spaces)] for _ in range(self.vertical_spaces)]
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
        0  will represent empty spaces
        1  will represent group a agents
        2  will represent group b agents
        """

        # creating an empty list the size of possible spaces
        g = [0] * self.total_spaces

        # filling it with the  designated number of agents
        red = int((self.total_spaces - self.empty_spaces) * self.ratio / (self.ratio + 1))
        grey = self.total_spaces - self.empty_spaces - red

        for i in range(red):
            g[i] = 1
        for i in range(red, red + grey):
            g[i] = 2

        # and shuffling it
        random.shuffle(g)

        # filling the grid
        for t in range(self.total_spaces):
            i = t // self.horizontal_spaces
            j = t % self.horizontal_spaces
            if g[t] == 0:
                self.grid[i][j] = Space((i, j))
            elif g[t] == 1:
                self.grid[i][j] = Agent(1, (i, j), self.thresh_a, (130, 130, 130))
            else:
                self.grid[i][j] = Agent(2, (i, j), self.thresh_b, (185, 15, 15))

        # calculates the pixel size of the space block and saves it in self.block
        self.block_calc()

    def print_grid(self):
        """prints the grid, for testing purposes."""
        for i in range(self.vertical_spaces):
            print(self.grid[i][:])

    def draw(self):
        """Drawing grid lines and agents"""
        self.draw_grid()
        self.draw_agents()
        pygame.draw.line(self.screen, (0, 0, 0), (self.screen_width - self.right_pad , 0),
                         (self.screen_width - self.right_pad, self.screen_height), 2)

    def draw_grid(self):
        self.screen.fill((245, 245, 245))

        for i in range(self.vertical_spaces + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (self.left_pad, i * self.block + self.top_pad),
                             (self.horizontal_spaces * self.block + self.left_pad, i * self.block + self.top_pad), 1)
        for j in range(self.horizontal_spaces + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (j * self.block + self.left_pad, self.top_pad),
                             (j * self.block + self.left_pad, self.vertical_spaces * self.block + self.top_pad), 1)

    def block_calc(self):
        """Calculates the block that will be used to create the grid."""
        if self.horizontal_spaces > self.vertical_spaces:
            self.block = (self.screen_width - self.right_pad ) / self.horizontal_spaces
        elif self.vertical_spaces > self.horizontal_spaces:
            self.block = self.screen_height / self.vertical_spaces
        else:
            self.block = self.screen_height / self.vertical_spaces

        self.top_pad = (self.screen_height - self.vertical_spaces * self.block) / 2
        self.left_pad = (self.screen_width - self.right_pad - self.horizontal_spaces * self.block) / 2

    def draw_agents(self):
        """Draws the agents in the grid"""
        for x in range(self.horizontal_spaces):
            for y in range(self.vertical_spaces):
                a = self.grid[y][x]
                if isinstance(a, Agent):
                    pygame.draw.circle(self.screen, a.color,
                                       (x * self.block + self.block / 2 + self.left_pad,
                                        y * self.block + self.block / 2 + self.top_pad), self.block / 2 - 1)


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
