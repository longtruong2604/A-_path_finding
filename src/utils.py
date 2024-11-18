def add_point(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> tuple[int, int]:
    """Adds two points represented as [x, y] coordinates."""
    return (pos_a[0] + pos_b[0], pos_a[1] + pos_b[1])


def print_queue(q):
    """Utility to print contents of a PriorityQueue without modifying it."""
    temp_queue = []
    while not q.empty():
        item = q.get()
        temp_queue.append(item)
        priority, cell = item
        print(f"Priority: {priority}, Position: {cell.pos}, Count: {cell.count}")

    for item in temp_queue:
        q.put(item)


def read_input(file_path: str):
    """
    Đọc file input.

    Parameters:
        file_path (str): Đường dẫn đến file input
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Đọc kích thước bản đồ
    size = int(lines[0].strip())

    # Đọc vị trí các vật cản
    walls = [
        tuple(map(int, pos.strip("()").split(",")))
        for pos in lines[1].strip().split("),(")
    ]

    # Đọc vị trí ô bắt đầu và ô kết thúc
    start = tuple(map(int, lines[2].strip("((\n)").split(",")))
    end = tuple(map(int, lines[3].strip("((\n)").split(",")))
    return size, walls, start, end
