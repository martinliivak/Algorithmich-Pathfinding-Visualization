from queue import PriorityQueue
import numpy as np
from scipy.constants.constants import N_A


def heuristic(a, b):
    """
    Manhattan heuristic """
    r1, c1 = a
    r2, c2 = b
    return abs(r1 - r2) + abs(c1 - c2)


class JPS:
    """
    Implementation of Jump Point Search - an improvement of A*
    """

    def __init__(self, graph, start, goal):
        """
        Initializing all of the parameters necessary to solve the maze using JPS """
        self.graph = graph
        self.start = start
        self.goal = goal
        self.h, self.w = self.graph.shape
        self.h -= 1
        self.w -= 1

        self.frontier = PriorityQueue()
        self.frontier.put(start, 0)

        self.came_from = dict()
        self.cost_so_far = dict()

        self.cost_so_far[start] = 0

    def __next__(self):
        """
        This makes the solver work in a Python generator style fashion, allowing the visualizer to call next until
        None is returned, which signifies that the maze has been solved
        
        The Jump Point Search can Jump over straights. In this implementation, the condition of a straight is checked and based on that
        either a jump is made or the usual a* procedure is carried out. 
        """
        while not self.frontier.empty():
            current = self.frontier.get()

            if current == self.goal:
                break
            else:
                if self.is_straight(current):
                    current = self.preform_straight_jump(current)
                else:
                    self.usual_a_star(current)

            return current

    def __iter__(self):
        return self

    def usual_a_star(self, current):
        for next_item in self._get_neighbours(current):
            new_cost = self.cost_so_far[current] + 1
            if next_item not in self.cost_so_far or new_cost < self.cost_so_far[next_item]:
                self.cost_so_far[next_item] = new_cost
                priority = new_cost + heuristic(self.goal, next_item)
                self.frontier.put(next_item, priority)
                self.came_from[next_item] = current

    # Performs a check to see, if the neighbors and the point form a line
    def is_straight(self, current):
        current_neighbours = self._get_neighbours(current)
        if (len(current_neighbours) == 2):
            nei_a = current_neighbours[0]
            a_x, a_y = nei_a
            nei_b = current_neighbours[1]
            b_x, b_y = nei_b
            if (a_x == b_x or a_y == b_y):
                return True
        return False

    def preform_straight_jump(self, current):
        jump_path = []
        jump_path.append(current)
        summer = 1
        current_p = current
        while (self.is_straight(current_p) or current_p == self.goal):
            new_cost = self.cost_so_far[current_p] + 1
            next_point = self.get_next_in_line(current_p)
            if next_point not in self.cost_so_far or new_cost < self.cost_so_far[next_point]:
                self.cost_so_far[next_point] = new_cost
                self.came_from[next_point] = current_p
            current_p = next_point
            jump_path.append(current_p)
            summer += 1
        if (current_p != self.goal):
            # priority = self.cost_so_far[current_p] + heuristic(self.goal, current_p)
            self.usual_a_star(current_p)
            # self.frontier.put(current_p, priority)
        # print("Made a jump of length", summer)
        return jump_path

    # Assumes, that this is already a line
    def get_next_in_line(self, current):
        current_neighbours = self._get_neighbours(current)
        prev_node = self.came_from[current]
        if current_neighbours[0] == prev_node:
            return current_neighbours[1]
        else:
            return current_neighbours[0]

    def _get_neighbours(self, current):
        """
        A simple method to fetch the allowed neighbours of a given location in the maze """
        r, c = current
        neighbours = []

        if r - 1 >= 0 and self.graph[r - 1, c] != 1:
            neighbours.append((r - 1, c))

        if r + 1 <= self.h and self.graph[r + 1, c] != 1:
            neighbours.append((r + 1, c))

        if c - 1 >= 0 and self.graph[r, c - 1] != 1:
            neighbours.append((r, c - 1))

        if c + 1 <= self.w and self.graph[r, c + 1] != 1:
            neighbours.append((r, c + 1))

        return neighbours

    def get_path(self):
        """
        Source: Wikipedia (https://en.wikipedia.org/wiki/A*_search_algorithm)
        Returns the path from goal to start as a list
        """
        current_node = self.goal
        total_path = [current_node]
        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            total_path.append(current_node)

        return total_path

    @staticmethod
    def get_name():
        return "Jump Point Search"
