import queue as Q

class Dijkstra:
    """
    Dijkstra algorithm solver for maze graph.
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    
    def __init__(self, graph, start, goal):
        """
        Initializing all of the parameters necessary to solve the maze using Dijkstra """
        self.graph = graph
        self.start = start
        self.goal = goal
        self.h, self.w = self.graph.shape
        self.h -= 1
        self.w -= 1
        
        #More
        self.came_from = dict()
        
        #self.current = start
        #http://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php
        self.queue = Q.PriorityQueue()
        self.queue.put((0, start))
        
        self.visited = []
        self.unvisited = [] 
        
    def __iter__(self):
        return self
    
    def __next__(self):
        """
        This makes the solver work in a Python generator style fashion, allowing the visualizer to call next until
        None is returned, which signifies that the maze has been solved
        """
        while not self.queue.empty():
            a, current = self.queue.get()
            if current in self.visited:
                continue
            else:
                self.visited.append(current)
                
            if current == self.goal:
                break
            
            min_len = self._length_of_path(current) + 1
            for next_item in self._get_neighbours(current):
                if next_item in self.visited:
                    continue
                if not next_item in self.came_from:
                    self.came_from[next_item] = current
                    self.queue.put((min_len, next_item))
                else:
                    if self._length_of_path(next_item) > min_len:
                        self.came_from[next_item] = self.current
                    
                        if not next_item in self.visited:
                            self.queue.put((min_len, next_item))
            
            return current
            
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
    
    def _length_of_path(self, c_start):
        
        if (c_start == self.start):
            return 0
        cntr = 1
        c = self.came_from[c_start]
        while(c != self.start):
            cntr += 1
            c = self.came_from[c]
            
        return cntr
    
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
        return "Dijkstra"
    