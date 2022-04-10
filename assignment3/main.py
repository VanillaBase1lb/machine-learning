#!/usr/bin/python3

import csv
import numpy
import pandas

input_file = open("input.csv", "r")
csv_file = csv.reader(input_file)

csv_header = []
csv_header = next(csv_file)

data = []
for row in csv_file:
    data.append(row[1:])

data = [[int(element) for element in column] for column in data]
# print(data)

normalization_upper_bound = [max([element[0] for element in data]), max([element[1] for element in data])]
normalization_lower_bound = [min([element[0] for element in data]), min([element[1] for element in data])]
# uncomment the below 2 lines and comment the above 2 lines to hard-code normalization upper and lower bounds
# normalization_upper_bound = [10, 30]
# normalization_lower_bound = [-10, -30]

normalized_data = []

for i in range(len(data)):
    normalized_data.append((data[i]))
    for j in range(len(data[i])):
        normalized_data[i][j] = (2 * data[i][j] - (normalization_upper_bound[j] + normalization_lower_bound[j])) / (normalization_upper_bound[j] - normalization_lower_bound[j])

fam = [[1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 3],
    [1, 1, 1, 1, 2, 3, 5],
    [1, 1, 1, 2, 2, 4, 6],
    [1, 1, 2, 3, 4, 6, 8],
    [1, 2, 3, 5, 6, 8, 9]]

def degreeOfBelonging(normalized_input):
    boundaries = [-0.66, -0.33, 0, 0.15, 0.33, 0.45, 0.75]
    degree = [0 for i in range(len(boundaries))]
    if normalized_input < boundaries[0]:
        degree[0] = 1
    elif normalized_input > boundaries[-1]:
        degree[-1] = 1
    else:
        for i in range(len(boundaries) - 1):
            if normalized_input >= boundaries[i] and normalized_input < boundaries[i + 1]:
                degree[i + 1] = (normalized_input - boundaries[i]) / (boundaries[i+1] - boundaries[i])
                degree[i] = (boundaries[i + 1] - normalized_input) / (boundaries[i+1] - boundaries[i])
                break
    return degree

fuzzified_input1 = [degreeOfBelonging(element[0]) for element in normalized_data]
fuzzified_input2 = [degreeOfBelonging(element[1]) for element in normalized_data]

def returnNewFAM(fam):
    finalFam = []
    for sections in fam:
        section = []
        for subsets in sections:
            if (subsets == 1):
                section.append(-0.75)
            elif (subsets == 2):
                section.append(0)
            elif (subsets == 3):
                section.append(0.2)
            elif (subsets == 4):
                section.append(0.4)
            elif (subsets == 5):
                section.append(0.5)
            elif (subsets == 6):
                section.append(0.6)
            elif (subsets == 7):
                section.append(0.7)
            elif (subsets == 8):
                section.append(0.8)
            elif (subsets == 9):
                section.append(0.95)
        finalFam.append(section)
    return finalFam

new_fam = returnNewFAM(fam)

def defuzzify(dob1, dob2, fam):
    dob1t = numpy.array(dob1)
    dob2t = numpy.array(dob2)
    dob1t = dob1t.reshape(-1, 1)
    dob2t = dob2t.reshape(1, -1)
    den = 0
    num = 0
    intensityweights = dob1t @ dob2t
    for i in range(len(intensityweights)):
        for j in range(len(intensityweights[0])):
            num = num + intensityweights[i][j] * fam[i][j]
            den = den + intensityweights[i][j]
            
    z = num / den
    return z

result = []
for i in range(len(data)):
    result.append(round(50 * (1 + defuzzify(fuzzified_input1[i], fuzzified_input2[i], new_fam)), 3))

input_file.close()
input_file = open("input.csv", "r")
output_file = open("output.csv", "w+")
output_file.write(input_file.read())
input_file.close()
output_file.close()

output_file_pd = pandas.read_csv("output.csv")
output_file_pd["Breakoutability"] = result
output_file_pd.to_csv("output.csv", index=False)

print(output_file_pd)