# FJSSP Datasets Reader to Dictionaries
# Lupercio F Luppi 2022
import random
import re                           # Regular Expressions - to read dataset and parse
from operator import itemgetter

# Classes for the FJSSP
from job import Job

# Kacem 4 Jobs x 5 Machines
#file = 'Encoding/datasets/test.fjs'
file = 'Encoding/datasets/Kacem1_4x5.fjs'

# Kacem 15 Jobs x 10 Machines
#file = 'Encoding/datasets/Kacem4.fjs'

# A list of Jobs
jobs_list = []

with open(file) as data:
    total_jobs, total_machines, max_operations = re.findall('\S+', data.readline())
    number_total_jobs, number_total_machines, number_max_operations = int(total_jobs), int(total_machines), int(float(
        max_operations))

    # Set Job Id to 1 to initiate dataset load
    currentJob = 1

    for key, line in enumerate(data):

        # Check if there are extra lines at the end of the dataset and stop the loop
        if key >= number_total_jobs:
            break
        parsed_line = re.findall('\S+', line)

        # For each Job a dict of operations
        job_operations = {}

        i = 1   # pointer to current item of parsed line

        currentOperation=1
        # while there are operations to retrieve for the current job in the parsed line extract tuples (machine, time)
        while i < len(parsed_line):
            number_operations = int(parsed_line[i])

            # a list to store pairs machine, time for each operation
            operation_tuples = []
            for id_operation in range(1, number_operations + 1):
                # operation tuple (machine, time)
                operation_tuple = int(parsed_line[i + 2 * id_operation - 1]), int(parsed_line[i + 2 * id_operation])
                # fill operation vector with machine,time
                operation_tuples.append(operation_tuple)

            # add operation and tuple sequence [(machine, exec_time)...] to dictionary
            job_operations[currentOperation] = operation_tuples
            currentOperation += 1

            # advance pointer to the next set of op sequences from dataset
            i += 1 + 2 * number_operations

        # add dictionary of operations for Job
        jobs_list.append(job_operations)

        # set next job to be processed
        currentJob += 1

print("List of ", len(jobs_list), " JOBs created")

for j in range(len(jobs_list)):
    print("JOB [", j+1, "] has ", len(jobs_list[j]), " operations")
    for key in jobs_list[j]:
        print(key, ' -> ', jobs_list[j][key])
print("\n")

#encoding
SolutionNum = 100
SolutionList = []
for i in range(SolutionNum):
    Solution = []
    for x in range(len(jobs_list)):
        for y in jobs_list[x]:
            #choose option rendomly to append to a solution being made
            OperationChosen = jobs_list[x][y][random.randint(0, len(jobs_list[x][y])-1)]
            Grade = len(jobs_list[x][y])
            for key in range(len(jobs_list[x][y])):
                if OperationChosen[1] > jobs_list[x][y][int(key)-1][1]: Grade = Grade -1
            Solution.append(Grade)
    SolutionList.append(Solution)

#print list os solutions
print("Solution list:")
for i in range(SolutionNum):
    print("Solution #",i,": ",SolutionList[i])
print("\n")


#crossover
ParsCrossover = 1
CrossoverList = []
for i in range(ParsCrossover):
    #getting two rendom solutions, cutting them in half and mixing them one with another
    s1 = SolutionList[random.randint(0, int(float(SolutionNum))-1)]
    s2 = SolutionList[random.randint(0, int(float(SolutionNum))-1)]
    Half = round(len(s1)/2)
    s1h1 = s1[:Half]
    s1h2 = s1[Half:]
    s2h1 = s2[:Half]
    s2h2 = s2[Half:]
    s2 = s1h1 + s2h2
    s1 = s2h1 + s1h2
    CrossoverList.append(s2)
    CrossoverList.append(s1)

#print new solutions made with crossover
print("New solutions made with crossover:")
print("Solution 1: ",CrossoverList[0])
print("Solution 2: ",CrossoverList[1])
print("\n")

#mutation
for i in range(len(CrossoverList)):
    #print("I: ",i)
    for x in range(len(jobs_list)):
        for y in jobs_list[x]:
            #print("len(jobs_list[x][y]) : ", len(jobs_list[x][y])," jobs_list[x][i+1]: ",len(jobs_list[x][i+1]))
            if len(jobs_list[x][y]) == len(jobs_list[x][i+1]): operatioNum = len(jobs_list[x][y]) 
    #print(operatioNum)           
    CrossoverList[i][random.randint(0, len(CrossoverList[i])-1)] = random.randint(1, operatioNum)

#Print new solutions after mutation
print("New solutions made with Mutation:")
print("Solution 1: ",CrossoverList[0])
print("Solution 2: ",CrossoverList[1])