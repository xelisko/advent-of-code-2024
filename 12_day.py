import time


class Garden:
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.counted = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.regionPlots = 0
        self.corners = []
        pass

    def showMap(self):
        for row in self.map:
            print(row)

    def showCounted(self):
        for row in self.counted:
            print(row)

    def showCorners(self):
        for row in self.corners:
            print(row)

    def getFencingPrice(self):
        price = 0
        for i, row in enumerate(self.map):
            for j, plant in enumerate(row):
                # checks if already processed
                if self.counted[i][j] == 0:
                    print("started with", plant)
                    # start tracing the region - Task 1
                    self.regionPlots = []
                    a, n = self.findRegion(i, j, plant)
                    price += a * (4 * a - n)

                    # start tracing outline for that region
                    self.startCornerChase(i, j)
                    return price
        return price

    def findRegion(self, row, col, plant):
        # print (plant, row, col)
        self.counted[row][col] = 1
        self.regionPlots.append([row, col])
        area = 1
        nghbrs = 0
        edgeCase = True
        # search one below in every direction
        # if: within bounds, match, uncounted
        if col + 1 < self.cols and self.map[row][col + 1] == plant:
            nghbrs += 1
            if self.counted[row][col + 1] == 0:
                a, n = self.findRegion(row, col + 1, plant)
                area += a
                nghbrs += n
        if col - 1 >= 0 and self.map[row][col - 1] == plant:
            nghbrs += 1
            if self.counted[row][col - 1] == 0:
                a, n = self.findRegion(row, col - 1, plant)
                area += a
                nghbrs += n
        if row + 1 < self.rows and self.map[row + 1][col] == plant:
            nghbrs += 1
            if self.counted[row + 1][col] == 0:
                a, n = self.findRegion(row + 1, col, plant)
                area += a
                nghbrs += n
        if row - 1 >= 0 and self.map[row - 1][col] == plant:
            nghbrs += 1
            if self.counted[row - 1][col] == 0:
                a, n = self.findRegion(row - 1, col, plant)
                area += a
                nghbrs += n
        return area, nghbrs

    def get(self, x, y):
        if x < 0 or y < 0:
            return None
        if x >= self.cols or y >= self.rows:
            return None
        return self.map[y][x]

    def isEdge(self, x0, y0, x1, y1, plant):
        # if (self.get(x0, y0) == self.get(x1, y1)):
        #    return
        assert abs(x0 - x1) <= 1 and abs(y0 - y1) <= 1
        assert (x0 != x1) or (y0 != y1)
        assert x0 == x1 or y0 == y1
        # assert self.corners != 0 and [x1, y1] not in self.corners

        if x0 == x1:
            if y0 > y1:  # up
                type0 = self.get(x0, y0 - 1)
                type1 = self.get(x0 - 1, y0 - 1)
                return (type0 != type1) and ((type0 == plant) or (type1 == plant))
            else:  # down
                # convert the edge between corners into tiles that have that edge
                type0 = self.get(x0, y0)
                type1 = self.get(x0 - 1, y0)
                return type0 != type1 and ((type0 == plant) or (type1 == plant))
        else:
            if x0 > x1:  # left1
                type0 = self.get(x0 - 1, y0)
                type1 = self.get(x0 - 1, y0 - 1)
                return type0 != type1 and ((type0 == plant) or (type1 == plant))
            else:  # right
                type0 = self.get(x0, y0)
                type1 = self.get(x0, y0 - 1)
                return type0 != type1 and ((type0 == plant) or (type1 == plant))

    def detectOutline(self, row, col, prevRow, prevCol, prev_dir):
        plant = self.get(col, row)
        print("plant type", plant)
        print("outline edge", row, col, prev_dir)

        if [row, col] in self.corners:
            # we got back to the starting corner
            return

        # try the corner on the right
        if (
            prevRow != row
            and prevCol != col + 1
            and self.isEdge(row, col, row, col + 1, plant)
        ):
            curr_dir = [0, +1]
            print("starting right")
            if prev_dir != curr_dir:
                print("new corner")
                self.corners.append([prevRow, prevCol])
            self.detectOutline(row, col + 1, row, col, curr_dir)
        # left
        elif (
            prevRow != row
            and prevCol != col - 1
            and self.isEdge(row, col, row, col - 1, plant)
        ):
            curr_dir = [0, -1]
            if prev_dir != curr_dir:
                print("new corner")
                self.corners.append(([row, col]))
            self.detectOutline(row, col - 1, row, col, curr_dir)
        # up
        elif (
            prevRow != row - 1
            and prevCol != col
            and self.isEdge(row, col, row - 1, col, plant)
        ):
            curr_dir = [-1, 0]
            if prev_dir != curr_dir:
                print("new corner")
                self.corners.append(([row, col]))
            self.detectOutline(row - 1, col, row, col, curr_dir)
        # down
        elif (
            prevRow != row + 1
            and prevCol != col
            and self.isEdge(row, col, row + 1, col, plant)
        ):
            curr_dir = [+1, 0]
            if prev_dir != curr_dir:
                print("new corner")
                self.corners.append([row, col])
            self.detectOutline(row + 1, col, row, col, curr_dir)

        return

    def startCornerChase(self, row, col):
        self.detectOutline(row, col, row - 1, col - 1, [0, 0])

    # def determineDirection(self, row, col, plant):
    #     if col + 1 < self.cols and self.map[row][col + 1] == plant:
    #         self.corners[row][col] = 1
    #         self.corners[row + 1][col] = 1
    #         self.findCorners([0, 1])
    #     elif col - 1 >= 0 and self.map[row][col - 1] == plant:
    #         self.corners[row][col] = 1
    #         self.corners[row + 1][col] = 1
    #         self.findCorners([0, -1])
    #     elif row + 1 < self.rows and self.map[row + 1][col] == plant:
    #         self.corners[row][col] = 1
    #         self.corners[row][col + 1] = 1
    #         self.findCorners([+1, 0])
    #     elif row - 1 >= 0 and self.map[row - 1][col] == plant:
    #         self.corners[row][col] = 1
    #         self.corners[row + 1][col] = 1
    #         self.findCorners([-1, 0])
    #     else:
    #         return 4  # corners

    # def findCorners(self, prev_direction, row, col):
    #     #     for row in co
    #     # find out the next direction
    #     next_direction = [1, 1]
    #     # if different --> new corner
    #     if prev_direction != next_direction:
    #         # mark corner based on the previous direction
    #         self.corners[row + prev_direction[0]][col + prev_direction[1]] = 1

    #     pass


def main():

    f = open("12_input.txt")
    # f = open("12_puzzle.txt")
    line = f.readline().strip()
    # IDs = []
    space = []
    # id = 0

    # read the line
    while line:
        space.append(line)
        line = f.readline().strip()

    garden = Garden(space)
    # garden.showMap()
    print("price = ", garden.getFencingPrice())


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
