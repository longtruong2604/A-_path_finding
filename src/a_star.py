from ast import Dict
import math
from queue import PriorityQueue
from src.grid import CellGrid
from src.utils import heuristic


def fill_shortest_path(board: CellGrid, max_distance=math.inf):
    start, end = board.start, board.end
    """Creates a duplicate of the board and fills the `Cell.count` field with the distance from the start to that cell."""
    # nboard = board.clone()
    # nboard.clear_count(math.inf)

    # mark the start and end for the UI
    # nboard.at(start).mark = CellMark.Start
    # nboard.at(end).mark = CellMark.End

    # # we start here, thus a distance of 0
    # open_list = [start]
    # nboard.at(start).count = 0

    # # (x,y) offsets from current cell
    # neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # while open_list:
    #     cur_pos = open_list.pop(0)
    #     cur_cell = nboard.at(cur_pos)

    #     for neighbour in neighbours:
    #         ncell_pos = maze.add_point(cur_pos, neighbour)
    #         if not nboard.is_valid_point(ncell_pos):
    #             continue

    #         cell = nboard.at(ncell_pos)

    #         if cell.type != maze.CellType.Empty:
    #             continue

    #         dist = cur_cell.count + 1
    #         if dist > max_distance:
    #             continue

    #         if cell.count > dist:
    #             cell.count = dist
    #             cell.path_from = cur_cell
    #             open_list.append(ncell_pos)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    print(type(start))
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == end:
            break

        for next in board.get_neighbors(current):
            print(type(next))
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                frontier.put(next, priority)
                came_from[next] = current
    return backtrack_to_start(came_from, end)


def backtrack_to_start(
    came_from: dict[tuple[int, int], tuple[int, int]], end: tuple[int, int]
):
    """Returns the path to the end, assuming the board has been filled in via fill_shortest_path"""
    pos = end
    path = []
    while pos is not None:
        path.append(pos)
        pos = came_from[pos]

    return path
