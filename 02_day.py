import numpy as np

# define lists
list1 = []
list2 = []
distances = []
similarity_score = []

# read the text file
file = open('input01.txt', 'r')
line = file.readline().strip()
while line:
    a, b = line.split('   ')
    list1.append(int(a))
    list2.append(int(b))
    line = file.readline().strip()

file.close()