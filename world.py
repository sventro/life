from cell import Cell, Status, Neighbors, Neighborhood
from dataclasses import dataclass
from random import randint
from presets import Preset


@dataclass(slots=True)
class Grid:
    width: int
    height: int
    cells: list[list[Cell]]


def bound(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


class World:
    def __init__(
        self,
        dimensions: tuple[int, int],
        stages: bool,
        preset: Preset,
        neighborhood: Neighborhood,
    ) -> None:
        self._stages = stages
        self._neighborhood = neighborhood
        Grid.width, Grid.height = dimensions
        Grid.cells = [
            [Cell(position=[column, row]) for row in range(Grid.height)]
            for column in range(Grid.width)
        ]
        self._generate_preset(preset=preset) if preset else self._generate_random()

    def _generate_random(self) -> None:
        for row in Grid.cells:
            for cell in row:
                chance_number = randint(0, 2)
                if chance_number == 1:
                    cell.status = Status.ALIVE

    def _generate_preset(self, preset: list[tuple[int, int]]) -> None:
        for row in Grid.cells:
            for cell in row:
                if cell.position in preset:
                    cell.status = Status.ALIVE

    def update_cells(self, running: bool = True) -> None:
        dies: Cell = []
        born: Cell = []
        if running:
            for row, _ in enumerate(Grid.cells):
                for column, _ in enumerate(Grid.cells[row]):
                    cell = Grid.cells[row][column]
                    neighbors = self._check_neighbors(row, column)
                    cell.status = (
                        Status.ALIVE if cell.status == Status.BORN else cell.status
                    )
                    cell.status = (
                        Status.DEAD if cell.status == Status.DYING else cell.status
                    )
                    if cell.status == Status.ALIVE:
                        if len(neighbors.alive) not in [2, 3]:
                            dies.append(cell)
                    if cell.status == Status.DEAD:
                        if len(neighbors.alive) == 3:
                            born.append(cell)
            for cell in dies:
                cell.status = Status.DYING if self._stages else Status.DEAD
            for cell in born:
                cell.status = Status.BORN if self._stages else Status.ALIVE

    def _check_neighbors(self, x: int, y: int) -> Neighbors:
        alive = []
        dead = []
        for offset in self._neighborhood:
            position = [
                bound(value=x + offset[0], low=0, high=Grid.width - 1),
                bound(value=y + offset[1], low=0, high=Grid.height - 1),
            ]
            neighbor = Grid.cells[position[0]][position[1]]
            alive.append(
                neighbor
            ) if neighbor.status == Status.ALIVE or neighbor.status == Status.BORN else dead.append(
                neighbor
            )
        return Neighbors(alive=alive, dead=dead)
