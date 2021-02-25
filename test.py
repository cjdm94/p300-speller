import numpy as np
from classifier import Classifier
import datetime

# INPUTS FOR CLASSIFIER - WHAT IS AN EPOCH

# when creating epochs, gives an averaged value accross channels for each SAMPLE in the window
# which makes sense if you imagine plotting the epoched data
# arr = np.array([[10, 5], [20, 30], [50, 40]])
# print(np.mean(arr.T, axis=0))
# [7.5, 25, 45] aka [sample1Mean, sample2Mean, sample3Mean]
# an epoch is an array containing many of these elements 
# - one element per sample in the window

# MAPPING THE ROWS/COLUMNS TO THE EPOCHS

epochs = np.array([
    [0, 1],[0, 2],[0, 3],[0, 4],[0, 5],[0, 6],
    [1, 1],[1, 2],[1, 3],[1, 4],[1, 5],[1, 6],
    [2, 1],[2, 2],[2, 3],[2, 4],[2, 5],[2, 6],
    [3, 1],[3, 2],[3, 3],[3, 4],[3, 5],[3, 6],
    [4, 1],[4, 2],[4, 3],[4, 4],[4, 5],[4, 6],
    [5, 1],[5, 2],[5, 3],[5, 4],[5, 5],[5, 6],
])
cols = epochs[[6,7,8,9,10,11,18,19,20,21,22,23,30,31,32,33,34,35]]

order = [5, 3, 2, 0, 4, 1, 3, 2, 0, 1, 5, 4, 3, 4, 0, 5, 2, 1]
num_ = 6

# now we have the epochs that represent the column flashes. 
# create a new array with 6 elements (one for each column)
# we get a new array. Each element represents a column.
# A column flashes 3 times, so each column element has 3 elements
# Let's say the first column to flash is col 5. Then the first arr element is:
# E.g. arr[0] = [col5Flash1, col5Flash2, col5Flash3]

# new_arr[5] = [cols[0]]
# new_arr[3] = [cols[1]]
# new_arr[2] = [cols[2]]
# new_arr[0] = [cols[3]]
# new_arr[4] = [cols[4]]
# new_arr[1] = [cols[5]]

# new_arr[3] = [cols[1], cols[6]]
# new_arr[2] = [cols[2], cols[7]]
# new_arr[0] = [cols[3], cols[8]]
# new_arr[1] = [cols[5], cols[9]]
# new_arr[5] = [cols[0], cols[10]]
# new_arr[4] = [cols[4], cols[11]]

# new_arr[3] = [cols[1], cols[6], cols[12]]
# new_arr[4] = [cols[4], cols[11], cols[13]]
# new_arr[0] = [cols[3], cols[8]], cols[14]]
# new_arr[5] = [cols[0], cols[10], cols[15]]
# new_arr[2] = [cols[2], cols[7], cols[16]]
# new_arr[1] = [cols[5], cols[9], cols[17]]
new_arr = [[] for i in range (0, num_)]
for i, elem in enumerate(order):
    new_arr[elem].append([cols[i]])
    
print(np.squeeze(np.array(new_arr)))
# Each element contains the 
# [
#     [
#         [0 4],[1 3],[2 3]
#     ],
#     [
#         [0 6],[1 4],[2 6]
#     ],
# ]

# clf = Classifier(datetime.datetime.now())

# arr = np.array([
#     [2, 5, 4], # sample 1, c1-c2-c3
#     [6, 15, 8], # sample 2, c1-c2-c3
#     [7, 9, 10] # sampel 3, c1-c2-c3
# ])

# print("mean of non-transposed:", np.mean(arr, axis=1))
# print("mean of transposed:", np.mean(arr.T, axis=0))

# arr = np.array([
#     ["a", "b", "c", "d", "e", "f"],
#     ["g", "h", "i", "j", "k", "l"],
#     ["m", "n", "o", "p", "q", "r"],
#     ["s", "t", "u", "v", "w", "x"],
#     ["y", "z", "_space_", "_backspace_", "_emoji_", "_speak_"],
# ])

# print(arr[29])

# clf = Classifier(datetime.datetime.now())

# arr = np.array([
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
#     [5.65521697, 5.01060437, 4.52770744, 10.3939686, 15.42979151, 22.98273716],
# ])

# arr = arr[[0,1,2]] # this indexing prints out the rows at index 0-2
# print(arr)

# TEST ARRAY STACKING
# t_ep = np.array([["c1_target", "c2_target"], ["c1_target", "c2_target"]])
# n_ep = np.array([["c1_non", "c2_non"], ["c1_non", "c2_non"]])

# t_ep = np.hstack((t_ep, np.ones([t_ep.shape[0],1])))

# [['c1_target' 'c2_target' '1.0']
#  ['c1_target' 'c2_target' '1.0']]
# print(t_ep)
# print()

# n_ep = np.hstack((n_ep, np.zeros([n_ep.shape[0],1])))

# [['c1_non' 'c2_non' '0.0']
#  ['c1_non' 'c2_non' '0.0']]
# print(n_ep)
# print()

# X = np.vstack((t_ep, n_ep))[:,:-1]
# Y = np.vstack((t_ep, n_ep))[:,-1]

# [['c1_target' 'c2_target']
#  ['c1_target' 'c2_target']
#  ['c1_non' 'c2_non']
#  ['c1_non' 'c2_non']]
# print(X)
# print()

# ['1.0' '1.0' '0.0' '0.0']
# print(Y)