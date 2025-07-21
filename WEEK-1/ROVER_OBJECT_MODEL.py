class Position:
    """
    Represents a coordinate on the map.

    Attributes:
        x (int): X-coordinate of the position.
        y (int): Y-coordinate of the position.
        traversable (bool): Whether this position is accessible.
    """

    def __init__(self, x, y, traversable=True):
        self.x = x
        self.y = y
        self.traversable = traversable

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Map:
    """
    Represents a 2D grid map made of Position objects.

    Attributes:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        grid (list[list[Position]]): 2D list of Position objects.
    """

    def __init__(self, grid):
        """
        Initializes the map using a grid of booleans.

        Args:
            grid (list[list[bool]]): True for traversable cells, False for blocked.
        """
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.grid = [
            [Position(i, j, grid[i][j]) for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def is_traversable(self, x, y):
        """
        Checks if a position (x, y) is within bounds and traversable.

        Args:
            x (int): Row index.
            y (int): Column index.

        Returns:
            bool: True if traversable, False otherwise.
        """
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y].traversable


class Rover:
    """
    Represents a rover that can traverse the map.

    Attributes:
        battery (int): Battery percentage (starts at 100%).
        current_position (Position): Current location of the rover.
    """

    def __init__(self, start_pos):
        """
        Initializes the rover with a starting position.

        Args:
            start_pos (Position): Initial position of the rover.
        """
        self.battery = 100
        self.current_position = start_pos

    def traverse(self, destination, map_obj):
        """
        Moves the rover from its current position to the destination
        by taking one non-diagonal step at a time.

        The rover consumes 1% battery for every step. It can only move
        to traversable blocks.

        Args:
            destination (Position): Target position to reach.
            map_obj (Map): The map object representing the terrain.

        Returns:
            int: Number of steps taken if successful,
                 -1 if the path is blocked or battery is insufficient.
        """
        x, y = self.current_position.x, self.current_position.y
        dest_x, dest_y = destination.x, destination.y
        steps = 0

        while (x, y) != (dest_x, dest_y):
            if steps >= self.battery:
                return -1  # Not enough battery

            # Move horizontally toward destination
            if x < dest_x and map_obj.is_traversable(x + 1, y):
                x += 1
            elif x > dest_x and map_obj.is_traversable(x - 1, y):
                x -= 1
            # Move vertically toward destination
            elif y < dest_y and map_obj.is_traversable(x, y + 1):
                y += 1
            elif y > dest_y and map_obj.is_traversable(x, y - 1):
                y -= 1
            else:
                return -1  # Blocked, cannot proceed

            steps += 1

        self.battery -= steps
        self.current_position = Position(x, y)
        return steps
