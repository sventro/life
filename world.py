from cell import Cell, Status
from dataclasses import dataclass
from random import randint
from presets import Preset


@dataclass
class Grid:
    width: int
    height: int
    cells: list[list[Cell]]


@dataclass
class Neighbors:
    alive: Cell
    dead: Cell


def bound(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


class World:
    def __init__(
        self, dimensions: tuple[int, int], stages: bool, preset: Preset
    ) -> None:
        self.stages = stages
        Grid.width, Grid.height = dimensions
        Grid.cells = [
            [Cell(position=[row, column]) for column in range(Grid.height)]
            for row in range(Grid.width)
        ]
        if preset:
            self.generate_preset(preset=preset)
        else:
            self.generate_random()

    def generate_random(self) -> None:
        for row in Grid.cells:
            for cell in row:
                chance_number = randint(0, 3)
                if chance_number == 1:
                    cell.status = Status.ALIVE

    def generate_preset(self, preset: list[tuple[int, int]]) -> None:
        for row in Grid.cells:
            for cell in row:
                if cell.position in preset:
                    cell.status = Status.ALIVE

    def update_cells(self) -> None:
        dies: Cell = []
        born: Cell = []
        for row, _ in enumerate(Grid.cells):
            for column, _ in enumerate(Grid.cells[row]):
                cell = Grid.cells[row][column]
                neighbors = self.check_neighbors(row, column)
                if cell.status == Status.BORN:
                    cell.status = Status.ALIVE
                if cell.status == Status.DYING:
                    cell.status = Status.DEAD
                if cell.status == Status.ALIVE:
                    if len(neighbors.alive) not in [2, 3]:
                        dies.append(cell)
                if cell.status == Status.DEAD:
                    if len(neighbors.alive) == 3:
                        born.append(cell)
        for cell in dies:
            cell.status = Status.DYING if self.stages else Status.DEAD
        for cell in born:
            cell.status = Status.BORN if self.stages else Status.ALIVE

    def check_neighbors(self, x: int, y: int) -> Neighbors:
        offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        alive = []
        dead = []
        for offset in offsets:
            position = [
                bound(value=x + offset[0], low=0, high=Grid.width - 1),
                bound(value=y + offset[1], low=0, high=Grid.height - 1),
            ]
            neighbor = Grid.cells[position[0]][position[1]]
            if neighbor.status == Status.ALIVE or neighbor.status == Status.BORN:
                alive.append(neighbor)
            elif neighbor.status == Status.DEAD or neighbor.status == Status.DYING:
                dead.append(neighbor)
            else:
                dead.append(neighbor)
        return Neighbors(alive=alive, dead=dead)
