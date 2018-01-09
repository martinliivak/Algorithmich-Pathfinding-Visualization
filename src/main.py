from tkinter import Tk, messagebox

from maze import Maze
from kruskal import Kruskal
from prims import Prims
from aldous_broder import AldousBroder
from maze_ui import MazeUI
from a_star import AStar, AStar2
from bfs import BFS
from dfs import DFS
from dijkstra import Dijkstra
from jps import JPS

hard_exit = False


def on_close():
    """
    Handling window close as a prompt."""
    global hard_exit

    # Comment out exit confirmation for ease of testing.
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #    hard_exit = True
    hard_exit = True


def resize_root_if_needed(root, number_of_solvers):
    root.geometry("%dx%d" % (number_of_solvers * 520, 620))


def generate_maze(solution_window):
    # Generate maze and its entrances
    m = Maze()
    m.generator = AldousBroder(solution_window.maze_width, solution_window.maze_height)
    m.generate()
    m.generate_entrances()

    # MazeUI initalization
    solution_window.initialize_maze(m)

    # Make entrance and exit into accessible areas
    solution_window.maze_grid[m.start[0], m.start[1]] = 0
    solution_window.maze_grid[m.end[0], m.end[1]] = 0

    return m


def start_solver(root, solution_window, solver):
    new_elem = next(solver)

    while True:
        if solution_window.generate_new:
            # Clear canvas from old maze (?? is it even necessary??) and stop new execution.
            # solution_window.clear_canvas_for_solver(solver.get_name())
            solution_window.start = False
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
            solution_window.recolor_point(solver.get_name(),
                                          new_elem[0],
                                          new_elem[1],
                                          (51, 109, 204))
            solution_window.update_maze()

            new_elem = next(solver)
        else:
            # Recolor endpoint
            solution_window.recolor_point(solver.get_name(),
                                          solution_window.maze.end[0],
                                          solution_window.maze.end[1],
                                          (51, 109, 204))
            solution_window.update_maze()

            path = solver.get_path()

            # Draw solution
            solution_window.draw_final_path(solver.get_name(),
                                            path,
                                            (53, 165, 24))
            solution_window.update_maze()


def start_solving(root, solution_window, active_solvers):
    nr_solvers = len(active_solvers)

    new_elems = [None] * nr_solvers
    for i, solver in enumerate(active_solvers):
        new_elems[i] = next(solver)

    while True:
        if solution_window.generate_new:
            # Clear canvas from old maze (?? is it even necessary??) and stop new execution.
            # solution_window.clear_canvas_for_solver(solver.get_name())
            solution_window.start = False
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

        for i, new_elem in enumerate(new_elems):
            solver = active_solvers[i]
            if new_elem is not None:
                solution_window.recolor_point(solver.get_name(),
                                              new_elem[0],
                                              new_elem[1],
                                              (51, 109, 204))
                solution_window.update_maze()

                new_elems[i] = next(solver)
            else:
                solution_window.recolor_point(solver.get_name(),
                                              solution_window.maze.end[0],
                                              solution_window.maze.end[1],
                                              (51, 109, 204))
                solution_window.update_maze()

                path = solver.get_path()

                # Draw solution
                solution_window.draw_final_path(solver.get_name(),
                                                path,
                                                (53, 165, 24))
                solution_window.update_maze()


def generation_and_solution(root, solution_window):
    """
    Maze's internal loop for solving and stepping."""

    global hard_exit

    # Generate maze and its entrances
    m = Maze()
    m.generator = AldousBroder(solution_window.maze_width, solution_window.maze_height)
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
        if solution_window.generate_new:
            # Clear canvas from old maze and stop new execution.
            # solution_window.canvas.delete("all")
            solution_window.start = False
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
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)

# List of solvers
solvers = [AStar, BFS, AStar2, Dijkstra, DFS, JPS]

# Might be avoided in the future, but atm needed for stupid reasons
solver_name_dict = {}
for solver in solvers:
    solver_name_dict[solver.get_name()] = solver

solution_window = MazeUI(root, solvers)

# External loop
while True:
    root.update()

    if hard_exit:
        break

    if not solution_window.start_solutions:
        continue

    if solution_window.generate_new:
        # Reset maze generation flag
        solution_window.generate_new = False

        # Generate and enable maze solution
        # generation_and_solution(root, solution_window)
        resize_root_if_needed(root, len(solution_window.selected_solver_names))
        maze = generate_maze(solution_window)

        active_solvers = []

        for solver_name, solver in solver_name_dict.items():
            if solver_name in solution_window.selected_solver_names:
                init_solver = solver(solution_window.maze_grid, maze.start, maze.end)
                active_solvers.append(init_solver)

        start_solving(root, solution_window, active_solvers)
