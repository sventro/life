from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    DEAD: tuple = (0, 0, 0)
    DYING: tuple = (101, 64, 64)
    BORN: tuple = (217, 234, 211)
    ALIVE: tuple = (255, 255, 255)


@dataclass(slots=True)
class Cell:
    status: Status = Status.DEAD
    position: tuple[int, int] = (0, 0)


@dataclass(slots=True)
class Neighbors:
    alive: Cell
    dead: Cell


class Neighborhood(Enum):
    ELEMENTARY = [[-1, 1], [0, 1], [1, 1]]
    MOORE = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    VON_NEUMANN = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    VON_NEUMANN2 = [(0, -1), (0, -2), (-1, 0), (-2, 0), (1, 0), (2, 0), (0, 1), (0, 2)]
