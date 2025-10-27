# Author: Vibo Huang 101187050
# Group: 15
# Project: COMP3106A F23 Project
# Version: 2.0.1

import random
import numpy as np
from Agent import*

class GridEnvironment:
    """
    A class to represent the grid-based environment for the agents.
    """
    def __init__(self, size): # Initialization and methods to manage grid state
        """
        Initializes the grid environment with a specified size.
        """
        self.size = size
        self.grid = np.zeros((size, size))  # 0 represents a free cell

    def is_position_free(self, position):
        """
        Checks if a given position on the grid is free (not occupied by an obstacle or another agent).
        """
        x, y = position
        return self.grid[x, y] == 0

    def update_position(self, old_position, new_position):
        """
        Updates the grid to reflect the movement of an agent from an old position to a new position.
        """
        self.grid[old_position] = 0  # Mark the old position as free
        self.grid[new_position] = 1  # Mark the new position as occupied

    def add_obstacle(self, position):
        """
        Adds an obstacle to a specified position on the grid.
        """
        self.grid[position] = -1  # -1 represents an obstacle

    def remove_obstacle(self, position):
        """
        Removes an obstacle from a specified position on the grid.
        """
        if self.grid[position] == -1:
            self.grid[position] = 0

    def display(self):
        """
        Displays the current state of the grid. 
        """        
        print("***********************************************************************************************************\n")
        print("Please note that for this graph x is the vertical coordinate (↓) and y is the horizontal coordinate (→)\n")
        print("***********************************************************************************************************\n")
        print("———————————————————\n")
        for i in self.grid:
            print("|", end = " ")
            for j in i:
                if j==0:
                    print("0",end = " ")
                elif j==1:
                    print("A",end = " ")
                elif j==-1:
                    print("W",end = " ")
            print("|\n")
        print("———————————————————\n")
        # print(self.grid)

    def __repr__(self):
        """
        String representation of the grid environment.
        """
        return f"GridEnvironment(Size: {self.size}x{self.size})"


    """
    other functions:
    """

    def collision_detection(self, agents):
        """
        Detects potential collisions between agents.

        :param agents: A list of agents in the environment.
        :return: A list of tuples, each containing two agents that are at risk of colliding.
        """
        collision_pairs = []
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                # Check if the next position of any two agents is the same
                if agents[i].step_index < len(agents[i].path) and agents[j].step_index < len(agents[j].path):
                    next_position_i = agents[i].path[agents[i].step_index]
                    next_position_j = agents[j].path[agents[j].step_index]
                    if next_position_i == next_position_j:
                        collision_pairs.append((agents[i], agents[j]))
                    if next_position_i == agents[j].get_position() and next_position_j == agents[i].get_position(): # head-on collision
                        collision_pairs.append((agents[i], agents[j]))
        return collision_pairs
    
    def all_agents_at_goals(self, agents):
        """
        Checks if all agents have reached their goals.

        :param agents: A list of Agent objects.
        :return: True if all agents have reached their goals, False otherwise.
        """
        return all(agent.has_reached_goal() for agent in agents)


    def main_simulation_loop(self):
        # Main loop to run the simulation
        right_of_way = False

        # Update environment and plan paths
        for agent in agents:
            agent.plan_path()

        while not environment.all_agents_at_goals(agents):
            # Detect and handle potential collisions
            collisions = environment.collision_detection(agents)
            if collisions != []:
                print("Potential Collision at: " + str(collisions))
                for agent1, agent2 in collisions:
                    agent1.move_back()
                    agent2.move()
                    right_of_way = True

            # Move agents by default
            if right_of_way == False:
                for agent in agents:
                    agent.move()
            right_of_way = False
            
            environment.display()
        print("** End of Program **")


# Instantiate environment and agents
environment = GridEnvironment(8)

# # Test case 0: start and end location is not in a wall
# agent_configs = [((0, 0), (7, 7))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
# environment.add_obstacle((0,0))


# # Test case 1: one-agent cross over
# agent_configs = [((0, 0), (7, 7))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).

# # Test case 2: two-agent cross over
# agent_configs = [((0, 0), (7, 7)), ((5, 0), (0, 7))] 

# # Test case 3: one-agent with obstacles
# agent_configs = [((0, 0), (7, 7))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
# for i in range(7):
#     environment.add_obstacle((i,3))

# Test case 4: two-agent potential collision with 1 flexible path
# agent_configs = [((0, 0), (7, 7)), ((0, 7), (7, 0))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
# for i in range(3):
#     environment.add_obstacle((7-i,3))
# for i in range(3):
#     environment.add_obstacle((i,3))

# # Test case 5: two-agent potential collision with NO flexible path
# agent_configs = [((0, 0), (7, 7)), ((0, 7), (7, 0))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
# for i in range(4):
#     environment.add_obstacle((7-i,3))
# for i in range(3):
#     environment.add_obstacle((i,3))

# # Test case 6: Double wall test, test two-agent potential collision with NO flexible path, the only path is also along the edge of the graph
# agent_configs = [((0, 0), (7, 7)), ((0, 7), (7, 0))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
# for i in range(7):
#     environment.add_obstacle((i,3))
#     environment.add_obstacle((i,4)) 

# Test case 7: Complex environment for 2 agent
agent_configs = [((0, 0), (7, 7)), ((7, 7), (7, 0))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
for i in range(4):
    environment.add_obstacle((i,1))
    environment.add_obstacle((i,3))
    environment.add_obstacle((i,5))
for i in range(3):
    environment.add_obstacle((7-i,1))
    environment.add_obstacle((7-i,3))
    environment.add_obstacle((7-i,5))

# # Test case 8: 3 agent test
# agent_configs = [((0, 0), (7, 7)), ((7, 7), (0, 0)), ((7, 1), (0, 3))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).

# Test case 9: Complex environment for 3 agent
# agent_configs = [((0, 0), (7, 7)), ((7, 7), (0, 0)), ((7, 0), (0, 6))] # List of agent (as tuples) and their starting position and goal position. For example agent1 has a starting position of (0,0) and a goal position of (5,5).
# for i in range(4):
#     environment.add_obstacle((i,2))
#     environment.add_obstacle((i,5))
# for i in range(3):
#     environment.add_obstacle((7-i,2))
#     environment.add_obstacle((7-i,5))
# environment.add_obstacle((3,3))
# environment.add_obstacle((3,4))
# environment.add_obstacle((5,3))
# environment.add_obstacle((5,4))


"""
Check valid location (do not uncomment theses) and run the code if all valid
"""
invalid_inital_location = False
for ag in agent_configs:
    for k in range(len(agent_configs)):
        if environment.grid[ag[0]] == -1 or environment.grid[ag[1]] == -1: # check if the starting/end location of an agent is a wall
            invalid_inital_location = True
            break

if invalid_inital_location:
    print("The start or end location of an agent is inside a wall! or overlap by another agent. Please re-check your inital locations.")
else:
    # create the agents along with an internal model of the environment.
    agents = [Agent(start, goal, environment) for start, goal in agent_configs]

    # Run the simulation
    environment.main_simulation_loop()
