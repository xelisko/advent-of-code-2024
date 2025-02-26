from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


@dataclass
class Position:
    x: int
    y: int


class Map:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.visited_positions = []
        self.cols = len(grid[0])

    def isObstable(self, position: Position) -> bool:
        if self.grid[position.y][position.x] == "#":
            return True
        return False

    def printMap(self):
        for row in self.grid:
            print(row)

    def getStartPos(self) -> list[int]:
        start_row, start_col = -1, -1
        for i, row in enumerate(self.grid):
            if "^" in row:
                start_col = row.find("^")
                start_row = i
                continue
        if start_row == -1 or start_col == -1:
            print("Error: initial position not found")
        return Position(start_col, start_row)

    def markVisit(self, position: list[int]):
        row = position.y
        col = position.x
        self.grid[row] = self.grid[row][:col] + "X" + self.grid[row][col + 1 :]
        self.visited_positions.append(Position(col, row))
        # print (self.grid[r])

    def calculateNextPosition(
        self, direction: Direction, position: Position
    ) -> Position:
        row = position.y
        col = position.x

        match (direction):
            case Direction.Right:
                return Position(col + 1, row)
            case Direction.Left:
                return Position(col - 1, row)
            case Direction.Up:
                return Position(col, row - 1)
            case Direction.Down:
                return Position(col, row + 1)
            case default:
                return Position(col, row + 1)

    def isInsideMap(self, position: Position) -> bool:
        row = position.y
        col = position.x
        if row <= 0 or col <= 0 or row >= self.rows - 1 or col >= self.cols - 1:
            return False
        return True

    def countVisited(self) -> int:
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == "X":
                    count += 1
        return count

    def changeDirection(self, curr_dir: Direction) -> Direction:
        match (curr_dir):
            case Direction.Right:
                return Direction.Down
            case Direction.Down:
                return Direction.Left
            case Direction.Left:
                return Direction.Up
            case Direction.Up:
                return Direction.Right

    def getVisitedPositions(self):
        for visited_tile in self.visited_positions:
            print(visited_tile)

    def selectStones(self) -> list[Position]:
        stones_positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == "#":
                    stones_positions.append(Position(col, row))
        return stones_positions

    # def selectAllStoneTriples(self):
    #     all_stones = self.selectStones()
    #     for i in range(all_stones):
    #         for j in range(all_stones[i:]):
    #             for z in range(all_stones[j:]):


def main():
    with open("06_input.txt") as f:
        map_grid = []
        for line in f:
            map_grid.append(line.strip())

    # initiate the MAP OBJECT
    map = Map(map_grid)
    curr_position = map.getStartPos()
    curr_direction = Direction.Up

    print(curr_direction, curr_position)

    # start moving
    inside = True
    x = 0
    while inside:
        # get the nert position
        next_position = map.calculateNextPosition(curr_direction, curr_position)
        # print (curr_direction, next_position)

        # check if there is no obstacle
        isObstacle = map.isObstable(next_position)

        if isObstacle:
            curr_direction = map.changeDirection(curr_direction)
            next_position = map.calculateNextPosition(curr_direction, curr_position)

        # if no obstacle, move there
        map.markVisit(next_position)
        curr_position = next_position

        # check if you are still in the map
        inside = map.isInsideMap(curr_position)
        # map.getMap()

    # escaped map -> # of visited tiles
    number = map.countVisited()
    print("# of visited tiles", number)
    map.printMap()
    # map.getVisitedPositions()
    return 0


if __name__ == "__main__":
    main()
