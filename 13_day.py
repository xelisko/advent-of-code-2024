import time
import re


def main():

    f = open("13_input.txt")
    # f = open("13_puzzle.txt")
    line = f.readline().strip()

    tokens = 0
    tokensB = 0
    while line:
        # read three lines
        puzzle = ""
        for i in range(3):
            puzzle += line  # .append(line)
            line = f.readline().strip()
        # extract the integers
        x1, y1, x2, y2, xresult, yresult = extract_pairs(puzzle)
        print(x1, x2, y1, y2, xresult, yresult)
        # solutions = isSolution(x1, x2, xresult,
        #                        y1, y2, yresult)
        # if (len(solutions)!=0):
        #     minTokens = minCost(solutions)
        #     tokens += minTokens
        #     # print (minTokens, tokens)
        # solutionsB = solutionPartB(x1-y1, x2-y2, xresult-yresult)
        solutions = newFunctionb(
            x1, x2, xresult + 10000000000000, y1, y2, yresult + 10000000000000
        )

        # if (len(solutionsB)!=0):
        #     minTokens = minCost(solutionsB)
        #     tokensB += minTokens
        #     print ("cost = ", minTokens)
        line = f.readline().strip()
        # line = False

    print("total tokens Part A = ", tokens)
    print("total tokens Part B = ", tokensB)


def extract_pairs(text):
    # Use a regular expression to find all integers in the text
    integers = re.findall(r"\d+", text)
    # Convert the list of string integers to a list of integers
    integers = [int(num) for num in integers]
    return integers


def minCost(solutions):
    minPrice = -1
    for a, b in solutions:
        price = a * 3 + b
        if (minPrice == -1 or price < minPrice) and price > 0:
            minPrice = price
            print(a, b, minPrice)
    return minPrice


def isSolution(x1, x2, xresult, y1, y2, yresult):
    i = 0
    solutions = []

    while x1 * i <= xresult and y1 * i <= yresult:  # and solution == False:
        xj = (xresult - x1 * i) // x2
        yj = (yresult - y1 * i) // y2
        # print (i, xj, yj)
        if (xresult - x1 * i) % x2 == 0 and (yresult - y1 * i) % y2 == 0 and (xj == yj):
            solutions.append([i, xj])  #  number of pressing button A, b
        i += 1
    return solutions


def newFunctionb(x1, x2, xresult, y1, y2, yresult):
    solutions = []
    x = x1 - y1
    y = x2 - y2
    result = xresult - yresult
    print(x, y, result)
    for b in range(result):
        a = (result - (y * b)) / x
        if ((result - (y * b)) % x == 0) and a > 0 and b > 0:
            # print (x1*a + x2*b)
            # print (a, b)# x1*a + x2*b)
            # if (a*x+(b*y)==result):
            print("solution")
            # if (x1*a + x2*b == xresult+10000000000000): # and y1*a+ y2*b == yresult+10000000000000):
            #     print ("solution")


def solutionPartB(x, y, result):
    a = 1
    b = 0
    solutions = []
    print(x, y, result)

    if y < 0 and result < 0:
        y = -1 * y
        x = -1 * x
        result = -1 * result

        # if (x<0 and result<0):
        #     y = -1 * y
        #     x = -1 * x
        result = -1 * result
    if y == 0 or x == 0:
        print("no solution")
        return solutions

    while a <= result:
        b = (result - x * a) // y
        if a * x + b * y == result:  # ((result-x*a) % y == 0) and (a>0 and b>0)):
            solutions.append([a, b])
            # print ("solution")
        a += 1
    if len(solutions) != 0 and (result != solutions[0][0] * x + solutions[0][1] * y):
        # print("no solution")
        return []
    # sol = []
    # for a,b in solutions:
    #     if (a>0 and b>0):
    #         sol.append
    return solutions


if __name__ == "__main__":
    start = time.time()
    main()
    print("time = ", time.time() - start)
