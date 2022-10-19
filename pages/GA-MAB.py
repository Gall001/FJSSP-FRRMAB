import imp
import streamlit as st
from algorithms.ga import GA
from algorithms.mab import Bandit

#streamlit info
st.title('Genetic Algorithm')

a = st.sidebar.number_input("Population size", 1, 100000)
b = st.sidebar.slider('Crossover Chance', 0.0, 1.0, 0.5)
e = st.sidebar.slider('Mutation Chance', 0.0, 1.0, 0.5)
d = st.sidebar.number_input("Number of Generations", 1, 100000)
f = st.sidebar.slider('exp_rate', 0.0, 1.0, 0.5)
g = st.sidebar.slider('lr', 0.0, 1.0, 0.5)
h = st.sidebar.selectbox(
    'UCB mode',
    ('False','True')
)
c1 = st.sidebar.selectbox(
    'Select dataset',
    ('FJSSP-FRRMAB/datasets/test.fjs', 'FJSSP-FRRMAB/datasets/Kacem1_4x5.fjs', 'FJSSP-FRRMAB/datasets/Kacem4.fjs'))

if st.sidebar.button("Run MAB"):
    bdt = Bandit(exp_rate=f, lr=g, ucb=h, a=a, b=b, c1=c1, e=e)
    bdt.play(d)