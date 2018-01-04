from tkinter import Tk, messagebox

from maze import Maze
from kruskal import Kruskal
from prims import Prims
from aldous_broder import AldousBroder
from maze_ui import MazeUI
from a_star import AStar, AStar2


hard_exit = False


def on_close():
    """
    Handling window close as a prompt."""
    global hard_exit

    # Comment out exit confirmation for ease of testing.
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #    hard_exit = True
    hard_exit = True


def generation_and_solution(root, solution_window):
    # Generate maze and its entrances
    m = Maze()
    m.generator = AldousBroder(solution_window.maze_width, solution_window.maze_width)
    m.generate()
    m.generate_entrances()

    # MazeUI initalization
    solution_window.initialize_maze(m)

    # Make entrance and exit into accessible areas
    solution_window.maze_grid[m.start[0], m.start[1]] = 0
    solution_window.maze_grid[m.end[0], m.end[1]] = 0

    solver = AStar(solution_window.maze_grid, m.start, m.end)
    new_elem = next(solver)

    while True:
        if solution_window.maze_generated:
            # Clear canvas from old maze
            solution_window.canvas.delete("all")
            return

        if hard_exit:
            break

        root.update()

        # If start hasn't been pressed don't start solving
        if not solution_window.start:
            continue

        # If pause is pressed, skip calculation. If next is pressed calculate until next iteration
        if solution_window.pause:
            if solution_window.next:
                solution_window.next = False
            else:
                continue

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


# Tkinter initalization
root = Tk()
root.geometry("%dx%d" % (520, 600))
root.protocol("WM_DELETE_WINDOW", on_close)
solution_window = MazeUI(root)

while True:
    root.update()

    if hard_exit:
        break

    if solution_window.maze_generated:
        # Reset maze generation flag
        solution_window.maze_generated = False

        # Generate and enable maze solution
        generation_and_solution(root, solution_window)
