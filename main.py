import pygame
import time
from world import World, Grid
from cell import Cell
from enum import Enum


class Shape(Enum):
    RECT: str = "rect"
    CIRCLE: str = "circle"


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    board = World(dimensions=[40, 40], stages=True, preset=False)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        Draw(screen=screen, border_size=1, shape=Shape.RECT)
        board.update_cells()
        pygame.display.flip()
        time.sleep(0.1)


class Draw:
    def __init__(self, screen: pygame.Surface, border_size: int, shape: Shape) -> None:
        self.screen = screen
        self.border_size = border_size
        self.shape = shape

        self.cell_width = self.screen.get_width() / Grid.width
        self.cell_height = self.screen.get_height() / Grid.height
        self.width = self.cell_width - border_size
        self.height = self.cell_height - border_size

        self.draw_world()

    def draw_world(self) -> None:
        for x, _ in enumerate(Grid.cells):
            for y, _ in enumerate(Grid.cells[x]):
                cell = Grid.cells[x][y]
                x_position = x * self.cell_width
                y_position = y * self.cell_height
                if self.shape == Shape.RECT:
                    self.draw_rect(cell, x_position, y_position)
                if self.shape == Shape.CIRCLE:
                    self.draw_circle(cell, x_position, y_position)

    def draw_circle(self, cell: Cell, x_pos: int, y_pos: int) -> None:
        radius = self.width / 2
        center_x = x_pos + radius + self.border_size
        center_y = y_pos + radius + self.border_size
        pygame.draw.circle(self.screen, cell.status.value, (center_x, center_y), radius)

    def draw_rect(self, cell: Cell, x_pos: int, y_pos: int) -> None:
        left = x_pos + self.border_size
        top = y_pos + self.border_size
        rect = (left, top, self.width, self.height)
        pygame.draw.rect(self.screen, cell.status.value, rect)


if __name__ == "__main__":
    main()
