import re

def main ():
    sum = 0
    sum_part1 = 0 
    prev_args = ""
    activate = True
    first_time = True
    
    # read the text file
    file = open('input2.txt', 'r')
    line = file.readline()

    while line:
        first_time = True
        index = line.find('mul')

        while index != -1:

            # select until the next 'mul'
            next_index = line.find('mul', index + 1)
            args = line[index + 3: next_index]

            # check for validity
            valid = correctFormat(args)

            if (not valid):
                index = next_index
                prev_args = prev_args + args
                continue   
            
            # calculate the product
            product = extractNumbersandMultiply(args)
            sum_part1 += product
            
            # search de/activation
            if (first_time):
                first_time = False
                activate = True
                prev_args = prev_args.strip() + line[:index]
            
            activate = activation(prev_args, activate)
            if (activate):
                sum += product

            prev_args = args
            if (next_index == -1):
                prev_args = line[index+3:]
            index = next_index

        line = file.readline()
    
    print ("final sums = ", sum_part1, sum)
    file.close()
    return 0

def activation(args, active_prev):
    # reverse the string 
    active = True
    dont_index = args.rfind("don't()")
    do_index = args.rfind("do()")
    
    if (dont_index > do_index):
        active = False
    elif (dont_index < do_index):
        active = True
    else:
        active = active_prev
    return active

def correctFormat(args):
    # valid = True
    if len(args) == 0:
        return False
    if ((args[0] == '(') and ( ',' in args) and (')' in args)):
        return True
    return False
    

def extractNumbersandMultiply(token):
    sum = 0
    
    comma = token.find(',')
    a = token[1:comma]
    closingBracket = token.find(')')
    b = token[comma+1:closingBracket]

    # only digits
    if (a.isdigit() == False or b.isdigit() == False):
        return 0
    
    # test the integer validity
    a = int(a)
    b = int(b)
    
    if ((a < 1000) and (b <1000)):
        sum += a*b

    return sum
        

if __name__ == "__main__":
    main()