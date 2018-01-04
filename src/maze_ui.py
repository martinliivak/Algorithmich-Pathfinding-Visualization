from tkinter import Frame, Label, Entry, Button, BOTH, Canvas, SE, messagebox
from PIL import Image, ImageOps, ImageTk
import numpy as np


class MazeUI(Frame):
    """
    Maze UI"""

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1

        self.maze_width = None
        self.maze_height = None
        self.maze_generated = False

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

        Label(self, text='Width').grid(row=0, column=0)
        Label(self, text='Height').grid(row=0, column=1)

        self.maze_width_entry = Entry(self)
        self.maze_width_entry.grid(row=1, column=0)
        self.maze_width_entry.insert('end', '50')

        self.maze_height_entry = Entry(self)
        self.maze_height_entry.grid(row=1, column=1)
        self.maze_height_entry.insert('end', '50')

        self.create_maze = Button(self, text="Generate maze", command=self.__generate_maze)
        self.create_maze.grid(row=1, column=2)

        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.grid(row=2, column=0, columnspan=3, pady=(5, 5), padx=(4, 4))

        self.start_solution = Button(self, text="Start", command=self.__start_solution)
        self.start_solution.grid(row=3, column=0, pady=(0, 10))

        self.pause_solution = Button(self, text="Pause", command=self.__pause_solution)
        self.pause_solution.grid(row=3, column=1, pady=(0, 10))

        self.next_step = Button(self, text="Next", command=self.__next_step)
        self.next_step.grid(row=3, column=2, pady=(0, 10))

    def __generate_maze(self):
        try:
            height = int(self.maze_height_entry.get())
            width = int(self.maze_width_entry.get())
        except (ValueError, TypeError):
            height, width = '-1', '-1'

        if isinstance(height, int) and isinstance(width, int):
            if 5 <= height <= 100 and 5 <= width <= 100:
                self.maze_width = width
                self.maze_height = height
                self.maze_generated = True
            else:
                messagebox.showwarning("Size error", "Height and width need to be between 5 and 100.")
        else:
            messagebox.showwarning("Input error", "Height and width need to be integers.")


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

    def initialize_maze(self, maze):
        self.maze_grid = maze.grid
        invert_bw_grid = 1 - maze.grid

        # Scale the numbers to 255 and create RGB channels
        self.visual_grid = np.stack((invert_bw_grid.astype('uint8')*255,
                                     invert_bw_grid.astype('uint8')*255,
                                     invert_bw_grid.astype('uint8')*255),
                                    axis=2)

        self.paint_entrances(maze.start, maze.end)
        self.update_maze()

    def paint_entrances(self, start, end):
        # Start to red
        self.recolor_point(start[0], start[1], (255, 53, 22))

        # End to green
        self.recolor_point(end[0], end[1], (2, 255, 32))

    def recolor_point(self, r, c, rgb_values):
        self.visual_grid[r][c][0] = rgb_values[0]
        self.visual_grid[r][c][1] = rgb_values[1]
        self.visual_grid[r][c][2] = rgb_values[2]

    def draw_final_path(self, path, rgb_values):
        for point in path:
            self.recolor_point(point[0], point[1], rgb_values)

    def update_maze(self):
        # Create image from RGB array and scale it to size 480x480
        # If image is not squared, it will be upscaled and aspect ratio is retained
        pil_image = Image.fromarray(self.visual_grid)
        #scaled_image = ImageOps.fit(pil_image, (480, 480))

        old_size = pil_image.size
        ratio = float(480) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        pil_image = pil_image.resize(new_size)
        scaled_image = Image.new("RGB", (480, 480))
        scaled_image.paste(pil_image,
                           ((480 - new_size[0]) // 2, (480 - new_size[1]) // 2))

        # Draw image onto the canvas
        self.photo = ImageTk.PhotoImage(scaled_image)
        self.canvas.create_image(500, 500, image=self.photo, anchor=SE)
