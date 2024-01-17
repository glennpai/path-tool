import pygame
from Grid import Grid
from UI import UI

GRID_WIDTH = 3
GRID_HEIGHT = 5
PATH_LENGTH = GRID_WIDTH * GRID_HEIGHT // 2
DISALLOWED_NODES_MODIFIER = 10
DISALLOWED_NODES = GRID_WIDTH + GRID_HEIGHT // (1 * DISALLOWED_NODES_MODIFIER)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

def main():
    pygame.init()

    grid = Grid(GRID_WIDTH, GRID_HEIGHT, PATH_LENGTH, DISALLOWED_NODES)
    ui = UI(WINDOW_WIDTH, WINDOW_HEIGHT, grid)

    running = True

    while running:
        ui.draw_grid()
        ui.draw_button()
        pygame.display.flip()  # Add this line
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui.handle_button_click(event.pos)

    pygame.quit()

if __name__ == "__main__":
    main()
