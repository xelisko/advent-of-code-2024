def main():
    # define variables
    word_grid = []
    xmas = "XMAS"

    # read input
    file = open("04_puzzle.txt", "r")
    line = file.readline().strip()

    while line:
        word_grid.append(line)
        line = file.readline().strip()

    # search horizontally
    count = 0
    for line in word_grid:
        count += searchForPhrase(line, xmas)

    print("horizontal count = ", count)

    # search vertically
    for i in range(len(word_grid)):
        column = "".join([s[i] for s in word_grid if s])
        count += searchForPhrase(column, xmas)

    print("after vertical count = ", count)

    # diagonal
    lenght = len(word_grid[0])
    a = 0
    b = 0

    for i in range(len(word_grid[0]) - 3):
        diagonal = "".join(word_grid[x][i + x] for x in range(lenght - i))
        a += searchForPhrase(diagonal, xmas)
        # print(diagonal, a)

        if i != 0:
            word_opposite = "".join(word_grid[i + x][x] for x in range(lenght - i))
            a += searchForPhrase(word_opposite, xmas)
            # print(word_opposite, a)

        flipped_diagonal = "".join(
            word_grid[x][lenght - i - 1 - x] for x in range(lenght - i)
        )
        b += searchForPhrase(flipped_diagonal, xmas)
        # print(flipped_diagonal, b)

        if i != 0:
            flipped_diagonal2 = "".join(
                word_grid[lenght - 1 - x][x + i] for x in range(lenght - i)
            )
            b += searchForPhrase(flipped_diagonal2, xmas)
            # print(flipped_diagonal2, b)
    count = count + b + a

    print("after diagonal count = ", count)

    return 0


def countWordInList(combinations: list[str], word: str, printflag=False) -> int:
    count = 0
    for line in combinations:
        count += line.count(word)
        count += line.count(word[::-1])
        if word in line and printflag:
            print(line, line.count(word))
        if word[::-1] in line and printflag:
            print(line, line.count(word[::-1]), "r")
    return count


def checkAllHorizontal(wordGrid: list[str], word: str) -> int:
    return countWordInList(wordGrid, word)


def checkAllVertical(wordGrid: list[str], word: str) -> int:
    combinations = []
    for i in range(len(wordGrid[0])):  # letter
        new_word = ""
        for j in range(len(wordGrid)):  # line
            new_word += wordGrid[j][i]
        combinations.append(new_word)
    return countWordInList(combinations, word)


def checkAllDiagonalTop(wordGrid: list[str], word: str) -> int:
    combinations = []
    n = len(wordGrid[0])
    for i in range(len(wordGrid[0])):  # starting columns
        diagonal_to_left = ""
        diagonal_to_right = ""
        for j in range(len(wordGrid)):  # starting line
            try:
                diagonal_to_left += wordGrid[j][i + j]
                diagonal_to_right += wordGrid[j][n - j]
            except:
                continue
        combinations.append(diagonal_to_right)
        combinations.append(diagonal_to_left)
    return countWordInList(combinations, word)


def checkAllDiagonalBottom(wordGrid: list[str], word: str) -> int:
    combinations = []
    n = len(wordGrid[0]) - 1
    for j in range(1, len(wordGrid)):  # starting line
        diagonal_to_left = ""
        diagonal_to_right = ""
        for i in range(len(wordGrid[0])):  # starting column - always the same
            try:
                diagonal_to_left += wordGrid[j + i][i]
                diagonal_to_right += wordGrid[j + i][n - i]
            except:
                continue
        combinations.append(diagonal_to_right)
        combinations.append(diagonal_to_left)
    return countWordInList(combinations, word)


def newMain():
    word_grid = []
    with open("04_puzzle.txt") as file:
        for line in file:
            word_grid.append(line.strip())
    count = 0
    count += checkAllHorizontal(word_grid, "XMAS")
    count += checkAllVertical(word_grid, "XMAS")
    count += checkAllDiagonalTop(word_grid, "XMAS")
    count += checkAllDiagonalBottom(word_grid, "XMAS")
    print("new count", count)


def searchForPhrase(word, xmas):
    count = 0

    a = word.find(xmas)
    while a != -1:
        count += 1
        a = word.find(xmas, a + 1)

    a = word.find(xmas[::-1])
    while a != -1:
        count += 1
        a = word.find(xmas, a + 1)

    return count


if __name__ == "__main__":
    # main()
    newMain()
