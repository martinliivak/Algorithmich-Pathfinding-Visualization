from queue import PriorityQueue


def heuristic(a, b):
    """
    Manhattan heuristic
    """
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbours(graph, current):
    r, c = current
    h, w = graph.shape
    neighbours = []

    if r - 1 >= 0 and c - 1 >= 0:
        if graph[r - 1, c - 1] != 1:
            neighbours.append((r - 1, c - 1))

    if r - 1 >= 0 and c + 1 < w:
        if graph[r - 1, c + 1] != 1:
            neighbours.append((r - 1, c + 1))

    if r + 1 < h and c - 1 >= 0:
        if graph[r + 1, c - 1] != 1:
            neighbours.append((r + 1, c - 1))

    if r + 1 < h and c + 1 < w:
        if graph[r + 1, c + 1] != 1:
            neighbours.append((r + 1, c + 1))

    return neighbours


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from = dict()
    cost_so_far = dict()

    came_from[start] = 0
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        # for next in graph.neighbors(current):
        for next in get_neighbours(graph, current):
            # new_cost = cost_so_far[current] + graph.cost(current, next)
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

        yield current

    return came_from, cost_so_far


class AStar:
    """
    A star algorithm solver for maze graph
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

        self.came_from[start] = 0
        self.cost_so_far[start] = 0

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
