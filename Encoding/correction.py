min = 5
max = 10
list = [(3, 7), (1, 8), (3, 9), (4, 10), (5, 11), (1, 12), (1, 1), (1, 2), (1, 3), (2, 4), (5, 5), (5, 6)]


def correction(min, max, list):
    atual = min
    for key in list:
        print(key[1])
        if key[1] >= atual and key[1] <= max and key[1] != atual:
            list.sort(key=lambda tup: tup[1])
            print('order needed: ', list)
            return list
        elif key[1] == atual and atual<max:
            atual = atual+1
    print('order not needed: ', list)
    return list

correction(min,max,list)

