from tkinter import Frame, Button, BOTH, Canvas, SE
from PIL import Image, ImageOps, ImageTk
import numpy as np
import logging


class MazeUI(Frame):
    """
    Maze UI"""

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1
        self.maze_grid = None
        self.visual_grid = None
        self.solution_grid = None
        self.photo = None
        self.__initUI()

    def __initUI(self):
        """
        Initialize UI."""

        self.parent.title("Maze traversal")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0, columnspan=3, pady=(10, 10), padx=(10, 10))

        self.start_solution = Button(self, text="Start", command=self.__start_solution)
        self.start_solution.grid(row=1, column=0, pady=(0, 10))

        self.pause_solution = Button(self, text="Pause", command=self.__pause_solution)
        self.pause_solution.grid(row=1, column=1, pady=(0, 10))

        self.next_step = Button(self, text="Next", command=self.__next_step)
        self.next_step.grid(row=1, column=2, pady=(0, 10))

    def __start_solution(self):
        pass

    def __pause_solution(self):
        pass

    def __next_step(self):
        pass

    def initialize_maze(self, grid):
        self.maze_grid = grid

        # Scale the numbers to 255 and create RGB channels
        self.visual_grid = np.vstack((self.maze_grid.astype('uint8')*255,
                                      self.maze_grid.astype('uint8')*255,
                                      self.maze_grid.astype('uint8')*255))

    def update_discoveries_visalization(self, doodoo):
        pass

    def update_maze(self, new_grid):
        self.solution_grid = new_grid

        # Create image from RGB array and scale it to size 500x500
        pil_image = Image.fromarray(self.visual_grid)
        scaled_image = ImageOps.fit(pil_image, (500, 500))

        # Draw image onto the canvas
        self.photo = ImageTk.PhotoImage(scaled_image)
        self.canvas.create_image(500, 500, image=self.photo, anchor=SE)
