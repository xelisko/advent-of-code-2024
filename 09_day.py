
def main():

    # f = open("09_input.txt")
    f = open("09_puzzle.txt")
    line = f.readline().strip()
    IDs = []
    space = []
    id = 0    

    # read the line
    while line:
        string = line
        line = f.readline().strip()

    print (len(string), string[-1])

    # create the string disk
    disk = ""
    files = ""
    for i, char in enumerate(string):
        if (i % 2 == 0): # file
            disk += str(id) * int (char)
            files += str(id) * int (char)
            id +=1
        else: # free space
            disk += '.' * int (char)

    # print (disk)
    # print (files)
    s = 0
    n = 0
    for pos in range (len(files)):
        if (disk[pos] == '.'):
            # use digit from the end
            s += int(files[-(1+n)]) * pos
            n += 1
        else:
            s += int(disk[pos]) * pos 
    print ("s = ", s)

    n_free_space = disk.count('.')

    disk = old_long_version(disk)
    
    # check sum
    sum = 0
    for pos, char in enumerate (disk): #(disk[:len(disk)-n_free_space]):
        if (char.isdigit()):
            sum += pos * int(char)
            # print (i, char, sum)

    print ("check sum = ", sum, s)

    return 0

def old_long_version(disk):

    #calculate the moves
    n_free_space = disk.count('.')
    
    for n in range (n_free_space):
        x = disk.find('.')
        last_digit = disk[-(n+1)]
        
        # if free space - skip
        if (last_digit == '.'):
            continue

        disk = disk[:x] + last_digit + disk[x+1:-(n+1)] + '.' * (n+1)
        x = disk.find('.', x+1)
        # print (x, '\t', disk)
    return disk

if __name__ == "__main__":
    main()