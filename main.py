import pygame
import time
from world import World, Grid


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    running = True
    board = World(dimensions=[40, 40], preset=True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        draw_world(screen, Grid)
        board.update_cells()
        pygame.display.flip()
        time.sleep(0.1)


def draw_world(
    screen: pygame.Surface, grid: Grid, rect: bool = True, circle: bool = False
) -> None:
    border_size = 1
    cell_width = screen.get_width() / grid.width
    cell_height = screen.get_height() / grid.height
    width = cell_width - border_size
    height = cell_height - border_size

    for x in range(len(grid.cells)):
        for y in range(len(grid.cells[x])):
            cell = grid.cells[x][y]
            if rect:
                left = x * cell_width + border_size
                top = y * cell_height + border_size
                pygame.draw.rect(screen, cell.status.value, (left, top, width, height))
            if circle:
                center = [
                    x * cell_width + width / 2 + border_size,
                    y * cell_height + height / 2 + border_size,
                ]
                radius = width / 2
                pygame.draw.circle(screen, cell.status.value, center, radius)


if __name__ == "__main__":
    main()
