import pygame
import time
from enum import StrEnum, auto
from presets import Preset
from world import World, Grid, Neighborhood
from cell import Cell, Status

WIDTH, HEIGHT = [800, 600]
CELL_SCALING_FACTOR = 0.1
CELL_BORDER_SIZE = 1
FRAMERATE = 30


class Shape(StrEnum):
    RECT: str = auto()
    CIRCLE: str = auto()


def main() -> None:
    dimensions = [int(WIDTH * CELL_SCALING_FACTOR), int(HEIGHT * CELL_SCALING_FACTOR)]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    world = World(
        dimensions=dimensions,
        stages=True,
        preset=Preset.R_PENTOMINO.value,
        neighborhood=Neighborhood.MOORE.value,
    )
    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = not running
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:
                toggle_cells(add=True)
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    or pygame.mouse.get_pressed()[0]
                ):
                    toggle_cells(add=False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(generate_preset())

        screen.fill("grey8")
        Draw(screen=screen, border_size=CELL_BORDER_SIZE, shape=Shape.RECT)
        world.update_cells(running=running)
        pygame.display.flip()
        time.sleep(1 / FRAMERATE)


def toggle_cells(add: bool):
    x, y = pygame.mouse.get_pos()
    row = int(x * CELL_SCALING_FACTOR)
    column = int(y * CELL_SCALING_FACTOR)
    cell = Grid.cells[row][column]
    cell.status = Status.ALIVE if add else Status.DEAD


def generate_preset():
    preset = []
    for row in Grid.cells:
        for cell in row:
            if cell.status is Status.ALIVE:
                preset.append(cell.position)
    return preset


class Draw:
    def __init__(self, screen: pygame.Surface, border_size: int, shape: Shape) -> None:
        self.screen = screen
        self.border_size = border_size
        self.shape = shape

        self.cell_width = self.screen.get_width() / Grid.width
        self.cell_height = self.screen.get_height() / Grid.height
        self.width = self.cell_width - border_size
        self.height = self.cell_height - border_size

        self.__world()

    def __world(self) -> None:
        for x, _ in enumerate(Grid.cells):
            for y, _ in enumerate(Grid.cells[x]):
                cell = Grid.cells[x][y]
                position = [x * self.cell_width, y * self.cell_height]
                if self.shape == Shape.RECT:
                    self.__rect(cell, position)
                if self.shape == Shape.CIRCLE:
                    self.__circle(cell, position)

    def __circle(self, cell: Cell, position: tuple[int, int]) -> None:
        radius = self.width / 2
        center_x = position[0] + radius + self.border_size
        center_y = position[1] + radius + self.border_size
        pygame.draw.circle(self.screen, cell.status.value, (center_x, center_y), radius)

    def __rect(self, cell: Cell, position: tuple[int, int]) -> None:
        left = position[0] + self.border_size
        top = position[1] + self.border_size
        rect = (left, top, self.width, self.height)
        pygame.draw.rect(self.screen, cell.status.value, rect)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")
    main()
