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


def checkAllDiagonalTop(wordGrid: list[str], word: str) -> int:
    combinations = []
    n = len(wordGrid[0])
    for i in range(len(wordGrid)):  # starting columns
        diagonal_to_left = ""
        diagonal_to_right = ""
        for j in range(len(wordGrid) - i):  # starting line
            diagonal_to_left += wordGrid[j][i + j]
            try:
                diagonal_to_right += wordGrid[j][n - j]
            except:
                continue
        combinations.append(diagonal_to_right)
        combinations.append(diagonal_to_left)
    return countWordInList(combinations, word)
    # diagonal = "".join(word_grid[x][i + x] for x in range(lenght - i))


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


def diagonals(word_grid: list[int], count: int):
    diagonal = []
    diagonal1 = []
    n = len(word_grid)
    print(len(word_grid), len(word_grid[0]))
    # from left top corner - bottom
    for i in range(n):
        diagonal.append("".join(word_grid[i + j][j] for j in range(n - i)))
        diagonal.append("".join(word_grid[i + j][n - j - 1] for j in range(n - i)))
    # from left top corner - top
    for i in range(1, n):
        diagonal1.append("".join(word_grid[j][i + j] for j in range(n - i)))
        diagonal1.append("".join(word_grid[j][n - i - 1 - j] for j in range(n - i)))
    print("count = ", count)
    print(countWordInList(diagonal, "XMAS"))
    print(countWordInList(diagonal1, "XMAS"))
    # print(diagonal1)
    return countWordInList(diagonal, "XMAS") + countWordInList(diagonal1, "XMAS")


def main():
    word_grid = []
    with open("04_input.txt") as file:
        for line in file:
            word_grid.append(line.strip())
    count = 0
    count += countWordInList(word_grid, "XMAS")
    # transpose the word grid
    word_grid_transpose = ["".join(char) for char in zip(*word_grid)]
    count += countWordInList(word_grid_transpose, "XMAS")

    print("countfinally correct = ", count + diagonals(word_grid, count))

    count += checkAllDiagonalTop(word_grid, "XMAS")
    count += checkAllDiagonalBottom(word_grid, "XMAS")
    print("new count", count)


if __name__ == "__main__":
    main()
