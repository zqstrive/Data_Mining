import numpy as np
import math

# binning
def binning(data_list, row, col):
    data = [data_list[-1] for _ in range(row * col - len(data_list))]
    array = np.hstack((data_list, data))
    binning = np.reshape(array, (row, col))
    return binning

# mean binning
def mean_binning(data_array, row, col):
    for i in range(row):
        mean_value = int(np.mean(data_array[i]))
        for j in range(col):
            data_array[i, j] = mean_value
    return data_array

# median binning
def median_binning(data_array, row, col):
    for i in range(row):
        median_value = int(np.median(data_array[i]))
        for j in range(col):
            data_array[i, j] = median_value
    return data_array

# border binning
def border_binning(data_array, row, col):
    for i in range(row):
        for j in range(1, col - 1):
            if (data_array[i, j] - data_array[i, 0]) ** 2 < (data_array[i, j] - data_array[i, col - 1]) ** 2:
                data_array[i, j] = data_array[i, 0]
            else:
                data_array[i, j] = data_array[i, col - 1]
    return data_array

# detect outlier
def outlier_detector(data_list):
    outlier = []
    quartile = np.percentile(data_list, (25, 50, 75))
    IQR = quartile[2] - quartile[0]
    for data in data_list:
        if data < quartile[0] - 1.5 * IQR or data > quartile[2] + 1.5 * IQR:
            outlier.append(data)
    return outlier

if __name__ == '__main__':

    # import data
    data = open('data.txt')
    data = data.readline().split(" ")
    data_list = [int(i) for i in data]
    data_list = np.array(data_list)
    print('原始数据:\n',data_list)

    # cal value
    mean_value = int(np.mean(data_list))
    median_value = int(np.median(data_list))
    max_value = np.max(data_list)
    min_value = np.min(data_list)
    mid_range = ((max_value + min_value) / 2)
    left_border = data_list[0]
    right_border = data_list[-1]

    # find outlier point
    outlier_point_arr = outlier_detector(data_list)
    for i in range(len(outlier_point_arr)):
        print('离群点为:',outlier_point_arr[i],end=' ')

    # binning
    depth = 3
    row = math.ceil(len(data_list) / depth)
    col = depth
    data_binning = binning(data_list, row, col)
    print('\n分箱后的数据:\n', data_binning)
    print("请选择分箱方式:1 均值分箱；2：中值分箱；3：边界值分箱")
    select_ = int(input())
    if select_ == 1:
        data_array = mean_binning(data_binning, row, col)
        print('平滑后的数据:\n',data_array)
    elif select_ == 2:
        data_array = median_binning(data_binning, row, col)
        print('平滑后的数据:\n',data_array)
    elif select_ == 3:
        data_array = border_binning(data_binning, row, col)
        print('平滑后的数据:\n',data_array)



