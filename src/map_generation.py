import random
from src.config import AUTO_MODE
from src.grid import Cell
from src.types import CellType


def gen_grid(
    width: int, height: int, walls: list[tuple[int, int]] = None
) -> list[list[Cell]]:
    """Sinh bản đồ cùng với các vật cản

    Args:
        width (int): Số lượng ô chiều ngang
        height (int): Số lượng ô chiều dọc
        walls ([List[Tuple[int, int]]]): Danh sách các ô vật cản

    Returns:
        List[List[Cell]]: Mảng 2 chiều chứa các ô kiểu Cell
    """

    grid = [
        [Cell(type=CellType.Empty, pos=(x, y)) for y in range(height)]
        for x in range(width)
    ]

    if AUTO_MODE:
        # Tạo vật cản tách bản đồ ra làm 4 góc phần tư
        for x in range(width):
            grid[x][height // 2].type = CellType.Wall
        for y in range(height):
            grid[width // 2][y].type = CellType.Wall

        # Đổi các ô vật cản thành ô trống 1 cách ngẫu nhiên để tạo lỗ trống
        grid[random.randint(0, width // 2 - 1)][height // 2].type = CellType.Empty
        grid[random.randint(width // 2 + 1, width - 1)][
            height // 2
        ].type = CellType.Empty
        grid[width // 2][random.randint(0, height // 2 - 1)].type = CellType.Empty
        grid[width // 2][
            random.randint(height // 2 + 1, height - 1)
        ].type = CellType.Empty
    else:
        # Place walls based on the provided wall list
        for x, y in walls:
            if 0 <= x < width and 0 <= y < height:  # Ensure the wall is within bounds
                grid[x][y].type = CellType.Wall
    return grid


def get_random_empty_cell(grid: list[list[Cell]]) -> tuple[int, int]:
    """Random đến khi nào ô đó không phải là ô vật cản

    Args:
        grid (list[list[Cell]]): Mảng grid 2 chiều chứa các Cell

    Returns:
        tuple[int, int]: 1 ô không phải là vật cản ngẫu nhiên
    """
    cell = None

    while not cell or grid[cell[0]][cell[1]].type == CellType.Wall:
        cell = (
            random.randrange(0, len(grid) - 1),
            random.randrange(0, len(grid) - 1),
        )

    return cell
