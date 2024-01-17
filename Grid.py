import random

DIRECTIONS = {
    "RIGHT": (0, 1),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "UP": (-1, 0)
}

class Grid:
    def __init__(self, grid_width, grid_height, path_length, disallowed_nodes):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.path_length = path_length
        self.initial_path_length = path_length
        self.start_point = self.generate_start_point()
        self.disallowed_nodes = self.generate_disallowed_nodes(disallowed_nodes)
        self.path = self.generate_path()

    def generate_start_point(self):
        """
        Generates the start point of the path.

        Returns:
            tuple: The start point of the path.
        """
        return (self.grid_width // 2, 0)

    def generate_disallowed_nodes(self, n):
        """
        Generates the disallowed nodes.

        Args:
            n (int): The number of disallowed nodes.

        Returns:
            set: The set of disallowed nodes.
        """
        disallowed_nodes = set()
        while len(disallowed_nodes) < n:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)

            # Skip if the node is the start point or is adjacent to the start point
            if (x, y) == self.start_point or \
                (x, y) == (self.start_point[0] + 1, self.start_point[1]) or \
                (x, y) == (self.start_point[0] - 1, self.start_point[1]) or \
                (x, y) == (self.start_point[0], self.start_point[1] + 1):
                continue

            disallowed_nodes.add((x, y))

        return disallowed_nodes

    def generate_path(self):
        """
        Generates the path.

        Returns:
            list: The grid with the path.
        """
        # Initialize path length
        self.path_length = self.initial_path_length

        # Initialize grid with zeros
        grid = [[0]*self.grid_width for _ in range(self.grid_height)]
        
        # Set start point
        x, y = self.start_point
        grid[y][x] = 1

        # Set disallowed nodes
        for dx, dy in self.disallowed_nodes:
            grid[dy][dx] = 2
        
        # Initialize stack with start point
        stack = [(x, y)]
        
        # Initialize max grid indices
        max_grid_x_index = self.grid_width - 1
        max_grid_y_index = self.grid_height - 1

        # Initialize disallowed nodes set
        disallowed_nodes_set = set(self.disallowed_nodes)

        # Initialize directions
        directions = list(DIRECTIONS.values())

        # Generate path
        while stack and self.path_length > 0:
            # Get top of stack
            x, y = stack[-1]

            # Shuffle directions to randomize path
            random.shuffle(directions)
            for dx, dy in directions:
                # Calculate next node
                nx, ny = x + dx, y + dy

                # If next node is out of grid boundaries or is a disallowed node, skip this direction
                if not (0 <= nx <= max_grid_x_index and 0 <= ny <= max_grid_y_index and grid[ny][nx] == 0 and (nx, ny) not in disallowed_nodes_set):
                    continue

                # Add the new node to the grid
                grid[ny][nx] = 1

                # Check if the new node has at least 3 adjacent path nodes
                for px, py in stack:
                    adjacent_path_nodes = 0
                    # Iterate over all possible directions
                    for ddx, ddy in DIRECTIONS.values():
                        # Calculate coordinates of the adjacent node
                        nnx, nny = px + ddx, py + ddy
                        # If adjacent node is a path node, increment adjacent path nodes
                        if 0 <= nnx <= max_grid_x_index and 0 <= nny <= max_grid_y_index and grid[nny][nnx] == 1:
                            adjacent_path_nodes += 1

                    # If any path node is adjacent to three other path nodes
                    if adjacent_path_nodes >= 3:
                        # Remove the new node from the grid and skip this direction
                        grid[ny][nx] = 0
                        break
                
                else:
                    # If no path node is adjacent to three other path nodes, add the new node to the stack and decrease the path length
                    stack.append((nx, ny))
                    self.path_length -= 1
                    break
                # If the direction was skipped, remove the new node from the grid
                grid[ny][nx] = 0
            else:
                # Backtrack if no valid direction was found
                bx, by = stack.pop()
                grid[by][bx] = 0

        # Set end point to the last node in the stack if it exists
        self.end_point = stack[-1] if stack else None

        return grid
