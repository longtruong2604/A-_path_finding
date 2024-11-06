import math
from queue import PriorityQueue
from src.grid import Cell, CellGrid


def a_star(grid: CellGrid, step: int) -> int:
    grid.clear_count(math.inf)
    start, end = grid.get_start(), grid.get_end()
    start.hidden = 0
    max_steps = 0

    frontier = PriorityQueue()
    frontier.put((0, start))
    visited = set()
    visited.add(start.pos)
    while not frontier.empty():
        _, current = frontier.get()
        if current.pos == end.pos:
            break
        for next in grid.get_neighbors(current.pos):
            new_cost = current.hidden + 1
            if next.pos not in visited or new_cost < next.hidden:
                visited.add(next.pos)
                priority = heuristic(end.pos, next.pos)
                if step > 0:
                    next.update_cell(new_cost, priority, current)
                next.hidden = new_cost
                frontier.put((priority, next))

        max_steps += 1
        step -= 1

    return max_steps


def backtrack_to_start(end: Cell) -> list[tuple[int, int]]:
    """Returns the path from the start to the end, assuming the grid has been filled in via fill_shortest_path"""
    current = end
    path = []

    while current is not None:
        path.append(current.pos)
        current = current.path_from

    # Reverse the path to go from start to end
    path.reverse()
    return path


def manhatan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def heuristic(goal: tuple[int, int], next: tuple[int, int]):
    return manhatan_distance(goal, next)
