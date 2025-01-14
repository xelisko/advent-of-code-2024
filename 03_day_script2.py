import re

def main ():
    sum = 0 
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
            args = line[index : next_index]
            print (args)

            # check for validity
            valid = correctFormat(args)

            if (not valid):
                index = next_index
                prev_args = prev_args + args
                continue   

            product = extractNumbersandMultiply(args)
            
            # search de/activation
            if (first_time):
                first_time = False
                activate = True
                prev_args = prev_args.strip() + line[:index]
            
            print ("prev args", prev_args)
            activate = activation(prev_args, activate)
            print ("activation - ", activate)

            if (activate):
                sum += product
                print ("sum = ", sum)

            prev_args = args
            if (next_index == -1):
                prev_args = line[index+3:]
            index = next_index
            print ("")

        # print("last mul of line to the end: ", index, next_index, prev_args)        
        line = file.readline()#.strip()
    
    print ("final sum = ", sum)
    file.close()
    return 0

def activation(args, active_prev):
    # reverse the string 
    active = True
    dont_index = args.rfind("don't()")
    do_index = args.rfind("do()")
    # print (dont_index, do_index)
    if (dont_index > do_index):
        active = False
    elif (dont_index < do_index):
        active = True
    else:
        active = active_prev
    return active

def correctFormat(args):

    format = r"^ mul \( \d{1,3} , \d{1,3} \) $" 
    return bool(re.match(args, format))

def extractNumbersandMultiply(tokens):
    sum = 0
    for token in tokens:
        comma = token.find(',')
        a = token[1:comma]
        closingBracket = token.find(')')
        b = token[comma+1:closingBracket]

    # for token in tokens:
    #     if len(token) == 0:
    #         continue
        # only digits
        if (a.isdigit() == False or b.isdigit() == False):
            # print ("A or B is not a valif INTEGER")
            continue
        # test the integer validity
        try:
            a = int(a)
            b = int(b)
        except ValueError:
           continue
        
        if ((a < 1000) and (b <1000)):
            # print ("OK", a, b, a*b)
            sum += a*b
    return sum
        

if __name__ == "__main__":
    main()