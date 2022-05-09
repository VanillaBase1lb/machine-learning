import pydot
import numpy as np
import random
import statistics
from cProfile import label
import csv
import math
from turtle import fillcolor

# file = open('data_banknote_authentication.txt')
file = open('Sensorless_drive_diagnosis.txt')
# type(file)
# csvfile = csv.reader(file)
# Uncomment the line below to use SDD dataset
csvfile = csv.reader(file, delimiter=" ")

graph = pydot.Dot(graph_type='digraph')

rows = []
test_data = []
t1 = 0
size = 1
for row in csvfile:
    t1 += 1
    if t1%200 == 0:
        test_data.append(row)
    else:
        rows.append(row)

for x in range(len(rows)):
    for y in range(len(rows[0])):
        rows[x][y]=float(rows[x][y])

for x in range(len(test_data)):
    for y in range(len(test_data[0])):
        test_data[x][y]=float(test_data[x][y])

classes = []
class_index = len(rows[0])-1
features = []
for x in range(len(rows[0])-1):
    features.append(x)
for x in range(len(rows)):
    if rows[x][class_index] not in classes:
        classes.append(rows[x][class_index])

def testSplit(rows, f_index, value):
    left = []
    right = []
    for x in range(len(rows)):
        if rows[x][f_index] > value:
            right.append(rows[x])
        elif rows[x][f_index] <= value:
            left.append(rows[x])
    return left, right

def classP(grp, cls):
    class_count = 0
    for x in range(len(grp)):
        if grp[x][class_index] == cls:
            class_count += 1
    if len(grp) != 0:
        p = class_count/len(grp)
    else:
        p = 0
    return p

def splitEntropy(groups, classes, rows):
    entropy = 0
    for grp in groups:
        grp_probability = len(grp)/len(rows)
        grp_sum = 0
        for cls in classes:
            if classP(grp, cls) != 0:
                grp_sum -= classP(grp, cls)*(math.log2(classP(grp, cls)))
            else:
                grp_sum = 0
        entropy += grp_probability*grp_sum
    return entropy

def bestSplit(rows):
    min_entropy = 999999
    for f_index in features:
        for x in range(0, len(rows), 100):
            groups = testSplit(rows, f_index, rows[x][f_index])
            entropy = splitEntropy(groups, classes, rows)
            if entropy < min_entropy:
                min_entropy = entropy
                best_f_index = f_index
                best_value = rows[x][f_index]
                best_groups = groups
    # print(best_value)
    # print(best_f_index)
    return best_groups, best_value, best_f_index

def sameClass(grp):
    current_class = grp[0][class_index]
    for x in range(len(grp)):
        if grp[x][class_index] != current_class:
            return False
    # print(current_class)
    return True

def groupSize(grp):
    if len(grp) < 500:
        return True
    else:
        return False

def majorityClass(grp):
    max_count = 0
    for x in classes:
        count = 0
        for y in range(len(grp)):
            if grp[y][class_index] == x:
                count+=1
        if count > max_count:
            max_count = count
            max_cls = x
    return max_cls

t2 = 1
def createDT(groups):
    global t2
    nodes = bestSplit(groups)
    for grp in nodes[0]:
        if sameClass(grp) is True:
            tn = pydot.Node(t2, label=str(grp[0][class_index]), style="filled", fillcolor="blue")
            graph.add_node(tn)
            t2 += 1
            graph.add_edge(pydot.Edge(str(str(nodes[1])+", "+ str(nodes[2])), tn))
            # print('terminal node')
            continue
        elif groupSize(grp) is True:
            val = majorityClass(grp)
            tn = pydot.Node(t2, label=str(val), style="filled", fillcolor="blue")
            graph.add_node(tn)
            t2 += 1
            graph.add_edge(pydot.Edge(str(str(nodes[1])+", "+ str(nodes[2])), tn))
            # print('terminal node')
            continue
        else:
            child = bestSplit(grp)
            graph.add_edge(pydot.Edge(str(str(nodes[1])+", "+ str(nodes[2])), str(str(child[1])+", "+ str(child[2]))))
            createDT(grp)

createDT(rows)
graph.write_png("output_dt.png")
result = []

def treeCheck(groups, test):
    c = 0
    nodes = bestSplit(groups)
    for grp in nodes[0]:
        if c == 0:
            if test[nodes[2]] < nodes[1]:
                if sameClass(grp) is True:
                    result.append(grp[0][class_index])
                    return
                elif groupSize(grp) is True:
                    val = majorityClass(grp)
                    result.append(val)
                    return
                else:
                    treeCheck(grp, test)
        elif c == 1:
            if test[nodes[2]] > nodes[1]:
                if sameClass(grp) is True:
                    result.append(grp[0][class_index])
                    return
                elif groupSize(grp) is True:
                    val = majorityClass(grp)
                    result.append(val)
                    return
                else:
                    treeCheck(grp, test)
        c += 1

def accuracyCheck(rows, test_data):
    global result
    result = []
    count = 0
    for test in test_data:
        treeCheck(rows, test)
    for y in range(len(test_data)):
        if result[y] != test_data[y][class_index]:
            count += 1
    acc = ((len(test_data)-count)/len(test_data))*100
    return acc, result

# print(accuracyCheck(rows, test_data))

def bagTree(rows, test_data):
    k = [2, 2, 4]
    total = []
    for x in k:
        random.shuffle(rows)
        arrs = np.array_split(rows, x)
        for arr in arrs:
            data = accuracyCheck(arr, test_data)
            print(data[0])
            total.append(data[1])

    final_result = []
    for y in range(len(test_data)):
        temp = []
        for x in range(len(total)):
            temp.append(total[x][y])
        final_result.append(statistics.mode(temp))

    error = 0
    for x in range(len(test_data)):
        if final_result[x] != test_data[x][class_index]:
            error += 1
    bag_acc = ((len(test_data)-error)/len(test_data))*100
    return bag_acc

# Uncomment the line below to enable bagging
# print(bagTree(rows, test_data))