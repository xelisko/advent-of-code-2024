def main ():

    # define lists
    sum = 0 

    # read the text file
    file = open('input2.txt', 'r')

    line = file.readline()#.strip()
    while line:
        print (line)
        # take arguments of every 'mul'
        line.find(r

        # tokens = line.split('mul', 'don't()', 'do()')
        print (tokens)

        # filter out the ones that do not start with '('
        tokens = noFirstBracket(tokens)
        print(tokens)
 
        # try to extract A and B
        sum += extractNumbersandMultiply(tokens)
        print ("sum = ", sum)

        line = file.readline()#.strip()
    
    file.close()
    return 0

def noFirstBracket(tokens):
    output = []
    for token in tokens:
        if len(token) == 0:
            continue
        if ((token[0] is '(') and ( ',' in token) and (')' in token)):
            output.append(token)
    return output

def extractNumbersandMultiply(tokens):
    sum = 0
    for token in tokens:
        print (token)
        comma = token.find(',')
        a = token[1:comma]
        # print ("A = ", a)
        closingBracket = token.find(')')
        b = token[comma+1:closingBracket]
        # print ("B = ", b)

        # only digits
        if (a.isdigit() == False or b.isdigit() == False):
            # print ("A or B is not a valif INTEGER")
            continue
        # test the integer validity
        try:
            a = int(a)
            b = int(b)
        except ValueError:
        #    print ("A or B not an int") 
           continue
        
        if ((a < 1000) and (b <1000)):
            print ("OK", a, b, a*b)
            sum += a*b
    return sum
        

if __name__ == "__main__":
    main()