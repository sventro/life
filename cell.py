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
