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

        self.start = False
        self.pause = False
        self.next = False

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
        """
        Stop pausing and start solving."""
        self.start = True
        self.pause = False

    def __pause_solution(self):
        """
        Start pausing and stop solving."""
        self.pause = True
        self.start = True

    def __next_step(self):
        """
        Pressing next has no meaning if solving isn't paused."""
        self.next = True

    def initialize_maze(self, grid):
        self.maze_grid = grid
        invert_bw_grid = 1 - grid

        # Scale the numbers to 255 and create RGB channels
        self.visual_grid = np.stack((invert_bw_grid.astype('uint8')*255,
                                     invert_bw_grid.astype('uint8')*255,
                                     invert_bw_grid.astype('uint8')*255),
                                    axis=2)
        self.update_maze()

    def paint_entrances(self, start, end):
        # Start to red
        self.recolor_point(start[0], start[1], (232, 9, 9))

        # End to green
        self.recolor_point(end[0], end[1], (20, 155, 40))

    def recolor_point(self, r, c, rgb_values):
        self.visual_grid[r][c][0] = rgb_values[0]
        self.visual_grid[r][c][1] = rgb_values[1]
        self.visual_grid[r][c][2] = rgb_values[2]

    def draw_final_path(self, path, rgb_values):
        for point in path:
            self.recolor_point(point[0], point[1], rgb_values)

    def update_maze(self):
        # Create image from RGB array and scale it to size 500x500
        pil_image = Image.fromarray(self.visual_grid)
        scaled_image = ImageOps.fit(pil_image, (480, 480))

        # Draw image onto the canvas
        self.photo = ImageTk.PhotoImage(scaled_image)
        self.canvas.create_image(500, 500, image=self.photo, anchor=SE)
