from collections import deque

class Position:
    def __init__(self, x, y, traversable=True):
        self.x = x
        self.y = y
        self.traversable = traversable

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Map:
    def __init__(self, grid):
        """
        grid: 2D list of booleans (True = traversable, False = blocked)
        """
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

        # Create a grid of Position objects
        self.grid = [
            [Position(row, col, traversable=grid[row][col]) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def get_position(self, x, y):
        """Return the Position object at (x, y) if within bounds."""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[x][y]
        return None


class Rover:
    def __init__(self, start_pos):
        self.battery = 100
        self.current_position = start_pos

    def traverse(self, destination, terrain_map):
        """
        Perform BFS to reach the destination.
        Returns number of steps if reachable and battery is sufficient; otherwise -1.
        """
        visited = [[False] * terrain_map.cols for _ in range(terrain_map.rows)]
        queue = deque([(self.current_position, 0)])  # (current position, steps taken)

        # Movement directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current, steps = queue.popleft()
            x, y = current.x, current.y

            if visited[x][y]:
                continue
            visited[x][y] = True

            if current == destination:
                if steps <= self.battery:
                    self.battery -= steps
                    self.current_position = destination
                    return steps
                return -1  # Not enough battery

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                next_pos = terrain_map.get_position(nx, ny)
                if next_pos and next_pos.traversable and not visited[nx][ny]:
                    queue.append((next_pos, steps + 1))

        return -1  # Destination not reachable
