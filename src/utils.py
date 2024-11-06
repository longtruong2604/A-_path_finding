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
