from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    DEAD: tuple = (0, 0, 0)
    DYING: tuple = (234, 153, 153)
    BORN: tuple = (182, 215, 168)
    ALIVE: tuple = (255, 255, 255)


@dataclass
class Cell:
    status: Status = Status.DEAD
    position: tuple[int, int] = (0, 0)
