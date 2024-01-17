import random
import pygame

class PathGenerator:
    def __init__(self, window_width, window_height, grid_size, path_length, disallowed_nodes):
        self.width = window_width
        self.height = window_height
        self.grid_size = grid_size
        self.cell_size = window_width // grid_size
        self.initial_path_length = path_length
        self.path_length = path_length
        self.grid = None
        self.animate = False
        self.animation_path = []
        self.animation_index = 0
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.window = pygame.display.set_mode((window_width, window_height))
        self.button = pygame.Rect(window_width - 100, window_height - 50, 80, 30)
        self.animation_button = pygame.Rect(window_width - 200, window_height - 50, 80, 30)
        self.font = pygame.font.Font(None, 24)
        self.start_point = self.generate_start_point()
        self.disallowed_nodes = self.generate_disallowed_nodes(disallowed_nodes)

    def generate_start_point(self):
        return (self.grid_size // 2, 0)

    def generate_disallowed_nodes(self, n):
        disallowed_nodes = set()
        while len(disallowed_nodes) < n:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) == self.start_point:
                continue
            disallowed_nodes.add((x, y))
        return disallowed_nodes

    def generate_path(self):
        self.path_length = self.initial_path_length

        grid = [[0]*self.grid_size for _ in range(self.grid_size)]
        
        x, y = 0, 0
        grid[y][x] = 1

        for dx, dy in self.disallowed_nodes:
            grid[dy][dx] = 2
        
        stack = [(x, y)]
        self.animation_path.append((x, y))
        
        max_grid_index = self.grid_size - 1

        disallowed_nodes_set = set(self.disallowed_nodes)

        while stack and self.path_length > 0:
            x, y = stack[-1]
            
            random.shuffle(self.directions)
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx <= max_grid_index and 0 <= ny <= max_grid_index and grid[ny][nx] == 0 and \
                (nx, ny) not in disallowed_nodes_set:
                    if (0 <= nx+dy <= max_grid_index and 0 <= ny-dx <= max_grid_index and grid[ny-dx][nx+dy] == 1) or \
                    (0 <= nx-dy <= max_grid_index and 0 <= ny+dx <= max_grid_index and grid[ny+dx][nx-dy] == 1):
                        continue
                    grid[ny][nx] = 1
                    stack.append((nx, ny))
                    self.animation_path.append((nx, ny))
                    self.path_length -= 1
                    break
            else:
                bx, by = stack.pop()
                grid[by][bx] = 0
                if self.animation_path:
                    self.animation_path.pop()
                    
        return grid

    def draw_grid(self):
        node_size = self.cell_size - 2
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.animate and self.animation_path and (x, y) == self.animation_path[self.animation_index]:
                    color = (255, 0, 0) 
                elif (x, y) in self.disallowed_nodes:
                    color = (255, 255, 0)
                elif self.animation_path and (x, y) == self.animation_path[0]:  # Start point
                    color = (0, 255, 0)
                elif self.animation_path and (x, y) == self.animation_path[-1]:  # End point
                    color = (0, 0, 255)
                else:
                    color = (255, 255, 255)
                rect = pygame.Rect(x * self.cell_size + 1, y * self.cell_size + 1, node_size, node_size)
                pygame.draw.rect(self.window, color if self.grid[y][x] else (0, 0, 0), rect)

    def draw_button(self):
        pygame.draw.rect(self.window, (0, 255, 0), self.button)
        pygame.draw.rect(self.window, (0, 0, 255), self.animation_button)

        label1 = self.font.render('New Path', True, (255, 0, 0))
        self.window.blit(label1, (self.button.x + 10, self.button.y + 5))  

        label2 = self.font.render('Walk', True, (255, 0, 0))
        self.window.blit(label2, (self.animation_button.x + 10, self.animation_button.y + 5))

    def handle_button_click(self, pos):
        if self.button.collidepoint(pos):
            self.animate = False
            self.animation_index = 0
            self.animation_path = []
            self.grid = self.generate_path()
            
        elif self.animation_button.collidepoint(pos):
            self.animate = True
            self.animation_index = 0

    def run(self):
        self.grid = self.generate_path()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_button_click(event.pos)
            self.window.fill((0, 0, 0))
            self.draw_grid()
            self.draw_button()
            pygame.display.update()
            if self.animate:
                pygame.time.delay(100)
                self.animation_index += 1
            if self.animation_index >= len(self.animation_path):
                self.animate = False

pygame.init()

path_generator = PathGenerator(800, 800, 10, 20, 15)
path_generator.run()
