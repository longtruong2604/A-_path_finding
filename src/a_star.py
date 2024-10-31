import math
from queue import PriorityQueue
from src.grid import Cell, CellGrid
from src.utils import heuristic


def fill_shortest_path(board: CellGrid, n=math.inf):
    board.clear_count(math.inf)
    start, end = board.get_start(), board.get_end()
    start.count = 0
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
    frontier.put((0, start))
    visited = set()
    visited.add(start.pos)
    print("start", start.pos, start.count)
    print("end", end.pos, end.count)
    while n > 0 and not frontier.empty():
        [print(p[0], p[1].pos, p[1].count) for p in frontier.queue]
        p, current = frontier.get()
        # if current.pos == end.pos:
        #     break
        print("current", current.pos, current.count, p)
        flag = False
        for next in board.get_neighbors(current.pos):
            new_cost = current.count + 1
            if next.pos not in visited or new_cost < next.count:
                next.count = new_cost
                next.path_from = current
                if next.pos == end.pos:
                    flag = True
                visited.add(next.pos)
                priority = new_cost + heuristic(end.pos, next.pos)
                frontier.put((priority, next))
        if flag:
            return
        n -= 1


def backtrack_to_start(end: Cell):
    """Returns the path from the start to the end, assuming the board has been filled in via fill_shortest_path"""
    current = end
    path = []

    while current is not None:
        path.append(current.pos)
        current = current.path_from

    # Reverse the path to go from start to end
    path.reverse()
    return path
