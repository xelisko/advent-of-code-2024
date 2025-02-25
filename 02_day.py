import numpy as np


def main():
    # define lists
    safe = 0

    # read the text file
    file = open("02_puzzle.txt", "r")

    line = file.readline().strip()
    while line:
        # map to a list
        levels = list(map(int, line.split(" ")))
        # print(levels)

        # find out if the level is safe, by removing 1:-1 reports
        out = isSafe(levels)
        # print(out)

        if out:
            safe += 1

        if out == False:
            # try fix by removing 0
            b = levels[1:]
            # print(levels, b)
            if isSafe(b, 1):
                # print("first")
                safe += 1
            # else:
            #     print(b,"-ist")

        line = file.readline().strip()
    print("# of safe reports = ", safe)
    file.close()
    return 0


def isSafe(levels, again=0):
    if levels[0] > levels[1]:
        levels = levels[::-1]

    flag = True
    for i in range(len(levels) - 1):
        if (levels[i + 1] <= levels[i]) or (levels[i + 1] > levels[i] + 3):
            # problem found
            # try fix by removng i+1
            if again == 0:
                b = levels[: i + 1] + levels[i + 2 :]
                # print(b)
                if isSafe(b, 1):
                    # print("corrected")
                    continue
            # try fix by removing i
            if again == 0:
                b = levels[:i] + levels[i + 1 :]
                # print(b)
                if isSafe(b, 1):
                    # print("corrected")
                    continue
            flag = False
    return flag


def isFullyAscendingorDescending(report):
    n = len(report)
    n_ascending = 0
    n_descending = 0
    prev_level = report[0]
    for level in report[1:]:
        if level > prev_level:
            n_ascending += 1
        elif level < prev_level:
            n_descending += 1
        prev_level = level
    return (n_ascending == n - 1) or (n_descending == n - 1)


def isDiferenceLargerThanX(report):
    for i, levels in enumerate(report[:-1]):
        if abs(levels - report[i + 1]) > 3:
            return False
    return True


def countTrue(valid_array):
    count = 0
    for result in valid_array:
        if result:
            count += 1
    return count


def isValidWhenXLevelIsRemoved(report):
    for i, _ in enumerate(report):
        new_report = report[:i] + report[i + 1 :]
        new_valid = isFullyAscendingorDescending(new_report) and isDiferenceLargerThanX(
            new_report
        )
        if new_valid:
            return True
    return False


def newMain():
    file = open("02_puzzle.txt", "r")
    line = file.readline().strip()
    reports = []
    validity = []
    while line:
        levels = list(map(int, line.split(" ")))
        reports.append(levels)
        validity.append(
            isFullyAscendingorDescending(levels) and isDiferenceLargerThanX(levels)
        )
        line = file.readline().strip()
    print("star One: # safe reports = ", countTrue(validity))
    # try the star no. 2
    validity_when_level_is_removed = []
    for report in reports:
        validity_when_level_is_removed.append(isValidWhenXLevelIsRemoved(report))
    print("star Two: # safe reports = ", countTrue(validity_when_level_is_removed))
    file.close()
    return 0


if __name__ == "__main__":
    newMain()
