import time


def addCountToDict(dict, value, count):
    if (value in dict.keys()):
        dict[value] += count
    else:
       dict[value] = count
    return dict

def blink(stonesDict):
    newDict = {} #dict(stonesDict)
    for stone_num, count in stonesDict.items():
        
        if (stone_num == '0'):
            newDict = addCountToDict(newDict, '1', count)

        elif (len(stone_num)%2==0):
            a = stone_num[:len(stone_num)//2]
            b = stone_num[len(stone_num)//2:]
            # remove leading zeros
            while a[0] == '0' and len(a)>1:
                a = a[1:]
            while b[0] == '0' and len(b)>1:
                b = b[1:]
            # add the count
            newDict = addCountToDict(newDict, a, count)
            newDict = addCountToDict(newDict, b, count)
        else:
            newDict = addCountToDict(newDict, str(int(stone_num) * 2024), count)
        # print (newDict)
    return newDict

def main():
 
    # f = open("11_input.txt")
    f = open("11_puzzle.txt")
    stones = f.readline().strip().split(' ')
    
    # create a dict to count the number of occurence
    stonesDict = {index: 1 for index in (stones)}
    
    for i in range (75):
        stonesDict = blink(stonesDict)
        # print (stonesDict.items())

    sum = 0
    for value in stonesDict.values():
        sum += value
    print (sum)

    return 0

if __name__ == "__main__":
    start = time.time()
    main() 
    end = time.time()
    print ("time = ", end - start)