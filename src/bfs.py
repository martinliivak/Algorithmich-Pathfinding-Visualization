from collections import deque


class BFS:
    def __init__(self, graph, start, goal):
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
            if current_node is not None:
                total_path.append(current_node)

        return total_path

    @staticmethod
    def get_name():
        return "Breadth-first search"
