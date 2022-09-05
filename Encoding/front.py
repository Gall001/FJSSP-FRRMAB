#streamlit Imports
import streamlit as st
import pandas as pd
import numpy as np
from crossover import PMX
from crossover import OX
from crossover import twoPoint
from mutation import swapMutation
from mutation import inverseMutation
from mutation import insertMutation
from correction import correction
#from mab import Bandit
from job import Job
from configparser import MissingSectionHeaderError
import random
import re                           # Regular Expressions - to read dataset and parse
from operator import itemgetter

#Genatic algorithm
class GA:

    def __init__(self,dataset, solutionNumber):
        # solutionNumber,crossoverChance,mutationChance, dataset, generationNumber
        # FJSSP Datasets Reader to Dictionaries
        # Lupercio F Luppi 2022
        # Kacem 4 Jobs x 5 Machines
        #file = 'FJSSP-FRRMAB/Encoding/datasets/test.fjs'
        #file = 'FJSSP-FRRMAB/Encoding/datasets/Kacem1_4x5.fjs'
        # Kacem 15 Jobs x 10 Machines
        #file = 'FJSSP-FRRMAB/Encoding/datasets/Kacem4.fjs'
        file = dataset

        # A list of Jobs
        self.jobs_list = []

        with open(file) as data:
            total_jobs, total_machines, max_operations = re.findall('\S+', data.readline())
            self.number_total_jobs, self.number_total_machines, number_max_operations = int(total_jobs), int(total_machines), int(float(
                max_operations))

            # Set Job Id to 1 to initiate dataset load
            currentJob = 1

            for key, line in enumerate(data):

                # Check if there are extra lines at the end of the dataset and stop the loop
                if key >= self.number_total_jobs:
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
                self.jobs_list.append(job_operations)

                # set next job to be processed
                currentJob += 1

        print("List of ", len(self.jobs_list), " JOBs created")
        st.write("List of ", len(self.jobs_list), " jobs created")

        for j in range(len(self.jobs_list)):
            print("JOB [", j+1, "] has ", len(self.jobs_list[j]), " operations")
            st.write("Job ", j+1, " has ", len(self.jobs_list[j]), " operations")
            for key in self.jobs_list[j]:
                print(key, ' -> ', self.jobs_list[j][key])
                st.write(key, ' -> ', self.jobs_list[j][key])
        print("\n")

        #encoding
        self.SolutionNum = solutionNumber
        self.SolutionList = []
        for i in range(self.SolutionNum):
            Solution = []
            Machine = []
            Order = []
            OperationOrder = 0
            for x in range(len(self.jobs_list)):
                for y in self.jobs_list[x]:
                    #choose option rendomly to append to a solution being made
                    OperationChosen = self.jobs_list[x][y][random.randint(0, len(self.jobs_list[x][y])-1)]
                    Grade = 1
                    for key in range(len(self.jobs_list[x][y])):
                        if OperationChosen[1] > self.jobs_list[x][y][int(key)-1][1]: Grade = Grade +1
                    OperationOrder += 1
                    Machine.append(Grade)
                    Order.append(OperationOrder)
            Solution.append(list(zip(Machine, Order)))
            self.SolutionList.append(Solution)

        #calculating incial makespan
        timeMachineOrganized = []
        for x in range(len(self.jobs_list)):
            for y in self.jobs_list[x]:
                timeMachineScrambled = []
                # Clone the vector into another one so it can organize
                for z in range(len(self.jobs_list[x][y])):
                    timeMachineScrambled.append(self.jobs_list[x][y][z])
                timeMachineOrganizedTemp = sorted(timeMachineScrambled, key=lambda x: x[1])
                timeMachineOrganized.append(timeMachineOrganizedTemp)
        self.solutionMachineTimeI = []

        #for each solution index number it search the number to add to self.solutionMachineTimeI
        for i in range(len(self.SolutionList)):
            timeMachineTemp = []
            order1 = []
            for x in range(len(self.SolutionList[i][0])):
                timeMachineTemp.append(timeMachineOrganized[x][self.SolutionList[i][0][x][0] - 1])
                order1.append(self.SolutionList[i][0][x][1])
            self.solutionMachineTimeI.append(timeMachineTemp)
            
        for i in range(len(self.solutionMachineTimeI)):
            jobs = []
            machines = []
            jobAtual = 0
            contador = 0
            for job in range(self.number_total_jobs):
                jobs.append(0)
            for machine in range(self.number_total_machines):
                machines.append(0)
            for solution in range(len(self.solutionMachineTimeI[i])):     
                if(contador > len(self.jobs_list[jobAtual])-1): 
                    jobAtual += 1
                    contador = 0
                contador += 1
                if(machines[self.solutionMachineTimeI[i][solution][0]-1] >= jobs[jobAtual]):
                    machines[self.solutionMachineTimeI[i][solution][0]-1] += self.solutionMachineTimeI[i][solution][1]
                    jobs[jobAtual] = machines[self.solutionMachineTimeI[i][solution][0]-1]
                else:
                    jobs[jobAtual] += self.solutionMachineTimeI[i][solution][1] 
                    machines[self.solutionMachineTimeI[i][solution][0]-1] = jobs[jobAtual]
            self.solutionMachineTimeI[i].append(order1)
            self.solutionMachineTimeI[i].append(max(machines))
        #print('ALL SOLUTIONS MACHINE TIME I: ',self.solutionMachineTimeI)

        #print list os solutions
        # print("Solution list:")
        # for i in range(self.SolutionNum):
        #     print("Solution #",i,": ",self.SolutionList[i])
        # print("\n")
        # st.write("Exemple of solution: ", self.SolutionList[0])

    def methods(self,generationNumber, crossoverChance, mutationChance, action):
        for i in range(generationNumber):
            #crossover
            for x in range(self.SolutionNum):
                CrossoverList = []
                s1 = self.SolutionList[random.randint(0, int(float(self.SolutionNum))-1)][0]
                s2 = self.SolutionList[random.randint(0, int(float(self.SolutionNum))-1)][0]
                CrossoverList.append(s1)
                CrossoverList.append(s2)
                validator = 0

                if(random.random() <= crossoverChance):

                    #crossover
                    if action == 0:
                        twoPoint(CrossoverList,s1,s2)
                    elif action == 1:
                        OX(CrossoverList,s1,s2)
                    elif action == 2:
                        PMX(CrossoverList,s1,s2)

                    validator = 1


                if(random.random() <= mutationChance):

                    #mutation
                    if action == 0:
                        swapMutation(CrossoverList)
                    elif action == 1:
                        inverseMutation(CrossoverList)
                    elif action == 2:
                        insertMutation(CrossoverList)

                    validator = 1

                #solution corrector
                for i in range(len(CrossoverList)):
                    minValue = 1
                    maxValue = 0
                    for job in range(len(self.jobs_list)):
                        maxValue += len(self.jobs_list[job])
                        CrossoverList[i] = correction(minValue,maxValue,CrossoverList[i])
                        minValue += len(self.jobs_list[job])
                        
                        
                #Print new solutions after mutation
                # print("New solutions made with Mutation/crossover:")
                # for i in range(len(CrossoverList)):
                #     print("Solution ",i,": ",CrossoverList[i])
                # print("\n")

                #inserting new solution in list
                for i in range(len(CrossoverList)):
                    self.SolutionList.append(CrossoverList[i])


            #makespan Vector for each index on encoding
            #Duas listas, uma com tempo de job e outra com tempo da máquina, toda vez que for pega o tempo do job adiciona tempo da maquina rodando, depois de adicioonar pega
            #esse numero e adiciona na lista para falar o tempoo do job e o proxima operaçao tem que ser iniciado depois desse tempo

            #array that stores each machine and time for each operation on each job globally
            if(validator == 1):
                timeMachineOrganized = []
                for x in range(len(self.jobs_list)):
                    for y in self.jobs_list[x]:
                        timeMachineScrambled = []
                        # Clone the vector into another one so it can organize
                        for z in range(len(self.jobs_list[x][y])):
                            timeMachineScrambled.append(self.jobs_list[x][y][z])
                        timeMachineOrganizedTemp = sorted(timeMachineScrambled, key=lambda x: x[1])
                        timeMachineOrganized.append(timeMachineOrganizedTemp)
                solutionMachineTime = []

                #for each solution index number it search the number to add to solutionMachineTime
                for i in range(len(CrossoverList)):
                    timeMachineTemp = []
                    order2 = []
                    for x in range(len(CrossoverList[i])):
                        timeMachineTemp.append(timeMachineOrganized[x][CrossoverList[i][x][0] - 1])
                        order2.append(self.SolutionList[i][0][x][1])
                    solutionMachineTime.append(timeMachineTemp)


                # Caluclating Makespan
                for i in range(len(solutionMachineTime)):
                    jobs = []
                    machines = []
                    jobAtual = 0
                    contador = 0
                    for job in range(self.number_total_jobs):
                        jobs.append(0)
                    for machine in range(self.number_total_machines):
                        machines.append(0)
                    for solution in range(len(solutionMachineTime[i])):     
                        if(contador > len(self.jobs_list[jobAtual])-1): 
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
                    self.solutionMachineTimeI.append(solutionMachineTime[i])

        # print("Final Solution list:")
        # for i in range(len(self.SolutionList)):
        #     print("Solution #",i,": ",self.SolutionList[i])
        # print("\n")
        return min(self.solutionMachineTimeI, key=lambda x: x[-1])[-1]

    def showResult(self):  
        st.write('Best solution sequence: ', min(self.solutionMachineTimeI, key=lambda x: x[-1]))
        st.write('Best solution found: ', min(self.solutionMachineTimeI, key=lambda x: x[-1])[-1])