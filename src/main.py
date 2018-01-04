from maze import Maze
from kruskal import Kruskal
from prims import Prims
from aldous_broder import AldousBroder

from maze_ui import MazeUI
from tkinter import Tk, messagebox
import matplotlib.pyplot as plt

from a_star import AStar, AStar2

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
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #    hard_exit = True
    hard_exit = True


# Generate maze and its entrances
m = Maze()
m.generator = AldousBroder(50, 50)
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

solver = AStar(solution_window.maze_grid, m.start, m.end)
new_elem = next(solver)

while True:
    print(new_elem)

    if hard_exit:
        break

    if new_elem is not None:
        # Recolor discovery path
        solution_window.recolor_point(new_elem[0], new_elem[1], (51, 109, 204))
        solution_window.update_maze()

        new_elem = next(solver)
    else:
        # Recolor endpoint
        solution_window.recolor_point(m.end[0], m.end[1], (51, 109, 204))
        solution_window.update_maze()

        path = solver.get_path()

        # Draw solution
        solution_window.draw_final_path(path, (53, 165, 24))
        solution_window.update_maze()

    root.update()
