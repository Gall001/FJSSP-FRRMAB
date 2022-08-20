#streamlit Imports
import streamlit as st
import pandas as pd
import numpy as np
from mutation import swapMutation
from mutation import inverseMutation
from mutation import insertMutation
from correction import correction
#streamlit title
st.title('Genetic Algorithm')

#Genatic algorithm
def GA(solutionNumber,crossoverChance,mutationChance, dataset, generationNumber):
    # FJSSP Datasets Reader to Dictionaries
    # Lupercio F Luppi 2022
    from configparser import MissingSectionHeaderError
    import random
    import re                           # Regular Expressions - to read dataset and parse
    from operator import itemgetter

    # Classes for the FJSSP
    from job import Job

    # Kacem 4 Jobs x 5 Machines
    #file = 'FJSSP-FRRMAB/Encoding/datasets/test.fjs'
    #file = 'FJSSP-FRRMAB/Encoding/datasets/Kacem1_4x5.fjs'

    # Kacem 15 Jobs x 10 Machines
    #file = 'FJSSP-FRRMAB/Encoding/datasets/Kacem4.fjs'

    file = dataset

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
    st.write("List of ", len(jobs_list), " jobs created")

    for j in range(len(jobs_list)):
        print("JOB [", j+1, "] has ", len(jobs_list[j]), " operations")
        st.write("Job ", j+1, " has ", len(jobs_list[j]), " operations")
        for key in jobs_list[j]:
            print(key, ' -> ', jobs_list[j][key])
            st.write(key, ' -> ', jobs_list[j][key])
    print("\n")

    #encoding
    SolutionNum = solutionNumber
    SolutionList = []
    for i in range(SolutionNum):
        Solution = []
        Machine = []
        Order = []
        OperationOrder = 0
        for x in range(len(jobs_list)):
            for y in jobs_list[x]:
                #choose option rendomly to append to a solution being made
                OperationChosen = jobs_list[x][y][random.randint(0, len(jobs_list[x][y])-1)]
                Grade = 1
                for key in range(len(jobs_list[x][y])):
                    if OperationChosen[1] > jobs_list[x][y][int(key)-1][1]: Grade = Grade +1
                OperationOrder += 1
                Machine.append(Grade)
                Order.append(OperationOrder)
        Solution.append(list(zip(Machine, Order)))
        SolutionList.append(Solution)
        # print('solution two vetors: ')
        # print(Solution)
        # print('solution one vetors: ')
        # print(Machine)

    #calculating incial makespan
    timeMachineOrganized = []
    for x in range(len(jobs_list)):
        for y in jobs_list[x]:
            timeMachineScrambled = []
            # Clone the vector into another one so it can organize
            for z in range(len(jobs_list[x][y])):
                timeMachineScrambled.append(jobs_list[x][y][z])
            timeMachineOrganizedTemp = sorted(timeMachineScrambled, key=lambda x: x[1])
            timeMachineOrganized.append(timeMachineOrganizedTemp)
    solutionMachineTimeI = []

    #for each solution index number it search the number to add to solutionMachineTimeI
    for i in range(len(SolutionList)):
        timeMachineTemp = []
        order1 = []
        for x in range(len(SolutionList[i][0])):
            timeMachineTemp.append(timeMachineOrganized[x][SolutionList[i][0][x][0] - 1])
            order1.append(SolutionList[i][0][x][1])
        solutionMachineTimeI.append(timeMachineTemp)
        
    for i in range(len(solutionMachineTimeI)):
        jobs = []
        machines = []
        jobAtual = 0
        contador = 0
        for job in range(number_total_jobs):
            jobs.append(0)
        for machine in range(number_total_machines):
            machines.append(0)
        for solution in range(len(solutionMachineTimeI[i])):     
            if(contador > len(jobs_list[jobAtual])-1): 
                jobAtual += 1
                contador = 0
            contador += 1
            if(machines[solutionMachineTimeI[i][solution][0]-1] >= jobs[jobAtual]):
                machines[solutionMachineTimeI[i][solution][0]-1] += solutionMachineTimeI[i][solution][1]
                jobs[jobAtual] = machines[solutionMachineTimeI[i][solution][0]-1]
            else:
                jobs[jobAtual] += solutionMachineTimeI[i][solution][1] 
                machines[solutionMachineTimeI[i][solution][0]-1] = jobs[jobAtual]
        solutionMachineTimeI[i].append(order1)
        solutionMachineTimeI[i].append(max(machines))
    #print('ALL SOLUTIONS MACHINE TIME I: ',solutionMachineTimeI)

    #print list os solutions
    print("Solution list:")
    for i in range(SolutionNum):
        print("Solution #",i,": ",SolutionList[i])
    print("\n")
    st.write("Exemple of solution: ", SolutionList[0])

    for i in range(generationNumber):
        #crossover
        for x in range(SolutionNum):
            CrossoverList = []
            validator = 0
            if(random.random() <= crossoverChance):
                #getting two rendom solutions, cutting them in half and mixing them one with another
                s1 = SolutionList[random.randint(0, int(float(SolutionNum))-1)][0]
                s2 = SolutionList[random.randint(0, int(float(SolutionNum))-1)][0]
                Half = round(len(s1)/2)
                s1h1 = s1[:Half]
                s1h2 = s1[Half:]
                s2h1 = s2[:Half]
                s2h2 = s2[Half:]
                s2 = s1h1 + s2h2
                s1 = s2h1 + s1h2
                CrossoverList.append(s2)
                CrossoverList.append(s1)
                validator +=1

                #print new solutions made with crossover
                # print("New solutions made with crossover:")
                # for i in range(len(CrossoverList)):
                #     print("Solution ",i,": ",CrossoverList[i])
                # print("\n")

            if(random.random() <= mutationChance and validator == 1):

                #mutation
                CrossoverList = swapMutation(CrossoverList)
                CrossoverList = inverseMutation(CrossoverList)
                CrossoverList = insertMutation(CrossoverList)

            #solution corrector
            for i in range(len(CrossoverList)):
                minValue = 1
                maxValue = 0
                print('solution #',i)
                for job in range(len(jobs_list)):
                    maxValue += len(jobs_list[job])
                    print("min value = ",minValue," max value = ",maxValue)
                    correction(minValue,maxValue,CrossoverList[i])
                    minValue += len(jobs_list[job])
                    
                    
                    
            #Print new solutions after mutation
            print("New solutions made with Mutation/crossover:")
            for i in range(len(CrossoverList)):
                print("Solution ",i,": ",CrossoverList[i])
            print("\n")

            #inserting new solution in list
            for i in range(len(CrossoverList)):
                SolutionList.append(CrossoverList[i])


        #makespan Vector for each index on encoding
        #Duas listas, uma com tempo de job e outra com tempo da máquina, toda vez que for pega o tempo do job adiciona tempo da maquina rodando, depois de adicioonar pega
        #esse numero e adiciona na lista para falar o tempoo do job e o proxima operaçao tem que ser iniciado depois desse tempo

        #array that stores each machine and time for each operation on each job globally
        if(validator == 1):
            timeMachineOrganized = []
            for x in range(len(jobs_list)):
                for y in jobs_list[x]:
                    timeMachineScrambled = []
                    # Clone the vector into another one so it can organize
                    for z in range(len(jobs_list[x][y])):
                        timeMachineScrambled.append(jobs_list[x][y][z])
                    timeMachineOrganizedTemp = sorted(timeMachineScrambled, key=lambda x: x[1])
                    timeMachineOrganized.append(timeMachineOrganizedTemp)
            solutionMachineTime = []

            #for each solution index number it search the number to add to solutionMachineTime
            for i in range(len(CrossoverList)):
                timeMachineTemp = []
                order2 = []
                for x in range(len(CrossoverList[i])):
                    timeMachineTemp.append(timeMachineOrganized[x][CrossoverList[i][x][0] - 1])
                    order2.append(SolutionList[i][0][x][1])
                solutionMachineTime.append(timeMachineTemp)

            # Print solution Machines and time after mutation
            # print("solution Machines and time after Mutation:")
            # for i in range(len(solutionMachineTime)):
            #     print("Solution ",i,": ",solutionMachineTime[i])
            # print("\n")


            # Caluclating Makespan
            for i in range(len(solutionMachineTime)):
                jobs = []
                machines = []
                jobAtual = 0
                contador = 0
                for job in range(number_total_jobs):
                    jobs.append(0)
                for machine in range(number_total_machines):
                    machines.append(0)
                for solution in range(len(solutionMachineTime[i])):     
                    if(contador > len(jobs_list[jobAtual])-1): 
                        jobAtual += 1
                        contador = 0
                    contador += 1
                    if(machines[solutionMachineTime[i][solution][0]-1] >= jobs[jobAtual]):
                        machines[solutionMachineTime[i][solution][0]-1] += solutionMachineTime[i][solution][1]
                        jobs[jobAtual] = machines[solutionMachineTime[i][solution][0]-1]
                    else:
                        jobs[jobAtual] += solutionMachineTime[i][solution][1] 
                        machines[solutionMachineTime[i][solution][0]-1] = jobs[jobAtual]
                solutionMachineTime[i].append(order2)
                solutionMachineTime[i].append(max(machines))
                solutionMachineTimeI.append(solutionMachineTime[i])

    print("Final Solution list:")
    for i in range(len(SolutionList)):
        print("Solution #",i,": ",SolutionList[i])
    print("\n")
            
    st.write('Best solution sequence: ', min(solutionMachineTimeI, key=lambda x: x[-1]))
    st.write('Best solution found: ', min(solutionMachineTimeI, key=lambda x: x[-1])[-1])


a = st.sidebar.number_input("Population size", 1, 100000)
b = st.sidebar.slider('Crossover Chance', 0.0, 1.0, 0.5)
e = st.sidebar.slider('Mutation Chance', 0.0, 1.0, 0.5)
d = st.sidebar.number_input("Number of Generations", 1, 100000)
c = st.sidebar.selectbox(
    'Select dataset',
    ('FJSSP-FRRMAB/Encoding/datasets/test.fjs', 'FJSSP-FRRMAB/Encoding/datasets/Kacem1_4x5.fjs', 'FJSSP-FRRMAB/Encoding/datasets/Kacem4.fjs'))


if st.sidebar.button("Run Genetic Algorithm"):
    GA(a,b,e,c,d)