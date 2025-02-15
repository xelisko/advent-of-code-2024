import time


class Room:
    def __init__(self, map):
        self.map = map
        self.mapriginal = map
        self.largeMap = []

    def showMap(self):
        for row in self.map:
            print(row)

    def showLargeMap(self):
        for row in self.largeMap:
            print(row)

    def countScore(self):
        score = 0
        for r, row in enumerate(self.map):
            for c, item in enumerate(row):
                if item == "O":
                    score += 100 * r + c
        return score

    def enlargeMap(self, originalMap):
        large = []
        start_pos = []
        for r, row in enumerate(originalMap):
            newRow = ""
            for c, item in enumerate(row):
                if item == "#":
                    newRow += "##"
                elif item == "O":
                    newRow += "[]"
                elif item == ".":
                    newRow += ".."
                elif item == "@":
                    newRow += "@."
                    start_pos = [c * 2, r]
            large.append(newRow)
        self.largeMap = large
        return start_pos

    def findNDoubleBoxes(self, x, y, move, n, bracket):
        outn = 0
        outbool = False
        if (
            self.largeMap[y][x] == "["
            and self.largeMap[y][x + 1] == "]"
            or self.largeMap[y][x] == "]"
            and self.largeMap[y][x - 1] == "["
        ):
            if move[0] == 0 and bracket == "]" and self.largeMap[y][x] == "[":
                return n, False
            if move[0] == 0 and bracket == "[" and self.largeMap[y][x] == "]":
                return n, False
            print("next box", n)
            outn, outbool = self.findNDoubleBoxes(
                x + move[0], y + move[1], move, n + 1, bracket
            )
        elif (  # for up and down
            move[0] == 0
            and self.largeMap[y][x] == "."
            and self.largeMap[y][x + 1] == "."
        ):
            print("final space", n)
            return n, True
        elif move[1] == 0 and self.largeMap[y][x] == ".":  # for left and right
            print("final space", n)
            return n, True
        else:
            return n, False
        return outn, outbool

    def findDoubleBoxesHorizontally(self, x, y, move, n):
        outn = 0
        outbool = False
        if (
            self.largeMap[y][x] == "["
            and self.largeMap[y][x + 1] == "]"
            or self.largeMap[y][x] == "]"
            and self.largeMap[y][x - 1] == "["
        ):
            print("next box", n)
            outn, outbool = self.findNDoubleBoxes(x + move[0], y + move[1], move, n + 1)
        elif self.largeMap[y][x] == "." and self.largeMap[y][x + 1] == ".":
            print("final space", n)
            return n, True
        else:
            return n, False
        return outn, outbool

    def findNboxes(self, x, y, move, n):
        outn = 0
        outbool = False
        if self.map[y][x] == "O":
            # print("next box", n)
            outn, outbool = self.findNboxes(x + move[0], y + move[1], move, n + 1)
        elif self.map[y][x] == ".":
            # print("final space", n)
            return n, True
        else:
            return n, False
        return outn, outbool

    def moveRobot(self, instructions, curr_position):
        x = curr_position[0]
        y = curr_position[1]
        for step in instructions:
            # self.showMap()
            # print(step)
            if step == "^" and y - 1 > 0:
                # #print(self.map[y - 1][x])
                if self.map[y - 1][x] == "#":
                    # #print("wall")
                    continue

                elif self.map[y - 1][x] == ".":
                    # print("volno")
                    self.map[y - 1] = (
                        self.map[y - 1][:x] + "@" + self.map[y - 1][x + 1 :]
                    )
                    self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]
                    y -= 1
                    continue

                if self.map[y - 1][x] == "O":
                    # compute
                    # print("here")
                    n, isSpace = self.findNboxes(x, y - 1, [0, -1], 0)
                    # print(n, isSpace)
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
                # print(x, y)
                # print(self.map[y + 1][x])
                if self.map[y + 1][x] == "#":
                    # print("wall")
                    continue

                elif self.map[y + 1][x] == ".":
                    # print("volno")
                    self.map[y + 1] = (
                        self.map[y + 1][:x] + "@" + self.map[y + 1][x + 1 :]
                    )
                    self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]
                    y += 1
                    continue

                if self.map[y + 1][x] == "O":
                    # compute
                    # print("here")
                    n, isSpace = self.findNboxes(x, y + 1, [0, +1], 0)
                    # print(n, isSpace)
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
                    # print(x, y)
                    continue

            elif step == ">":
                # print(self.map[y][x + 1])
                if self.map[y][x + 1] == "#":
                    # print("wall")
                    continue

                elif self.map[y][x + 1] == ".":
                    # print("volno")
                    self.map[y] = self.map[y][:x] + ".@" + self.map[y][x + 2 :]
                    x += 1
                    continue

                if self.map[y][x + 1] == "O":
                    # compute
                    # print("here")
                    n, isSpace = self.findNboxes(x + 1, y, [+1, 0], 0)
                    # print(n, isSpace)
                    if isSpace:
                        # move  robot and n boxes
                        self.map[y] = (
                            self.map[y][:x] + ".@" + "O" * n + self.map[y][x + n + 2 :]
                        )
                        x += 1
                    continue

            elif step == "<":
                # print(self.map[y][x - 1])
                if self.map[y][x - 1] == "#":
                    # print("wall")
                    continue

                elif self.map[y][x - 1] == ".":
                    # print("volno")
                    self.map[y] = self.map[y][: x - 1] + "@." + self.map[y][x + 1 :]
                    x -= 1
                    continue

                if self.map[y][x - 1] == "O":
                    # compute
                    # print("here")
                    n, isSpace = self.findNboxes(x - 1, y, [-1, 0], 0)
                    # print(n, isSpace)
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

    def moveRobotLargeMap(self, instructions, curr_position):
        x = curr_position[0]
        y = curr_position[1]
        for step in instructions:
            self.showLargeMap()
            print(step)
            if step == "^" and y - 1 > 0:
                print(self.largeMap[y - 1][x])
                if self.largeMap[y - 1][x] == "#":
                    print("wall")
                    continue

                elif self.largeMap[y - 1][x] == ".":
                    print("volno")
                    self.largeMap[y - 1] = (
                        self.largeMap[y - 1][:x] + "@" + self.largeMap[y - 1][x + 1 :]
                    )
                    self.largeMap[y] = (
                        self.largeMap[y][:x] + "." + self.largeMap[y][x + 1 :]
                    )
                    y -= 1
                    continue

                if (
                    self.largeMap[y - 1][x] == "["
                    and self.largeMap[y - 1][x + 1] == "]"
                ) or (
                    self.largeMap[y - 1][x] == "]"
                    and self.largeMap[y - 1][x - 1] == "["
                ):
                    # compute
                    print("here")

                    n, isSpace = self.findNDoubleBoxes(
                        x, y - 1, [0, -1], 0, self.largeMap[y - 1][x]
                    )
                    print(n, isSpace)
                    if isSpace:
                        # move robot
                        self.largeMap[y - 1] = (
                            self.largeMap[y - 1][:x]
                            + "@."
                            + self.largeMap[y - 1][x + 2 :]
                        )
                        self.largeMap[y] = (
                            self.largeMap[y][:x] + "." + self.largeMap[y][x + 1 :]
                        )
                        # move n boxes
                        self.largeMap[y - n - 1] = (
                            self.largeMap[y - n - 1][:x]
                            + "[]"
                            + self.largeMap[y - n - 1][x + 2 :]
                        )
                        y -= 1
                    continue
            if step == "v" and y + 1 < len(self.largeMap):
                print(self.largeMap[y + 1][x])
                if self.largeMap[y + 1][x] == "#":
                    print("wall")
                    continue

                elif self.largeMap[y + 1][x] == ".":
                    print("volno")
                    self.largeMap[y + 1] = (
                        self.largeMap[y + 1][:x] + "@" + self.largeMap[y + 1][x + 1 :]
                    )
                    self.largeMap[y] = (
                        self.largeMap[y][:x] + "." + self.largeMap[y][x + 1 :]
                    )
                    y += 1
                    continue

                if (
                    self.largeMap[y + 1][x] == "["
                    and self.largeMap[y + 1][x + 1] == "]"
                ) or (
                    self.largelargeMap[y + 1][x] == "]"
                    and self.largelargeMap[y + 1][x - 1] == "["
                ):
                    # compute
                    print("here")

                    n, isSpace = self.findNDoubleBoxes(
                        x, y + 1, [0, +1], 0, self.largeMap[y + 1][x]
                    )
                    print(n, isSpace)
                    if isSpace:
                        # move robot
                        self.largeMap[y + 1] = (
                            self.largeMap[y + 1][:x]
                            + "@."
                            + self.largeMap[y + 1][x + 2 :]
                        )
                        self.largeMap[y] = (
                            self.largeMap[y][:x] + "." + self.largeMap[y][x + 1 :]
                        )
                        # move n boxes
                        self.largeMap[y + n + 1] = (
                            self.largeMap[y + n + 1][:x]
                            + "[]"
                            + self.largeMap[y + n + 1][x + 2 :]
                        )
                        y += 1
                    continue

            if step == ">":
                print(self.largeMap[y][x + 1])
                if self.largeMap[y][x + 1] == "#":
                    print("wall")
                    continue

                elif self.largeMap[y][x + 1] == ".":
                    print("volno")
                    self.largeMap[y] = (
                        self.largeMap[y][:x] + ".@" + self.largeMap[y][x + 2 :]
                    )
                    x += 1
                    continue

                if self.largeMap[y][x + 1] == "[" and self.largeMap[y][x + 2] == "]":
                    # compute
                    print("here")

                    n, isSpace = self.findNDoubleBoxes(x + 1, y, [+1, 0], 0, "[")
                    print(n, isSpace)
                    if isSpace:
                        z = n // 2
                        # move robot and boxes
                        self.largeMap[y] = (
                            self.largeMap[y][:x]
                            + ".@"
                            + "[]" * z
                            + self.largeMap[y][x + n + 2 :]
                        )
                        x += 1
                    continue
            if step == "<":
                print(self.largeMap[y][x - 1])
                if self.largeMap[y][x - 1] == "#":
                    print("wall")
                    continue

                elif self.largeMap[y][x - 1] == ".":
                    print("volno")
                    self.largeMap[y] = (
                        self.largeMap[y][: x - 1] + "@." + self.largeMap[y][x + 1 :]
                    )
                    x -= 1
                    continue

                if self.largeMap[y][x - 1] == "]" and self.largeMap[y][x - 2] == "[":
                    # compute
                    print("here")

                    n, isSpace = self.findNDoubleBoxes(x - 1, y, [-1, 0], 0, "]")
                    print(n, isSpace)
                    if isSpace:
                        z = n // 2
                        # move robot and boxes
                        self.largeMap[y] = (
                            self.largeMap[y][: x - n - 1]
                            + "[]" * z
                            + "@."
                            + self.largeMap[y][x + 1 :]
                        )
                        x -= 1
                    continue


def main():
    f = open("15_input.txt", "r")
    # f = open("15_puzzle.txt", "r")
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

    startPosLargeMap = top_map.enlargeMap(map)
    print("Part 1 starting pos:", start)
    print("Part 2 starting pos:", startPosLargeMap)
    # top_map.showMap()
    top_map.showLargeMap()

    top_map.moveRobot(instructions, start)
    print(top_map.countScore())
    top_map.moveRobotLargeMap(instructions, startPosLargeMap)

    return 0


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
