#test
import random
def simpleMutation(CrossoverList, jobs_list):
    for i in range(len(CrossoverList)):
        for x in range(len(jobs_list)):
            for y in jobs_list[x]:
                operatioNum = len(jobs_list[x][y])  
        tempList = list(CrossoverList[i][random.randint(0, len(CrossoverList[i])-1)])
        tempList[0] = random.randint(1, operatioNum)
        CrossoverList[i][tempList[1]-1] = tempList
    return CrossoverList