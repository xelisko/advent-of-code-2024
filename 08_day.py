import time
class Map:
    def __init__(self, map):
        self.grid = map
        self.dict = {}
        self.rows = len(map)
        self.cols = len(map[0])
        self.types = []
        self.antinodes = map
    
    def showMap(self):
        for row in self.grid:
            print (row)

    def showAntinodes(self):
        for row in self.antinodes:
            print (row)

    def clasiffyAntennas(self):
        
        for j, row in enumerate(self.grid):
            for i, ant in enumerate(row):
                if (ant != "."):
                    # print (dict.keys(), dict.values())
                    if (ant in self.dict.keys()):
                        x = self.dict.get(ant)
                        x.append([j,i])
                        self.dict[ant] = x
                    else:
                        self.types.append(ant)
                        self.dict[ant] = [[j,i]]
        # return self.dict
    
    def replaceonmap(self, a):
        x = a[1]
        # add cases for outside of range
        if (a[0] >= self.rows or a[1] >= self.cols or a[0] < 0 or a[1] < 0):
            return
        # add condition for being occupied with an antenna already
        if (self.grid[a[0]][x] == "*"):
            return
        # overwrite only whene there is not antenna 
        self.antinodes[a[0]] = str(self.grid[a[0]][:x]) + "*" + str(self.grid[a[0]][x+1:])
        
        if (self.grid[a[0]][x] != "."):
            return
        self.grid[a[0]] = str(self.grid[a[0]][:x]) + "*" + str(self.grid[a[0]][x+1:])

    def createAntinodes(self, resonantMode = True):
        types = self.types
        print (types)
        for type in types:
            antennas = self.dict.get(type)
            
            for i in range (len(antennas)):
                for j in range (i+1, len(antennas)):
                    self.calculateAntinode(a = antennas[i], b = antennas[j], resonant = resonantMode)

    def calculateAntinode(self, a, b, resonant = True):
        r_diff = b[0] - a[0]
        c_diff = b[1] - a[1]

        # compute
        if (c_diff < 0 ):
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]
        else:
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]
        # print (c,d)

        # mark in the antinode map
        self.replaceonmap(c)
        self.replaceonmap(d)

        if (resonant == False):
            return
        
        # resonant - one way
        self.resonantAntinodes(b,c)
        # resonant - the other way
        self.resonantAntinodesA(d,a)
    
    def resonantAntinodes(self, a, b):
        # calculate the  new d
        r_diff = b[0] - a[0]
        c_diff = b[1] - a[1]
        if (c_diff < 0 ):
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]
        else:
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]

        self.replaceonmap(c)
        if (c[0]>0 and c[1]>0 and c[0]<self.rows and c[1]<self.cols):
            self.resonantAntinodes(b, c)

    def resonantAntinodesA(self, a, b):
        # calculate the  new d
        r_diff = b[0] - a[0]
        c_diff = b[1] - a[1]
        if (c_diff < 0 ):
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]
        else:
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]

        self.replaceonmap(d)
        if (d[0]>0 and d[1]>0 and d[0]<self.rows and d[1]<self.cols):
            self.resonantAntinodesA(d, a)
        return

    def countAntinodes(self):
        a = 0
        for row in self.antinodes:
            a += row.count("*")
        return a

    def countResonantAntinodes(self):
        sum = 0  
        for row in self.antinodes:
            for char in row:
                if (char != "."):
                    sum += 1
        return sum

def main():

    f = open("08_puzzle.txt", "r")
    
    line = f.readline().strip()
    map = []
    antenna_dict = {}
 
    while line:
        map.append(line)
        line = f.readline().strip()

    antenna_plan = Map(map)
    # antenna_plan.showMap()


    # sort out the different tpes of freq antennas
    antenna_plan.clasiffyAntennas()
    
    # create the antinodes
    antenna_plan.createAntinodes(resonantMode = False)
    print ("unique antinodes Part 1 = ", antenna_plan.countAntinodes())
    
    antenna_plan.createAntinodes(resonantMode = True)
    # antenna_plan.showAntinodes()
    print ("unique antinodes Part 2 = ", antenna_plan.countResonantAntinodes())

    return 0

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print ("run time = ", end-start)