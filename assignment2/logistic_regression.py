#!/usr/bin/python3

import openpyxl

filename = "data.xlsx"
sheetname = "Sheet2"
test_data = []
train_data = []
train_test_ratio = 5

data_workbook = openpyxl.load_workbook(filename)
data_sheet = data_workbook[sheetname]
cell_range = data_sheet["A2": "D1332"]
for i in range(len(cell_range)):
    x1 = cell_range[i][0].value
    x2 = cell_range[i][1].value
    x3 = cell_range[i][2].value
    y = cell_range[i][3].value
    if i % train_test_ratio == 0:
        test_data.append([x1, x2, x3, y])
    else:
        train_data.append([x1, x2, x3, y])

print(test_data)