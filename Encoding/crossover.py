import random

def twoPoint(CrossoverList,SolutionList,SolutionNum):
    s1 = SolutionList[random.randint(0, int(float(SolutionNum))-1)][0]
    s2 = SolutionList[random.randint(0, int(float(SolutionNum))-1)][0]

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

def OX(CrossoverList,SolutionList,SolutionNum):
    s1 = SolutionList[random.randint(0, int(float(SolutionNum))-1)][0]
    s2 = SolutionList[random.randint(0, int(float(SolutionNum))-1)][0]

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
