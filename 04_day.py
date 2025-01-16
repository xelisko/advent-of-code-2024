

def main ():
    # define variables
    word_grid = []
    xmas = "XMAS"

    # read input
    file = open("input2.txt","r")
    line = file.readline().strip()

    while line:
        word_grid.append(line)
        line = file.readline().strip()

    # search horizontally
    count = 0
    for line in word_grid:
        count += searchForPhrase(line, xmas)
    
    print ("horizontal count = ", count)

    # search vertically
    for i in range (len(word_grid)):
        column = ''.join([s[i] for s in word_grid if s])
        count += searchForPhrase(column, xmas)

    print ("after vertical count = ", count)

    # diagonal 
    lenght = len(word_grid[0])
    a = 0
    b = 0

    for i in range (len(word_grid[0])-3):
        diagonal = ''.join(word_grid[x][i+x] for x in range(lenght-i))
        a += searchForPhrase(diagonal, xmas)
        print (diagonal, a)

        if (i !=0):
            word_opposite = ''.join(word_grid[i+x][x] for x in range(lenght-i))
            a += searchForPhrase(word_opposite, xmas)
            print(word_opposite, a)

        flipped_diagonal = ''.join(word_grid[x][lenght-i-1-x] for x in range(lenght-i))
        b += searchForPhrase(flipped_diagonal, xmas)
        # print(flipped_diagonal, b)

        if (i !=0): 
            flipped_diagonal2 = ''.join(word_grid[lenght-1-x][x+i] for x in range(lenght-i))
            b += searchForPhrase(flipped_diagonal2, xmas)
            # print(flipped_diagonal2, b)
    count = count+ b+ a

    print ("after diagonal count = ", count)

    return 0

def searchForPhrase(word, xmas):
    count = 0
    
    a = word.find(xmas)
    while (a != -1): 
        count +=1
        a = word.find(xmas, a+1)

    a = word.find(xmas[::-1])
    while (a != -1): 
        count +=1
        a = word.find(xmas, a+1)

    return count

if __name__ == "__main__":
    main()