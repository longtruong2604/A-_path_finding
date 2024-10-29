from enum import Enum


class CellType(Enum):
    Empty = 1
    Wall = 2


class CellMark(Enum):
    No = 0
    Start = 1
    End = 2
