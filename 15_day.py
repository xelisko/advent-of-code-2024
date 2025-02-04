import time


class Room:
    def __init__(self, map):
        self.map = map

    def showMap(self):
        for row in self.map:
            print(row)

    def countScore(self):
        score = 0
        for r, row in enumerate(self.map):
            for c, item in enumerate(row):
                if item == "O":
                    score += 100 * r + c
        return score

    def findNboxes(self, x, y, move, n):
        outn = 0
        outbool = False
        if self.map[y][x] == "O":
            print("next box", n)
            outn, outbool = self.findNboxes(x + move[0], y + move[1], move, n + 1)
        elif self.map[y][x] == ".":
            print("final space", n)
            return n, True
        else:
            return n, False
        return outn, outbool

    def moveNboxes(self, x, y, n):
        self.map[y - n] = self.map[y - n][:x] + "N" + self.map[y - n][x + 1 :]

    def moveRobot(self, instructions, curr_position):
        x = curr_position[0]
        y = curr_position[1]
        for step in instructions:
            # self.showMap()
            print(step)
            if step == "^" and y - 1 > 0:
                print(self.map[y - 1][x])
                if self.map[y - 1][x] == "#":
                    print("wall")
                    continue

                elif self.map[y - 1][x] == ".":
                    print("volno")
                    self.map[y - 1] = (
                        self.map[y - 1][:x] + "@" + self.map[y - 1][x + 1 :]
                    )
                    self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]
                    y -= 1
                    continue

                if self.map[y - 1][x] == "O":
                    # compute
                    print("here")
                    n, isSpace = self.findNboxes(x, y - 1, [0, -1], 0)
                    print(n, isSpace)
                    if isSpace:
                        # move robot
                        self.map[y - 1] = (
                            self.map[y - 1][:x] + "@" + self.map[y - 1][x + 1 :]
                        )
                        self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]
                        # move n boxes
                        self.map[y - n - 1] = (
                            self.map[y - n - 1][:x] + "O" + self.map[y - n - 1][x + 1 :]
                        )
                        y -= 1
                    continue

            elif step == "v":
                print(x, y)
                print(self.map[y + 1][x])
                if self.map[y + 1][x] == "#":
                    print("wall")
                    continue

                elif self.map[y + 1][x] == ".":
                    print("volno")
                    self.map[y + 1] = (
                        self.map[y + 1][:x] + "@" + self.map[y + 1][x + 1 :]
                    )
                    self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]
                    y += 1
                    continue

                if self.map[y + 1][x] == "O":
                    # compute
                    print("here")
                    n, isSpace = self.findNboxes(x, y + 1, [0, +1], 0)
                    print(n, isSpace)
                    if isSpace:
                        # move robot
                        self.map[y + 1] = (
                            self.map[y + 1][:x] + "@" + self.map[y + 1][x + 1 :]
                        )
                        self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]
                        # move n boxes
                        self.map[y + n + 1] = (
                            self.map[y + n + 1][:x] + "O" + self.map[y + n + 1][x + 1 :]
                        )
                        y += 1
                    print(x, y)
                    continue

            elif step == ">":
                print(self.map[y][x + 1])
                if self.map[y][x + 1] == "#":
                    print("wall")
                    continue

                elif self.map[y][x + 1] == ".":
                    print("volno")
                    self.map[y] = self.map[y][:x] + ".@" + self.map[y][x + 2 :]
                    x += 1
                    continue

                if self.map[y][x + 1] == "O":
                    # compute
                    print("here")
                    n, isSpace = self.findNboxes(x + 1, y, [+1, 0], 0)
                    print(n, isSpace)
                    if isSpace:
                        # move  robot and n boxes
                        self.map[y] = (
                            self.map[y][:x] + ".@" + "O" * n + self.map[y][x + n + 2 :]
                        )
                        x += 1
                    continue

            elif step == "<":
                print(self.map[y][x - 1])
                if self.map[y][x - 1] == "#":
                    print("wall")
                    continue

                elif self.map[y][x - 1] == ".":
                    print("volno")
                    self.map[y] = self.map[y][: x - 1] + "@." + self.map[y][x + 1 :]
                    x -= 1
                    continue

                if self.map[y][x - 1] == "O":
                    # compute
                    print("here")
                    n, isSpace = self.findNboxes(x - 1, y, [-1, 0], 0)
                    print(n, isSpace)
                    if isSpace:
                        # move  robot and n boxes
                        self.map[y] = (
                            self.map[y][: x - n - 1]
                            + "O" * n
                            + "@."
                            + self.map[y][x + 1 :]
                        )
                        x -= 1
                    continue


def main():
    # f = open("15_input.txt", "r")
    f = open("15_puzzle.txt", "r")
    line = f.readline().strip()

    map = []
    y = 0
    # read the line
    while line != "":
        map.append(line)
        if line.find("@") != -1:
            x = line.find("@")
            start = [x, y]
        y += 1
        line = f.readline().strip()
    top_map = Room(map)

    line = f.readline().strip()
    instructions = ""
    while line:
        instructions += line
        line = f.readline().strip()

    print(instructions)
    print(start)
    top_map.moveRobot(instructions, start)
    print(top_map.countScore())

    return 0


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
