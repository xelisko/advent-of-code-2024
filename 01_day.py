import math
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

# sort the list
list1.sort()
list2.sort()

# calculate the distance
for i in range (len(list1)):
    d = np.abs(list1[i] - list2[i])
    # print (i, list1[i], list2[i], d)
    distances.append(d)

# print the total distance
print ("Total distance = ", sum(distances))

# part B - Similarity Score
for i in range (len(list1)):
    x = list1[i]
    n_appear = list2.count(x)
    score = x * n_appear
    # print (i, score)
    similarity_score.append(score)

print ("Similarity Score = ", sum(similarity_score))