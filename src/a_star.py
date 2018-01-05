from queue import PriorityQueue
import numpy as np


def heuristic(a, b):
    """
    Manhattan heuristic
    """
    r1, c1 = a
    r2, c2 = b
    return abs(r1 - r2) + abs(c1 - c2)


def heuristic_euc(a, b):
    """
    Source: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html"""
    r1, c1 = a
    r2, c2 = b
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    return np.sqrt(dr * dr + dc * dc)


class AStar():
    """
    A-star algorithm solver for maze graph
    """

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.h, self.w = self.graph.shape
        self.h -= 1
        self.w -= 1

        self.closed_set = set()
        self.open_set = set()
        self.open_set.add(start)

        self.came_from = {}

        self.g_score = {}
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                self.g_score[(j, i)] = float("inf")

        self.g_score[start] = 0

        self.f_score = self.g_score.copy()
        self.f_score[start] = heuristic(start, goal)

    def __iter__(self):
        return self

    def __next__(self):
        while len(self.open_set) != 0:
            current = min(self.open_set, key=self.f_score.get)
            if current == self.goal:
                break

            self.open_set.remove(current)
            self.closed_set.add(current)

            # Find the proper "neighbours" of this "current" point
            for neighbour in self._get_neighbours(current):
                if neighbour in self.closed_set:
                    continue

                if neighbour not in self.open_set:
                    self.open_set.add(neighbour)

                # tentative_g_score = self.g_score[current] + self.dist(current, neighbour)
                tentative_g_score = self.g_score[current] + 1
                if tentative_g_score >= self.g_score[neighbour]:
                    continue

                self.came_from[neighbour] = current
                self.g_score[neighbour] = tentative_g_score
                self.f_score[neighbour] = self.g_score[neighbour] + heuristic(neighbour, self.goal)

            return current

    def _get_neighbours(self, current):
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
        Source: Wikipedia (https://en.wikipedia.org/wiki/A*_search_algorithm)"""
        current_node = self.goal
        total_path = [current_node]
        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            total_path.append(current_node)

        return total_path

    def get_final_output(self):
        return self.get_path(), self.g_score, self.closed_set, self.g_score[self.goal]

    def dist(self, node_a, node_b):
        return np.sqrt((node_a[0] - node_b[0]) ** 2 + (node_a[1] - node_b[1]) ** 2) * self.graph[node_b[1], node_b[0]]

    @staticmethod
    def get_name():
        return "A*"


class AStar2:
    """
    Alternative (worse) A-star algorithm solver for maze graph
    """

    def __init__(self, graph, start, goal):
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
        while not self.frontier.empty():
            current = self.frontier.get()

            if current == self.goal:
                break

            for next_item in self._get_neighbours(current):
                new_cost = self.cost_so_far[current] + 1
                if next_item not in self.cost_so_far or new_cost < self.cost_so_far[next_item]:
                    self.cost_so_far[next_item] = new_cost
                    priority = new_cost + heuristic(self.goal, next_item)
                    self.frontier.put(next_item, priority)
                    self.came_from[next_item] = current

            return current

    def __iter__(self):
        return self

    def _get_neighbours(self, current):
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
        Source: Wikipedia (https://en.wikipedia.org/wiki/A*_search_algorithm)"""
        current_node = self.goal
        total_path = [current_node]
        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            total_path.append(current_node)

        return total_path

    @staticmethod
    def get_name():
        return "A* (alternative)"
