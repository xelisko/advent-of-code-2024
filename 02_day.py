import numpy as np


def main():
    # define lists
    safe = 0 

    # read the text file
    file = open('input01.txt', 'r')
    line = file.readline().strip()
    while line:
        levels = list(map(int, line.split(' ')))
        out = isSafe(levels)
        print (out)
        if (out):
            safe += 1
        line = file.readline().strip()
    print ("# of safe reports = ", safe)
    file.close()
    return 0


def isSafe(levels, again = 0):
    type = True # true - increasing, false - decreasing
    if (levels[0] < levels[1]):
        type = True
    elif (levels[0] > levels[2]):
        levels.reverse()
    #     type = False
    # else:
    #     return False
    
    flag = True
    for i in range (len(levels)-1):
        # it must be larger but not by more than 3
        if (type):
            if (levels[i+1] <= levels[i]) or (levels[i+1] > levels[i]+3):
                if (again == 0):
                    b = levels[:i+1] + levels[i+2:]
                    if (isSafe(b, 1)):
                        # print ("corrected")
                        continue
                flag = False
        else: # descending
            if (levels[i+1] >= levels[i]) or (levels[i+1] < levels[i]-3):
                if (again == 0):
                    b = levels[:i+1] + levels[i+2:]
                    if (isSafe(b, 1)):
                        # print ("corrected")
                        continue
                flag = False
    return flag

if __name__ == "__main__":
    main()
