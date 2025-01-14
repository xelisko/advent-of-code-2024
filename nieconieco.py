from re import findall

total1 = total2 = 0
enabled = True
data = open('input2.txt').read()

for a, b, do, dont in findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", data):
    if do or dont:
        enabled = bool(do)
    else:
        x = int(a) * int(b)
        total1 += x
        total2 += x * enabled

print(total1, total2)