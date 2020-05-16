import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# cal distance between two points
def get_distance(point_a,point_b):
    """

    :param point_a: point a
    :param point_b: point b
    :return: euclidean distance
    """
    point_a_arr = np.array(point_a)
    point_b_arr = np.array(point_b)
    dis = float(np.sqrt(np.sum(np.square(point_a_arr-point_b_arr))))
    return dis

# first random select points
def init_center(data_list,n,k):
    """

    :param data_list: database
    :param n: n rows
    :param k: k classes
    :return: k points
    """
    center_points = []
    index = []
    for i in range(k):
        index.append(random.randint(0,n-1))
    for j in index:
        center_points.append(data_list[j])
    return center_points

# determine the end of condition of iteration
def get_mean_value(data_cluster,k):
    """

    :param data_cluster: data cluster
    :param k: k classes
    :return: mean var value
    """
    mean_var_value = 0.0
    for i in range(k):
        center_point = np.mean(np.array(data_cluster[i]),axis=0).tolist()
        dis = []
        for j in range(len(data_cluster[i])):
            dis.append(get_distance(data_cluster[i][j],center_point))
        dis_arr = np.array(dis)
        mean_var_value += np.var(dis_arr)
    return mean_var_value/k

# package function to use
def get_multi_dim_list(k,first_item_list):
    """

    :param k: k classes
    :param first_item_list: first select points
    :return: first cluster center points
    """
    list_return = []
    for i in range(k):
        list_return.append([])
    for i in range(k):
        list_return[i].append(first_item_list[i])
    return list_return

# package function to use
def get_multi_empty_list(k):
    """

    :param k: k classes
    :return: k-dim list
    """
    list_return = []
    for i in range(k):
        list_return.append([])
    return list_return

# package function to iteration the cluster
def cluster_list(data_cluster,n,k,data_cluster_points):
    """

    :param data_cluster: last data cluster
    :param n: n rows
    :param k: k classes
    :param data_cluster_points: selected center points
    :return: new data cluster
    """
    for i in range(n):
        dist_list = []
        for i_compare in range(k):
            dis = get_distance(data_list[i], data_cluster_points[i_compare])
            dist_list.append(dis)
        index = dist_list.index(min(dist_list))
        data_cluster[index].append(data_list[i])
    return data_cluster

# k_means main function
def k_means(data_list,n,k,dist=get_distance,init_centers=init_center,get_cluster=get_multi_dim_list):
    """

    :param data_list: initial data base
    :param n: n rows
    :param k: k classes
    :param dist: euclidean distance
    :param init_centers: initial selected points
    :param get_cluster: package function
    :return: final data cluster
    """
    data_cluster_points = []
    init_points = init_centers(data_list,n,k)
    for i in range(k):
        # data_cluster[i].append(init_points[i])
        data_cluster_points.append(init_points[i])
    data_cluster = get_multi_empty_list(k)

    flag = True
    mean_var_values  = []
    while flag:
        data_cluster = cluster_list(data_cluster,n,k,data_cluster_points)

        last_mean_var_value = get_mean_value(data_cluster, k)

        if len(mean_var_values) >1 and last_mean_var_value == mean_var_values[-1]:
            flag = False

        if len(mean_var_values) == 0 or last_mean_var_value != mean_var_values[-1]:
            mean_var_values.append(last_mean_var_value)

            new_center_tmp = []
            for i in range(k):
                new_center_tmp.append(np.mean(np.array(data_cluster[i]),axis=0).tolist())

            data_cluster_points = new_center_tmp
            data_cluster = get_multi_empty_list(k)

    return data_cluster,mean_var_values


if __name__ == '__main__':
    # read files
    with open('data.txt') as f:
        n = int(f.readline())
        data_list = []
        data = f.readlines()
        for line in data:
            line = list(map(float,line.strip().split(' ')))
            data_list.append(line)

    k = int(input('seperate k classes:\n'))
    data_cluster, mean_var_values = k_means(data_list,n,k)
    print(data_cluster)
    print(mean_var_values)

    # show in 3-dim coordinate system
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(list(np.array(data_cluster[0])[:,0]),list(np.array(data_cluster[0])[:,1]),list(np.array(data_cluster[0])[:,2]), c='r', marker='o')
    ax.scatter(list(np.array(data_cluster[1])[:,0]),list(np.array(data_cluster[1])[:,1]),list(np.array(data_cluster[1])[:,2]), c='b', marker='*')
    ax.scatter(list(np.array(data_cluster[2])[:,0]),list(np.array(data_cluster[2])[:,1]),list(np.array(data_cluster[2])[:,2]), c='g', marker='+')
    plt.show()
    