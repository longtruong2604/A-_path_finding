# Tùy chỉnh các thông số cố định UI

GAME_TITLE = "A* Pathfinding"  # Tên cửa sổ
SCREEN_WIDTH = 1100  # Chiều rộng cửa sổ
SCREEN_HEIGHT = 1000  # Chiều cao cửa sổ
MARGIN = 5  # Lề

BOARD_SIZE = 800  # Kích thước bảng === chiều rộng cửa sổ
GRID_SIZE = 15  # Số ô trên mỗi hàng và cột
CELL_COLOR_EMPTY = (60, 60, 60)  # Màu ô trống
CELL_COLOR_WALL = (139, 69, 19)  # Màu của ô vật cản
CELL_GAP = 1  # Khoảng cách giữa các ô
CELL_CURRENT_COLOR = (0, 255, 255)
CELL_NEXT_COLOR = (255, 0, 0)
CELL_SIZE = (
    BOARD_SIZE - 2 * MARGIN - ((GRID_SIZE - 1) * CELL_GAP)
) / GRID_SIZE  # Kích thước hình vuông của mỗi ô
PATH_LINE_WIDTH = 3  # Độ dày của đường đi

FONT_SIZE = round(CELL_SIZE) // 2  # Cỡ chữ
FONT_COLOR = (255, 255, 255)  # Màu chữ

SLIDER_WIDTH = 800 // 2  # Chiều rộng thanh trượt
SLIDER_HEIGHT = 20  # Chiều cao thanh trượt
SLIDER_BAR_COLOR = (100, 100, 100)  # Màu của thanh trượt
SLIDER_THUMB_SIZE = SLIDER_HEIGHT * 1.5  # Kích thước nút trượt
SLIDER_THUMB_COLOR = (255, 255, 255)  # Màu của nút trượt

ARROW_COLOR = (255, 255, 255)  # Màu mũi tên
ARROW_SIZE = 2  # Độ dày mũi tên
