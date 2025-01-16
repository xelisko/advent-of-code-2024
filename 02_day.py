import numpy as np


def main():
    # define lists
    safe = 0 

    # read the text file
    file = open('input01.txt', 'r')

    line = file.readline().strip()
    while line:
        # map to a list
        levels = list(map(int, line.split(' ')))
        print (levels)

        # find out if the level is safe, by removing 1:-1 reports
        out = isSafe(levels)
        print (out)

        if (out):
            safe += 1
        
        if (out == False):
            # try fix by removing 0
            b = levels[1:]
            print (levels, b)
            if (isSafe(b, 1)):
                print ("first")
                safe += 1
            else:
                print("nist")
        
        line = file.readline().strip()
    print ("# of safe reports = ", safe)
    file.close()
    return 0



def isSafe(levels, again = 0):
    if (levels[0] > levels[1]):
        levels = levels[::-1]
    
    flag = True
    for i in range (len(levels)-1):
        if (levels[i+1] <= levels[i]) or (levels[i+1] > levels[i]+3):
            # problem found
            # try fix by removng i+1
            if (again == 0):
                b = levels[:i+1] + levels[i+2:]
                print (b)
                if (isSafe(b, 1)):
                    print ("corrected")
                    continue
            # try fix by removing i 
            if (again == 0):
                b = levels[:i] + levels[i+1:]
                print (b)
                if (isSafe(b, 1)):
                    print ("corrected")
                    continue
            flag = False
    return flag

if __name__ == "__main__":
    main()
