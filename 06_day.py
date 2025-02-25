class Map:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def isObstable(self, position):
        r = position[0]
        c = position[1]

        if self.grid[r][c] == "#":
            return True
        return False

    def getMap(self):
        for row in self.grid:
            print(row)

    def getStartPos(self):
        start_r, start_c = -1, -1
        for r, row in enumerate(self.grid):
            if "^" in row:
                start_c = row.find("^")
                start_r = r
                continue
        if start_r == -1 or start_c == -1:
            print("Error: initial position not found")
        return [start_r, start_c]

    def markVisit(self, pos):
        r = pos[0]
        c = pos[1]

        self.grid[r] = self.grid[r][:c] + "X" + self.grid[r][c + 1 :]
        # print (self.grid[r])

    def move(self, dir, pos):
        r = pos[0]
        c = pos[1]

        match (dir):
            case 1:  # right
                return [r, c + 1]
            case 3:  # left
                return [r, c - 1]
            case 0:  # up
                return [r - 1, c]
            case 2:  # down
                return [r + 1, c]
            case default:
                return [r, c + 1]

    def isInsideMap(self, pos):
        r = pos[0]
        c = pos[1]
        if r <= 0 or c <= 0 or r >= self.rows - 1 or c >= self.cols - 1:
            return False
        return True

    def countVisited(self):
        vis = 0
        for j in range(self.rows):
            for i in range(self.cols):
                if self.grid[j][i] == "X":
                    vis += 1
        return vis

    def changeDir(self, curr_dir):
        new_dir = curr_dir + 1
        if new_dir == 4:
            return 0
        return new_dir


def main():
    f = open("06_puzzle.txt", "r")
    line = f.readline().strip()

    map_read = []

    # read the map
    while line:
        map_read.append(line)
        line = f.readline().strip()

    # initiate the map object
    map = Map(map_read)
    pos = map.getStartPos()
    dir = 0  # "UP"

    print(dir, pos)

    # start moving
    inside = True
    x = 0
    while inside:
        # get the nert position
        next_pos = map.move(dir, pos)
        # print (dir, next_pos)

        # check if there is no obstacle
        obstacle = map.isObstable(next_pos)
        # print (obstacle)

        if obstacle:
            # change direction
            dir = map.changeDir(dir)
            # get new position
            next_pos = map.move(dir, pos)

        # if no obstacle, move there
        map.markVisit(next_pos)
        pos = next_pos

        # check if you are still in the map
        inside = map.isInsideMap(pos)
        # map.getMap()

    # escaped map -> # of visited tiles
    number = map.countVisited()
    print("# of visited tiles", number)
    return 0


if __name__ == "__main__":
    main()
