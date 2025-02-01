import numpy as np
import time

def main():
    start = time.time()

    f = open("07_puzzle.txt", "r")
    line = f.readline().strip()
    sum = 0

    while line:
        # read and process the line
        values = line.split(' ')
        result = int(values[0][:-1])
        values = list(map(int, values[1:]))

        # get all the combinations of operators
        operators = np.array(generateRecursive('', len(values)-1))
        operators = operators.reshape((-1))

        # calculate all the values
        all_results = []
        for comb in operators: # pick a combination
            intrmdt = values[0] # set the first values

            for i,opr in enumerate(comb): # for each operator in the list
                if (opr == '+'):
                    intrmdt += values[i+1]
                elif (opr == '*'):
                    intrmdt *= values[i+1]
                elif (opr == "|"):
                    intrmdt = int(str(intrmdt)+str(values[i+1]))
                # print(opr, intrmdt)
            # print (comb)

            all_results.append(intrmdt)

        if (result in all_results):
            sum += result 
        
        line = f.readline().strip()
        
    print ("sum of the correct equations = ", sum)
    end = time.time()
    print ("processing time = ", end - start)
    return 0

def generateRecursive(curr_str, n):
    if (len(curr_str)==n):
        return str(curr_str)
    
    # recursive call
    combinations = []
    combinations.append(generateRecursive(curr_str+'*', n))
    combinations.append(generateRecursive(curr_str+'+', n))
    combinations.append(generateRecursive(curr_str+'|', n))

    return combinations

if __name__ == "__main__":
    main()
    # a = generateRecursive('', 5)
    # b = np.array(a)
    # b = b.reshape((-1))
    # print (b)