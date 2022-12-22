import random
import pygame
import math

full_rads = 2 * math.pi


class Grid:
    """The class that creates the grid and agents inside it

    parameters
    ******************************
    horizontal_spaces  : int
        The number of horizontal_spaces in the grid.
    vertical_spaces  : int
        The number of vertical_spaces  in the grid.
    ratio :  float
            the ration of  O agents to X agents.
    empty : float
            the percentage of empty spaces in the grid.
    thresh_a : float
            the min percentage of same neighbours around O agents for them to stay in the same place.
    thresh_b : float
            the min percentage of same neighbours around X agents for them to stay in the same place.
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
        self.side_pad = None

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

        # O is 1 in grid
        for i in range(red):
            g[i] = 1
        # X is 2 in grid
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
            elif g[t] == 1:  # greys
                self.grid[i][j] = Agent(1, (i, j))
            else:  # reds
                self.grid[i][j] = Agent(2, (i, j))

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
        pygame.draw.line(self.screen, (0, 0, 0), (self.screen_width - self.right_pad, 0),
                         (self.screen_width - self.right_pad, self.screen_height), 2)

    def draw_grid(self):
        self.screen.fill((245, 245, 245))

        for i in range(self.vertical_spaces + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (self.side_pad, i * self.block + self.top_pad),
                             (self.horizontal_spaces * self.block + self.side_pad, i * self.block + self.top_pad), 1)
        for j in range(self.horizontal_spaces + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (j * self.block + self.side_pad, self.top_pad),
                             (j * self.block + self.side_pad, self.vertical_spaces * self.block + self.top_pad), 1)

    def block_calc(self):
        """Calculates the block that will be used to create the grid."""
        if self.horizontal_spaces > self.vertical_spaces:
            self.block = (self.screen_width - self.right_pad) / self.horizontal_spaces
        elif self.vertical_spaces > self.horizontal_spaces:
            self.block = self.screen_height / self.vertical_spaces
        else:
            self.block = self.screen_height / self.vertical_spaces

        # creates a top pad if horizontal spaces are more than vertical
        self.top_pad = (self.screen_height - self.vertical_spaces * self.block) / 2
        # creates a side pad if horizontal spaces are more than vertical
        self.side_pad = (self.screen_width - self.right_pad - self.horizontal_spaces * self.block) / 2

    def draw_agents(self):
        """Draws the agents in the grid"""
        for x in range(self.horizontal_spaces):
            for y in range(self.vertical_spaces):
                a = self.grid[y][x]
                if a.group == 1:
                    pygame.draw.arc(self.screen, (0, 0, 0),
                                    (x * self.block + self.side_pad + 2,
                                     y * self.block + self.top_pad + 2, self.block - 2, self.block - 2),
                                    0, full_rads, width=3)

                elif a.group == 2:
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (self.side_pad + x * self.block + 1, self.top_pad + y * self.block + 1),
                                     (self.side_pad + x * self.block + self.block - 1,
                                      self.top_pad + y * self.block + self.block - 1), 3)
                    pygame.draw.line(self.screen, (0, 0, 0), (x * self.block + self.block + self.side_pad - 1,
                                                              self.top_pad + y * self.block + 1),
                                     (x * self.block + self.side_pad + 1,
                                      y * self.block + self.block + self.top_pad - 1), 3)

    def migration(self):
        """Starting from the first cell of the grid and moving on, checks if each agent is satisfied in his current
        position by comparing tolerance with threshold. Moves the agents that are not happy to new spaces that satisfy
        their thresholds

        :return: None
        """

        for j in range(self.vertical_spaces):
            for i in range(self.horizontal_spaces):
                obj = self.grid[j][i]

                # if obj.group is not 0 it must be an agent
                # noinspection PyUnresolvedReferences
                if obj.group != 0:
                    # calculate the current tolerance and compare it to threshold
                    # noinspection PyUnresolvedReferences
                    if obj.group == 1:
                        # checking threshold
                        if obj.calc_tolerance() > self.thresh_a:  # move agent

                            # search for nearest free space with acceptable tolerance

                            pass

    def free_space(self, agent):
        """
        Searches the area around an agent progressively to find and empty space with tolerance bellow the agents
        threshold.

        :param agent: the object agent that needs to migrate.
        :return: tuple - the position of the available space that the agent can migrate.
        """
        x = agent.x
        y = agent.y

        min_x = 0 if x == 0 else x - 1
        max_x = self.horizontal_spaces if x == self.horizontal_spaces else x + 1

        min_y = 0 if y == 0 else y - 1
        max_y = self.vertical_spaces if y == self.vertical_spaces else y + 1


class Agent:
    """The agent belongs in one of the two groups  and has a specific position in the grid.
        The threshold value show the percentage of neighbors from all the neighbors around the agent (3 x 3 square )
        that belong  to the same group. Happiness is the current status of the agent depending on the neighbors if it
        is lower than the threshold the agent will change neighborhood. """

    def __init__(self, group, pos):
        self.group = group
        self.x = pos[0]
        self.y = pos[1]
        self.happiness = None

    def calc_tolerance(self, width, height, grid):
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
        self.group = 0
        self.x = pos[0]
        self.y = pos[1]
        self.group_a = None
        self.group_b = None
        self.distance = None

    def calc_tolerance(self, width, height, grid):
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

    def __repr__(self):
        return "0"
