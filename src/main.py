from maze import Maze
from kruskal import Kruskal
from prims import Prims
from aldous_broder import AldousBroder

from maze_ui import MazeUI
from tkinter import Tk, messagebox
import matplotlib.pyplot as plt

from a_star import AStar

hard_exit = False


def showPNG(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation="nearest")
    plt.xticks([]), plt.yticks([])
    plt.show()


def on_close():
    """
    Handling window close as a prompt."""
    # ???
    global hard_exit
    # ???

    # Comment out exit confirmation for ease of testing.
    #if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #    hard_exit = True
    hard_exit = True


m = Maze()
m.generator = AldousBroder(30, 30)
m.generate()
m.generate_entrances()

# Tkinter initalization
root = Tk()
root.geometry("%dx%d" % (520, 600))
root.protocol("WM_DELETE_WINDOW", on_close)

# MazeUI initalization
solution_window = MazeUI(root)
solution_window.initialize_maze(m.grid)
solution_window.paint_entrances(m.start, m.end)

solution_window.maze_grid[m.start[0], m.start[1]] = 0
solution_window.maze_grid[m.end[0], m.end[1]] = 0

print(m.start)
print(m.end)
print(solution_window.maze_grid)

asd = AStar(solution_window.maze_grid, m.start, m.end)

while True:
    new_elem = next(asd)
    print(new_elem)

    if not new_elem:
        break

    solution_window.recolor_point(new_elem[0], new_elem[1], (51, 109, 204))
    solution_window.update_maze(solution_window.visual_grid)
    root.update()
