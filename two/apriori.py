# count
def get_count(database, items):
    """

    :param database: data base
    :param items: C_i items
    :return: C_i items corresponding counts
    """
    counts = []
    for item in items:
        c = 0
        for i in database:
            include = True
            for k in item:
                if k not in i:
                    include = False
            if include:
                c += 1
        counts.append(c)
    return counts

# cut
def get_cut_items(items, counts, min_sup, length):
    """

    :param items: C_i items
    :param counts: C_i items corresponding counts
    :param min_sup: min support count
    :param length: total items
    :return: fre items
    """
    items_return = []
    # append
    for i, key in enumerate(items):
        if float(counts[i]) / length >= min_sup:
            items_return.append(items[i])
    return items_return

# join
def aproiri_gen(fre_items):
    """

    :param fre_items: fre items
    :return: C_i+1 items
    """
    single = fre_items[0]
    items_return = []
    if len(single) <=1:
        for i in range(len(fre_items)):
            for j in range(i+1,len(fre_items)):
                tmp = fre_items[i].copy()
                tmp.extend(fre_items[j])
                items_return.append(tmp)
        return items_return
    else:
        for i in range(len(fre_items)):
            for j in range(1,len(fre_items)):
                if set(fre_items[i]).isdisjoint(set(fre_items[j])):
                    pass
                else:
                    tmp = list(set(fre_items[i])|set(fre_items[j]))
                    tmp.sort()
                    if len(tmp) > len(single) and tmp not in items_return:
                        items_return.append(tmp)
        return items_return

# apriori main function
def apriori(database, min_sup):

    """

    :param database: data base
    :param min_sup: min support count
    :return: fre items
    """
    C_1 = {}
    for items in database:
        for item in items:
            if item in C_1:
                C_1[item] += 1
            else:
                C_1[item] = 1
    print ('C_1:', C_1)
    one_items = C_1.keys()
    items = []
    for i in one_items:
        items.append([i])
    n = len(database)
    cut_items = []
    for k in items[:]:
        if C_1[k[0]]*1.0/n >= min_sup:
            cut_items.append(k)
    cut_items.sort()
    fre_items = cut_items
    all_items = []
    while fre_items != []:
        counts = get_count(database, fre_items)
        cut_items = get_cut_items(fre_items, counts, min_sup, len(database))
        for item in cut_items:
            all_items.append(item)
        fre_items = aproiri_gen(cut_items)
    return all_items



if __name__ == '__main__':
    # read file
    with open('data.txt') as f:
        next(f)
        data = []
        while True:
            line = f.readline()
            if not line:
                break
            line = list(line.strip().split(' '))
            print(line)
            x = line[1].split(',')
            x = tuple(x)
            data.append(x)
        print(data)
        items_return = apriori(data, 0.4)
        print('\nfrequent items set:\n', items_return)
        items_1 = []
        items_2 = []
        items_3 = []
        for i in range(len(items_return)):
            if len(items_return[i]) == 1:
                items_1.append(items_return[i])
            elif len(items_return[i]) == 2:
                items_2.append(items_return[i])
            elif len(items_return[i]) == 3:
                items_3.append(items_return[i])
        print('频繁1项集:',items_1)
        print('频繁2项集:',items_2)
        print('频繁3项集:',items_3)






