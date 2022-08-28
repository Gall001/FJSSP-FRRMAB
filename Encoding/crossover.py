import random

def twoPoint(CrossoverList,s1,s2):

    firstThird = int(round(len(s1)/3))
    secondThird = int(round(len(s1)/3) * 2)

    s1t1 = s1[:firstThird]
    s1t2 = s1[firstThird:secondThird]
    s1t3 = s1[secondThird:]

    s2t1 = s2[:firstThird]
    s2t2 = s2[firstThird:secondThird]
    s2t3 = s2[secondThird:]

    s1 = s1t1+s2t2+s1t3
    s2 = s2t1+s1t2+s2t3

    CrossoverList.append(s1)
    CrossoverList.append(s2)

    return CrossoverList

def OX(CrossoverList,s1,s2):

    core = []
    core.append(random.randint(1, len(s1)-1))
    core.append(random.randint(1, len(s1)-1))
    core.sort()

    newS2 = []
    for key in s2:
        if key[1] < core[0] or key[1] > core[1]:
            newS2.append(key)

    newSolution = []
    counter = 1
    newS2counter = 0

    for key in s2:

        if counter < core[0] or counter > core[1]:
            newSolution.append(newS2[newS2counter])
            newS2counter = newS2counter + 1
        else:
            newSolution.append(s1[counter-1])

        counter = counter + 1

    CrossoverList.append(newSolution)
    return CrossoverList

def PMX(CrossoverList,s1,s2):
    core = []
    core.append(random.randint(1, len(s1)-1))
    core.append(random.randint(1, len(s1)-1))
    core.sort()

    size = min(len(s1), len(s2))
    p1, p2 = [0] * size, [0] * size

    for i in range(size-1):
        print('s1[i][1]: ',s1[i][1])
        p1[s1[i][1]] = i
        p2[s2[i][1]] = i

    for i in range(core[0], core[1]):
        temp1 = s1[i]
        temp2 = s2[i]

        s1[i], s1[p1[temp2[1]]] = temp2, temp1
        s2[i], s2[p2[temp1[1]]] = temp1, temp2

        p1[temp1[1]], p1[temp2[1]] = p1[temp2[1]], p1[temp1[1]]
        p2[temp1[1]], p2[temp2[1]] = p2[temp2[1]], p2[temp1[1]]
    CrossoverList.append(s1)
    CrossoverList.append(s2)

    return CrossoverList