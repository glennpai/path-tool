import pygame

from Grid import Grid

class UI:
    def __init__(self, window_width, window_height, grid: Grid):
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = min(window_width // grid.grid_width, window_height // grid.grid_height)
        self.window = pygame.display.set_mode((window_width, window_height))
        self.new_path_button = pygame.Rect(self.window_width - 100, self.window_height - 170, 100, 50)
        self.new_disallowed_button = pygame.Rect(self.window_width - 100, self.window_height - 110, 100, 50)
        self.animation_button = pygame.Rect(self.window_width - 100, self.window_height - 50, 100, 50)
        self.font = pygame.font.Font(None, 24)
        self.grid = grid

    def draw_grid(self):
        """
        Draws the grid on the window.
        """
        # Draw nodes slightly smaller than cells to make the grid visible
        node_size = self.cell_size - 2

        for y in range(self.grid.grid_height):
            for x in range(self.grid.grid_width):
                if (x, y) == self.grid.start_point:
                    color = (0, 255, 0) # Green
                elif (x, y) == self.grid.end_point:
                    color = (0, 0, 255) # Blue
                elif (x, y) in self.grid.disallowed_nodes:
                    color = (255, 255, 0) # Yellow
                else:
                    color = (255, 255, 255) # White

                rect = pygame.Rect(x * self.cell_size + 1, y * self.cell_size + 1, node_size, node_size)
                pygame.draw.rect(self.window, color if self.grid.path[y][x] else (0, 0, 0), rect)

    def draw_button(self):
        """
        Draws the buttons on the window.
        """
        pygame.draw.rect(self.window, (0, 255, 0), self.new_path_button)
        pygame.draw.rect(self.window, (0, 255, 255), self.new_disallowed_button)
        pygame.draw.rect(self.window, (0, 0, 255), self.animation_button)

        label1 = self.font.render('New Path', True, (255, 0, 0))
        self.window.blit(label1, (self.new_path_button.x + 10, self.new_path_button.y + 5))  

        label2 = self.font.render('New Disallowed', True, (255, 0, 0))
        self.window.blit(label2, (self.new_disallowed_button.x + 10, self.new_disallowed_button.y + 5))  

        label3 = self.font.render('Walk', True, (255, 0, 0))
        self.window.blit(label3, (self.animation_button.x + 10, self.animation_button.y + 5))

    def handle_button_click(self, pos):
        """
        Handles the button click events.

        Args:
            pos (tuple): The position of the mouse click.
        """
        if self.new_path_button.collidepoint(pos):
            self.grid.path = self.grid.generate_path()
        
        elif self.new_disallowed_button.collidepoint(pos):
            self.grid = Grid(self.grid.grid_width, self.grid.grid_height, self.grid.initial_path_length, len(self.grid.disallowed_nodes))
            
        elif self.animation_button.collidepoint(pos):
            pass
