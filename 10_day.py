
class Map:
    def __init__(self, map):
        self.map = map
        self.dict = {}
        self.rows = len(map)
        self.cols = len(map[0])
        self.tailHeadRatings = [[ 0 for j in range (self.cols)] for i in range (self.rows)]
        self.tailHeadScores = [[ 0 for j in range (self.cols)] for i in range (self.rows)]
        self.tickOffGrid = [[ 0 for x in range (self.cols)] for z in range (self.rows)]

    def showMap(self):
        for row in self.map:
            print (row)

    def showTailHeadScores(self):
        for row in self.tailHeadRatings:
            print(row)
        
    def countTailheadScores(self):
        return sum(sum(row) for row in self.tailHeadScores)

    def countTailheadRatings(self):
        return sum(sum(row) for row in self.tailHeadRatings)

    def countTickOffGrid(self):
        # returns rating
        return sum(sum(row) for row in self.tickOffGrid)
    
    def countTickOffScores(self):
        # returns scores
        sum = 0
        for row in self.tickOffGrid:
            for item in row:
                if (item != 0):
                    sum += 1
        return sum

    def findPath(self):
        for i,row in enumerate(self.map):
            tailHead = row.find('0')
            while tailHead != -1:
                # clear the grid 
                self.tickOffGrid = [[ 0 for x in range (self.cols)] for z in range (self.rows)]
                # search for all possible paths to the reachable peaks (9)
                self.findNext(i, tailHead, 0)
                # count unique reach peaks
                tailhead_rating = self.countTickOffGrid()
                tailhead_score = self.countTickOffScores()
                # print (i, tailHead, tailhead_score)
                # save the score and rating
                self.tailHeadScores[i][tailHead] = tailhead_score
                self.tailHeadRatings[i][tailHead] = tailhead_rating
                # move to the next tail head
                tailHead = row.find('0', tailHead+1)
        return

    def findNext(self, row, col, x):
        # if 9 is reached
        if (self.map[row][col] == str(9)): 
            # if not marked yet, mark
            # if (self.tickOffGrid[row][col] == 0):
            self.tickOffGrid[row][col] += 1
                # print ("9 found", row, col)
            return
        # search one below in every direction
        if (col+1<self.cols and self.map[row][col+1] == str(x+1)):
            self.findNext(row, col+1, x+1)
        if (col-1>=0 and self.map[row][col-1] == str(x+1)):
            self.findNext(row, col-1, x+1)
        if (row+1<self.rows and self.map[row+1][col] == str(x+1)):
            self.findNext(row+1, col, x+1)
        if (row-1>=0 and self.map[row-1][col] == str(x+1)):
            self.findNext(row-1, col, x+1)
        return

def main():
    # f = open("10_input.txt", "r")
    f = open("10_puzzle.txt", "r")
    line = f.readline().strip()

    map = []
    # read the line
    while line:
        map.append(line)
        line = f.readline().strip()
    top_map  = Map(map)

    top_map.showMap()
    top_map.findPath()
    # top_map.showTailHeadScores()
    print ("part 1 = ", top_map.countTailheadScores())
    print ("part 2 = ", top_map.countTailheadRatings())


    return 0


if __name__ == "__main__":
    main()