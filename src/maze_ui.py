from tkinter import Frame, Label, Entry, Button, BOTH, Canvas, SE, CENTER, messagebox
from tkinter.ttk import Treeview
from PIL import Image, ImageOps, ImageTk
import numpy as np


class MazeUI(Frame):
    """
    Maze UI"""

    def __init__(self, parent, solvers):
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1

        self.solvers = solvers
        self.selected_solver_names = []

        self.maze_width = None
        self.maze_height = None
        self.start_solutions = False
        self.generate_new = False

        self.start = False
        self.pause = False
        self.next = False

        self.maze = None
        self.maze_grid = None
        self.visual_grids = {}
        self.canvases = {}
        self.photos = {}
        self.photo1 = None
        self.photo2 = None

        self.__initUI()

    def __initUI(self):
        """
        Initialize UI."""

        self.parent.title("Maze traversal")
        self.pack(fill=BOTH, expand=1)

        Label(self, text='Height').grid(row=0, column=0)
        Label(self, text='Width').grid(row=0, column=1)

        self.maze_width_entry = Entry(self)
        self.maze_width_entry.grid(row=1, column=0)
        self.maze_width_entry.insert('end', '50')

        self.maze_height_entry = Entry(self)
        self.maze_height_entry.grid(row=1, column=1)
        self.maze_height_entry.insert('end', '50')

        self.create_maze = Button(self, text="Generate maze", command=self.__generate_maze)
        self.create_maze.grid(row=1, column=2)

        self.initial_canvas = Canvas(self, width=500, height=500)
        self.initial_canvas.grid(row=2, column=0, columnspan=3, padx=(4, 4), pady=(5, 5))

        self.solver_list = Treeview(self, columns='algorithms')
        self.solver_list['show'] = 'headings'
        self.solver_list.heading('algorithms', text='Algorithms')
        self.solver_list.column('algorithms', width=250, anchor=CENTER)
        self.solver_list.grid(row=2, column=0, columnspan=3, padx=(4, 4), pady=(5, 5))

        for solver in self.solvers:
            name = '"' + solver.get_name() + '"'
            self.solver_list.insert('', 'end', values=name)

        self.start_solution = Button(self, text="Start", command=self.__start_solution)
        self.start_solution.grid(row=3, column=0, pady=(0, 10))

        self.pause_solution = Button(self, text="Pause", command=self.__pause_solution)
        self.pause_solution.grid(row=3, column=1, pady=(0, 10))

        self.next_step = Button(self, text="Next", command=self.__next_step)
        self.next_step.grid(row=3, column=2, pady=(0, 10))

    def __generate_maze(self):
        size_ok = False
        algos_ok = False
        # Clear previous list
        self.selected_solver_names = []

        # Size input validation
        try:
            height = int(self.maze_height_entry.get())
            width = int(self.maze_width_entry.get())
        except (ValueError, TypeError):
            height, width = '-1', '-1'

        if isinstance(height, int) and isinstance(width, int):
            if 5 <= height <= 100 and 5 <= width <= 100:
                self.maze_width = width
                self.maze_height = height
                size_ok = True
            else:
                messagebox.showwarning("Size error", "Height and width need to be between 5 and 100.")
                return
        else:
            messagebox.showwarning("Input error", "Height and width need to be integers.")
            return

        # Getting solver list selections
        solver_selection = self.solver_list.selection()
        if 0 < len(solver_selection) <= 2:
            for selection in solver_selection:
                self.selected_solver_names.append(self.solver_list.item(selection)['values'][0])
            algos_ok = True
        else:
            messagebox.showwarning("Selection error", "Please select 1-2 solver algorithms.")
            return

        # If inputs are okay, lose the listview and show the canvas
        if size_ok and algos_ok:
            self.solver_list.grid_forget()
            self.initial_canvas.grid_forget()
            self.start_solutions = True
            self.generate_new = True

    def __start_solution(self):
        """
        Stop pausing and start solving."""
        if self.start_solutions:
            self.start = True
            self.pause = False

    def __pause_solution(self):
        """
        Start pausing and stop solving."""
        if self.start_solutions:
            self.pause = True
            self.start = True

    def __next_step(self):
        """
        Pressing next has no meaning if solving isn't paused."""
        if self.start_solutions:
            self.next = True

    def initialize_maze(self, maze):
        self.maze = maze
        self.maze_grid = np.copy(maze.grid)
        self.create_visual_grids(maze)
        self.update_maze()

    def create_visual_grids(self, maze):
        for solver_name in self.selected_solver_names:
            invert_bw_grid = 1 - maze.grid

            # Scale the numbers to 255 and create RGB channels
            visual_grid = np.stack((invert_bw_grid.astype('uint8') * 255,
                                    invert_bw_grid.astype('uint8') * 255,
                                    invert_bw_grid.astype('uint8') * 255),
                                   axis=2)

            self.visual_grids[solver_name] = np.copy(visual_grid)
            self.paint_entrances(solver_name, maze.start, maze.end)

    def paint_entrances(self, solver_name, start, end):
        # Start to red
        self.recolor_point(solver_name, start[0], start[1], (255, 53, 22))

        # End to green
        self.recolor_point(solver_name, end[0], end[1], (2, 255, 32))

    def recolor_point(self, solver_name, r, c, rgb_values):
        self.visual_grids[solver_name][r][c][0] = rgb_values[0]
        self.visual_grids[solver_name][r][c][1] = rgb_values[1]
        self.visual_grids[solver_name][r][c][2] = rgb_values[2]

    def draw_final_path(self, solver_name, path, rgb_values):
        for point in path:
            self.recolor_point(solver_name, point[0], point[1], rgb_values)

    def update_maze(self):
        i = 0
        for solver_name in self.selected_solver_names:
            canvas = Canvas(self, width=500, height=500)
            canvas.grid(row=2, column=i * 4, columnspan=3, padx=(4, 4), pady=(5, 5))
            self.canvases[solver_name] = canvas
            i += 1

            # Create image from RGB array and scale it to size 480x480
            # If image is not squared, it will be upscaled and aspect ratio is retained
            pil_image = Image.fromarray(self.visual_grids[solver_name])
            # scaled_image = ImageOps.fit(pil_image, (480, 480))

            old_size = pil_image.size
            ratio = float(480) / max(old_size)
            new_size = tuple([int(x * ratio) for x in old_size])
            pil_image = pil_image.resize(new_size)
            scaled_image = Image.new("RGB", (480, 480))
            scaled_image.paste(pil_image,
                               ((480 - new_size[0]) // 2, (480 - new_size[1]) // 2))

            # Draw image onto the canvas
            self.photos[solver_name] = ImageTk.PhotoImage(scaled_image)
            canvas.create_image(500, 500, image=self.photos[solver_name], anchor=SE)

    def clear_canvas_for_solver(self, solver_name):
        self.canvases[solver_name].delete("all")
