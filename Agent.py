from os import path


class Agent: ##A class to represent an agent in a grid environment.
    def __init__(self, start_position, goal_position, environment):
        """
        Initializes the agent with a start position, a goal position, and the environment it operates in.
        """
        self.position = start_position
        self.goal = goal_position
        self.environment = environment
        self.path = self.plan_path()
        self.step_index = 0
    
    def astar(self, grid, start, end):
        """
        A* Pathfinding Algorithm to find the shortest path from start to end in a grid.
        """

        class Node:
            """A node class for A* Pathfinding"""

            def __init__(self, parent=None, position=None):
                self.parent = parent
                self.position = position
                self.g = 0  # Distance to start node
                self.h = 0  # Distance to goal node
                self.f = 0  # Total cost

            def __eq__(self, other):
                return self.position == other.position

        # Initialize start and end nodes
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until finding the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current node from open list and add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # If the goal is reached, return the path
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children from adjacent squares
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

                # Node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range of the grid
                if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0:
                    continue

                # Ensure walkable terrain
                if grid[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                if child in closed_list:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                if any(child == open_node and child.g > open_node.g for open_node in open_list):
                    continue

                # Add the child to the open list
                open_list.append(child)

        return []  # Return empty path if no path is found


    def plan_path(self):
        """
        Plans the path from the current position to the goal using the A* algorithm.
        """
        return self.astar(self.environment.grid, self.position, self.goal)
    
    def set_path(self, p):
        """
        Set a new path for this agent
        """
        self.path = p

    def move(self):
        """
        Moves the agent along the planned path by one step.
        """
        if self.step_index < len(self.path):
            new_position = self.path[self.step_index]

            # Check for collisions or dynamic obstacles in the new position
            if self.environment.is_position_free(new_position):
                self.environment.update_position(self.position, new_position)
                self.position = new_position
                self.step_index += 1
            else:
                # Recalculate the path if a collision or obstacle is detected
                new_path = self.plan_path()
                if new_path != []:
                    self.path = self.plan_path()
                    self.step_index = 1
    
    def move_back(self):
        """
        Moves back the agent along the planned path by one step.
        """
        if self.step_index < len(self.path) and self.step_index > 2:
            prev_position = self.path[self.step_index-2]

            # Check for collisions or dynamic obstacles in the new position
            if self.environment.is_position_free(prev_position):
                self.environment.update_position(self.position, prev_position)
                self.position = prev_position
                self.step_index -= 1

    def has_reached_goal(self):
        """
        Checks if the agent has reached its goal.
        """
        return self.position == self.goal

    def detect_collision(self, other_agent_position):
        """
        Detects potential collisions with another agent.
        """
        if self.step_index < len(self.path):
            next_position = self.path[self.step_index]
            return next_position == other_agent_position
        return False

    def handle_collision(self):
        """
        Handles collision by recalculating the path.
        """
        self.path = self.plan_path()
        self.step_index = 0

    def get_position(self):
        """
        Returns the position of this agent
        """
        return self.position

    def __repr__(self):
        """
        String representation of the agent's current state.
        """
        return f"Agent(Position: {self.position}, Goal: {self.goal})"
