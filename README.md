# Overview

In 1971, the American economist Thomas Schelling created an agent-based model that suggested inadvertent behavior might also contribute to segregation. His model of segregation showed that even when individuals (or "agents") didn't mind being surrounded or living by agents of a different race or economic background, they would still choose to segregate themselves from other agents over time! Although the model is quite simple, it provides a fascinating look at how individuals might self-segregate, even when they have no explicit desire to do so.

**macro- level behaviours might not represent micro-level behaviours** 

# How the model works

Schelling's model will now be explained with some minor changes. Suppose there are two types of agents: X and O. The two types of agents might represent different
races, ethnicity, economic status, etc. Two populations of the two agent types are initially placed into random locations of a neighborhood represented by a grid. After placing all the agents in the grid, each cell is either occupied by an agent or is empty as shown below.

-15x15 grid created as an example
![Screenshot 2023-01-01 171857](https://user-images.githubusercontent.com/88309714/210175875-52a0f269-4410-4438-a16b-8be2959edfbc.png)

Each type of agent has a threshold value that expresses what percentage of it's surrounding neighbors (3x3 square) are of the same type. If the percentage of the neighbors is lower than the threshold the agent is disatisfied.

When an agent is not satisfied, it can be moved to any vacant location in the grid. Any algorithm can be used to choose this new location. For example, a randomly selected cell may be chosen, or the agent could move to the nearest available location. In our case it chooses the latter.


The dissatisfied agents are moving to new places during rounds. At the beggining of of each round starting from the the start of the grid an algorithm checks each grid space. If it is an agent it calculates the tolerance value and compares it with the threshold. If it is lower than it, searches for the nearest available empty space that satisfies the threshold and moves the agent there.

All dissatisfied agents must be moved in the same round. After the round is complete, a new round begins, and dissatisfied agents are once again moved to new locations in the grid. These rounds continue until all agents in the neighborhood are satisfied with their location. Bellow is the initial grid when it reaches equilibrium.

![Screenshot 2023-01-01 171932](https://user-images.githubusercontent.com/88309714/210175880-aedebfe1-b65e-4a17-b13c-56816ee03d30.png)

# Links

wiki link : https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation

Shelling's paper : https://www.jstor.org/stable/1823701

extract from Model Thinking course by Scott E.Page : https://www.youtube.com/watch?v=42STyM7RfrU&ab_channel=ActuarialScience
