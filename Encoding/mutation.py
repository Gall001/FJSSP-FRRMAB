#test
import random
def swapMutation(CrossoverList):
    for i in range(len(CrossoverList)):
        memoryA = random.randint(1, len(CrossoverList[i])-1)
        memoryB = random.randint(1, len(CrossoverList[i])-1)

        mutationA = list(CrossoverList[i][memoryA])
        mutationB = list(CrossoverList[i][memoryB])

        mutationA[1] = list(CrossoverList[i][memoryB])[1]
        mutationB[1] = list(CrossoverList[i][memoryA])[1]

        CrossoverList[i][memoryA],CrossoverList[i][memoryB] = mutationB,mutationA
    return CrossoverList

def insertMutation(CrossoverList):
    for i in range(len(CrossoverList)):

        memoryA = random.randint(1, len(CrossoverList[i])-1)
        memoryB = random.randint(1, len(CrossoverList[i])-1)

        if memoryA > memoryB:
            switcher = list(CrossoverList[i][memoryA-1])
            switcher[1] = memoryB+1

            CrossoverList[i].insert(memoryB,switcher)
            CrossoverList[i].pop(CrossoverList[i][memoryA][1])

            for x in range(memoryB+1, memoryA):
                newValue =list(CrossoverList[i][x])
                newValue[1] = newValue[1]+1
                CrossoverList[i][x] = newValue

        elif memoryB > memoryA:
            switcher = list(CrossoverList[i][memoryB-1])
            switcher[1] = memoryA+1

            CrossoverList[i].insert(memoryA,switcher)
            CrossoverList[i].pop(CrossoverList[i][memoryB][1])

            for x in range(memoryA+1, memoryB):
                newValue =list(CrossoverList[i][x])
                newValue[1] = newValue[1]+1
                CrossoverList[i][x] = newValue

def inverseMutation(CrossoverList):
    for i in range(len(CrossoverList)):

        mutationSizeA = random.randint(1, len(CrossoverList[i])-1)
        mutationSizeB = random.randint(1, len(CrossoverList[i])-1)
        
        if(mutationSizeA > mutationSizeB):
            size = mutationSizeA + mutationSizeB
            for leftSide in range(mutationSizeB, (size + 1) // 2):
                rightSide = size - leftSide

                newLeftSide = list(CrossoverList[i][rightSide])
                newRightSide = list(CrossoverList[i][leftSide])

                newLeftSide[1] = CrossoverList[i][leftSide][1]
                newRightSide[1] = CrossoverList[i][rightSide][1]

                CrossoverList[i][leftSide], CrossoverList[i][rightSide] = newLeftSide, newRightSide
        elif(mutationSizeB > mutationSizeA):
            size = mutationSizeB + mutationSizeA
            for leftSide in range(mutationSizeA, (size + 1) // 2):
                rightSide = size - leftSide

                newLeftSide = list(CrossoverList[i][rightSide])
                newRightSide = list(CrossoverList[i][leftSide])

                newLeftSide[1] = CrossoverList[i][leftSide][1]
                newRightSide[1] = CrossoverList[i][rightSide][1]

                CrossoverList[i][leftSide], CrossoverList[i][rightSide] = newLeftSide, newRightSide
    return CrossoverList


#insertMutation([[(5, 1), (2, 2), (1, 3), (3, 4), (4, 5), (3, 6), (3, 7), (4, 8), (1, 9), (4, 10), (3, 11), (1, 12)], [(5, 1), (2, 2), (3, 3), (5, 4), (1, 5), (5, 6), (4, 7), (2, 8), (3, 9), (4, 10), (5, 11), (3, 12)]])