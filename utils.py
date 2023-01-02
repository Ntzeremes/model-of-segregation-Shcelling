import random
import pygame
import math
import random

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
            the percentage of possible spaces filled with  O agents.
    empty : float
            the percentage of empty spaces in the grid.
    thresh_a : float
            the min percentage of same neighbours around O agents for them to stay in the same place.
    thresh_b : float
            the min percentage of same neighbours around X agents for them to stay in the same place.
    """

    def __init__(self, horizontal_spaces, vertical_spaces, ratio,
                 empty, thresh_a, thresh_b, screen, screen_width, screen_height):
        self.horizontal_spaces = horizontal_spaces
        self.vertical_spaces = vertical_spaces
        self.total_spaces = horizontal_spaces * vertical_spaces  # number of possible spaces inside grid
        self.ratio = ratio
        self.empty_spaces = int(empty * horizontal_spaces * vertical_spaces)
        self.grid = [[0 for _ in range(self.horizontal_spaces)] for _ in range(self.vertical_spaces)]
        self.space_array = []
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
        o = int((self.total_spaces - self.empty_spaces) * self.ratio)
        x = self.total_spaces - self.empty_spaces - o

        # O is 1 in grid
        for i in range(o):
            g[i] = 1
        # X is 2 in grid
        for i in range(o, o + x):
            g[i] = 2

        random.seed(1)
        # and shuffling it
        random.shuffle(g)

        # filling the grid
        for t in range(self.total_spaces):
            i = t // self.horizontal_spaces
            j = t % self.horizontal_spaces
            if g[t] == 0:
                self.space_array.append(Space((j, i)))
            elif g[t] == 1:  # 0 agents
                self.grid[i][j] = Agent(1, (j, i))
            else:  # x agents
                self.grid[i][j] = Agent(2, (j, i))

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
        pygame.draw.line(self.screen, (0, 0, 0), (self.screen_width, 0),
                         (self.screen_width, self.screen_height), 2)

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
            self.block = self.screen_width / self.horizontal_spaces
        elif self.vertical_spaces > self.horizontal_spaces:
            self.block = self.screen_height / self.vertical_spaces
        else:
            self.block = self.screen_height / self.vertical_spaces

        # creates a top pad if horizontal spaces are more than vertical
        self.top_pad = (self.screen_height - self.vertical_spaces * self.block) / 2
        # creates a side pad if horizontal spaces are more than vertical
        self.side_pad = (self.screen_width - self.horizontal_spaces * self.block) / 2

    def draw_agents(self):
        """Draws the agents in the grid"""
        for x in range(self.horizontal_spaces):
            for y in range(self.vertical_spaces):
                a = self.grid[y][x]
                if isinstance(a, Agent):
                    if a.group == 1:
                        pygame.draw.arc(self.screen, (255, 0, 0),
                                        (x * self.block + self.side_pad + 2,
                                         y * self.block + self.top_pad + 2, self.block - 2, self.block - 2),
                                        0, full_rads, width=3)

                    elif a.group == 2:
                        pygame.draw.line(self.screen, (0, 0, 255),
                                         (self.side_pad + x * self.block + 1, self.top_pad + y * self.block + 1),
                                         (self.side_pad + x * self.block + self.block - 1,
                                          self.top_pad + y * self.block + self.block - 1), 3)
                        pygame.draw.line(self.screen, (0, 0, 255), (x * self.block + self.block + self.side_pad - 1,
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
                if obj != 0:
                    # calculate the current tolerance and compare it to threshold
                    # noinspection PyUnresolvedReferences
                    tolerance = obj.calc_tolerance(self.horizontal_spaces, self.vertical_spaces, self.grid)
                    if obj.group == 1:
                        # checking threshold
                        if tolerance < self.thresh_a:
                            new_y, new_x = self.free_space(obj)
                            if new_y is not None:
                                self.grid[new_y][new_x] = Agent(1, (new_x, new_y))

                                self.grid[j][i] = 0
                                self.space_array.insert(0, Space((i, j)))

                    else:
                        if tolerance < self.thresh_b:
                            new_y, new_x = self.free_space(obj)
                            if new_y is not None:
                                self.grid[new_y][new_x] = Agent(2, (new_x, new_y))

                                self.grid[j][i] = 0

                                self.space_array.insert(0, Space((i, j)))

    def free_space(self, agent):
        """
        Checks the array of spaces for any available space the distance and threshold to find and empty space with
        tolerance bellow the agents threshold and returns it

        :param agent: the object agent that needs to migrate.
        :return: tuple - the position of the available space that the agent can migrate.
        """

        best_space = None
        pos = None
        min_dist = 1000

        agent_threshold = self.thresh_a if agent.group == 1 else self.thresh_b

        for i, space in enumerate(self.space_array):
            new_tolerance = space.calc_tolerance(self.horizontal_spaces,
                                                 self.vertical_spaces,
                                                 self.grid, agent)
            if space.calc_distance(agent) < min_dist and new_tolerance > agent_threshold:
                min_dist = space.calc_distance(agent)
                best_space = space
                pos = i

        if best_space:
            del self.space_array[pos]

            return best_space.y, best_space.x

        return None, None

    def calculate_metrics(self):
        happy = 0
        tolerance_tot = 0
        for j in range(self.vertical_spaces):
            for i in range(self.horizontal_spaces):
                if self.grid[j][i] != 0:
                    agent = self.grid[j][i]
                    tolerance = agent.calc_tolerance(self.horizontal_spaces, self.vertical_spaces, self.grid)

                    tolerance_tot += tolerance

                    if agent.group == 1:
                        if tolerance >= self.thresh_a:
                            happy += 1
                    else:
                        if tolerance >= self.thresh_b:
                            happy += 1
        hap = happy/(self.vertical_spaces * self.horizontal_spaces - self.empty_spaces)
        tol = tolerance_tot/(self.vertical_spaces * self.horizontal_spaces - self.empty_spaces)
        return hap, tol


class Agent:
    """The agent belongs in one of the two groups  and has a specific position in the grid.
        The threshold value show the percentage of neighbors from all the neighbors around the agent (3 x 3 square )
        that belong  to the same group. Happiness is the current status of the agent depending on the neighbors if it
        is lower than the threshold the agent will change neighborhood. """

    def __init__(self, group, pos):
        self.group = group
        self.x = pos[0]
        self.y = pos[1]

    def calc_tolerance(self, width, height, grid):
        """percentage of neighbors that belong to the same group as the agent"""
        min_x = 0 if self.x == 0 else self.x - 1
        max_x = width if self.x + 1 == width else self.x + 2

        min_y = 0 if self.y == 0 else self.y - 1
        max_y = height if self.y + 1 == height else self.y + 2

        tot_neigh = 0
        same_group = 0
        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                neigh = grid[j][i]
                if neigh != 0:
                    tot_neigh += 1
                    if neigh.group == self.group:
                        same_group += 1

        return (same_group - 1) / (tot_neigh - 1) if tot_neigh - 1 != 0 else 0

    def __repr__(self):
        return str(self.group)


class Space:
    """It is the class that represents the empty space on which agents can move on."""

    def __init__(self, pos):
        self.group = 0
        self.x = pos[0]
        self.y = pos[1]

    def calc_tolerance(self, width, height, grid, agent):
        """Calculates the percentage of each neighbor group around the empty space"""
        min_x = 0 if self.x == 0 else self.x - 1
        max_x = width if self.x + 1 == width else self.x + 2

        min_y = 0 if self.y == 0 else self.y - 1
        max_y = height if self.y + 1 == height else self.y + 2

        tot_neigh = 0
        group_neigh = 0
        agent_group = agent.group
        ag_x = agent.x
        ag_y = agent.y
        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                neigh = grid[j][i]
                if neigh != 0:
                    if not (j == ag_y and i == ag_x):
                        tot_neigh += 1
                        if neigh.group == agent_group:
                            group_neigh += 1

        return group_neigh / tot_neigh if tot_neigh != 0 else 0

    def calc_distance(self, agent):
        """Calculates the  manhatan distance from a specific agent"""
        return abs(self.x - agent.x) + abs(self.y - agent.y)

    def __repr__(self):
        return "0"
