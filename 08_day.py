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
                if (ant is not "."):
                    # print (dict.keys(), dict.values())
                    if (ant in self.dict.keys()):
                        x = self.dict.get(ant)
                        x.append([j,i])
                        self.dict[ant] = x
                    else:
                        self.types.append(ant)
                        self.dict[ant] = [[j,i]]
        return self.dict
    
    def createAntinodes(self):
        type = self.types
        # print (self.types)
        for type in self.types:
            antennas = self.dict.get(type)
            # print (antennas)
            for i in range (len(antennas)):
                for j in range (i+1, len(antennas)):
                    # print (i,j)
                    self.distance(antennas[i], antennas[j])

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

    def distance(self, a, b):
        r_diff = b[0] - a[0]
        c_diff = b[1] - a[1]
        # print ("diffference: ",a,b,r_diff, c_diff)
        # compute
        if (c_diff < 0 ):
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]
        else:
            c = [b[0]+r_diff, b[1]+c_diff]
            d = [a[0]-r_diff, a[1]-c_diff]
        # print (c,d )
        self.replaceonmap(c)
        self.replaceonmap(d)
    
    def produceResonant(self, b, d):
        # calculate the  new d
        # check if d is still in the map
        # if in the map -> mark, recall again
        # if out of map -> return    
        passs

    def countAntinodes(self):
        a = 0
        for row in self.antinodes:
            a += row.count("*")
        return a


def main():

    f = open("08_input.txt", "r")
    
    line = f.readline().strip()
    map = []
    antenna_dict = {}
 
    while line:
        map.append(line)
        line = f.readline().strip()

    antenna_plan = Map(map)
    # antenna_plan.showMap()
    antenna_dict = antenna_plan.clasiffyAntennas()
    print (antenna_dict)
    antenna_plan.createAntinodes()
    # print ("\n \n ")
    # antenna_plan.showMap()
    # print()
    # antenna_plan.showAntinodes()

    print ("unique antinodes = ", antenna_plan.countAntinodes())

    return 0

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print ("run time = ", end-start)