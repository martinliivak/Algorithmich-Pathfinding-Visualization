from collections import deque


class BFS:
    """
    Breadth-first search solver for maze graph
    """

    def __init__(self, graph, start, goal):
        """
        Initializing all of the parameters necessary to solve the maze using BFS """
        self.graph = graph
        self.start = start
        self.goal = goal
        self.h, self.w = self.graph.shape
        self.h -= 1
        self.w -= 1

        self.queue = deque([(start, 0)])
        self.came_from = dict()
        self.came_from[start] = None

    def __iter__(self):
        return self

    def __next__(self):
        """
        This makes the solver work in a Python generator style fashion, allowing the visualizer to call next until
        None is returned, which signifies that the maze has been solved
        """
        while self.queue:
            vertex, val = self.queue.popleft()

            if vertex == self.goal:
                break

            for next_item in self._get_neighbours(vertex):
                if next_item not in self.came_from:
                    self.came_from[next_item] = vertex
                    self.queue.append((next_item, val + 1))

            return vertex

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
        Returns the path from goal to start as a list """
        current_node = self.goal
        total_path = [current_node]

        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            if current_node is not None:
                total_path.append(current_node)

        return total_path

    @staticmethod
    def get_name():
        return "Breadth-first search"
