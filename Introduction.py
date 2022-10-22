import streamlit as st


st.title('Using Hyper-hueristics to resolve the FJSSP')
st.caption('This project was made by Gal Levy, a member of the artificial intelligence scientific research group of UniFil.')
st.caption('In this project, a genetic algorithm utilizing the multi-armed bandit problem as a hyper-heuristic to choose the methods used in each generation.')

st.header('Genetic Algorithm Parameters')

st.subheader('Population size')
st.caption('This parameter represents the number of individuals created as baseline for the genetic algorithm to utilize.')

st.subheader('Crossover Chance')
st.caption('This parameter represents the chance of a new solution being made to go through the crossover methods, meaning it will be made by two existing solutions combining them to create a new solution.')

st.subheader('Mutation Chance')
st.caption('This parameter represents the chance of a new solution being made to go through the mutation method, meaning the solution will suffer a mutation changing a part pf the solution to add variation.')

st.subheader('Number of Generations')
st.caption('This parameter represents the quantity of generation that the algorithm will goo trough, in each generation the algorithm will create new solution using the old population and then replacing them.')

st.header('Multi-Armed Bandit Parameters')

st.subheader('exp_rate')
st.caption('This parameter represents the rate in which the Multi-Amred Bandit will explore new possibilities utilizing randoms values to set the method of the genetic algorithm .')

st.subheader('lr')
st.caption('This parameter represents the rate in which the Multi-Amred Bandit will remember and learn which arm brings the best results to use in futures generations .')
