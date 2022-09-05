import numpy as np
import streamlit as st
from front import GA

#streamlit title
st.title('Genetic Algorithm')

class Bandit:
    def __init__(self, k=3, exp_rate=0.3, lr=0.1, ucb=False, seed=None, c=2, a=100,b=0.7,c1='FJSSP-FRRMAB/Encoding/datasets/Kacem1_4x5.fjs',d=10,e=0.4):
        self.k = k #PMX, OX and two vetores = 3
        self.actions = range(self.k) #[0,1,2]
        self.exp_rate = exp_rate
        self.lr = lr
        self.total_reward = 0
        self.avg_reward = []
        self.generation = d
        self.crossovr = b
        self.mutation = e
        
        self.TrueValue = []
        np.random.seed(seed)
        for i in range(self.k):
            self.TrueValue.append(np.random.randn()+2)  # normal distribution
        
        self.values = np.zeros(self.k)
        # for ucb
        self.times = 0
        self.action_times = np.zeros(self.k)
        
        self.ucb = ucb  # if select action using upper-confidence-bound
        self.c = c
        self.ga = GA(c1,a)
    
    def chooseAction(self):
        # explore
        # when ucb is turned on, exp_rate can tune to 0
        if np.random.uniform(0, 1) <= self.exp_rate:  
            action = np.random.choice(self.actions)
        else:
            # exploit
            if self.ucb:
                if self.times == 0:
                    action = np.random.choice(self.actions)
                else:
                    confidence_bound = self.values + self.c*np.sqrt(np.log(self.times)/(self.action_times+0.1))  # c=2
                    action = np.argmax(confidence_bound)
            else:
                action = np.argmax(self.values)
        return action
    
    def takeAction(self, action):
        self.times += 1
        self.action_times[action] += 1
        # take action and update value estimates
        reward = self.ga.methods(self.generation,self.crossovr,self.mutation, action) + self.TrueValue[action]  # add randomness to reward
        # using incremental method to propagate
        self.values[action] += self.lr * (reward - self.values[action])  # look like fixed lr converges better
        
        self.total_reward += reward
        self.avg_reward.append(self.total_reward/self.times)
        
    def play(self, n):
        for _ in range(n):
            #GA 
            #PARTE DO CROSS E MUT
            action = self.chooseAction()
            #Action = 0 - PMX
            self.takeAction(action)
        self.ga.showResult()


#streamlit info
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
    ('FJSSP-FRRMAB/Encoding/datasets/test.fjs', 'FJSSP-FRRMAB/Encoding/datasets/Kacem1_4x5.fjs', 'FJSSP-FRRMAB/Encoding/datasets/Kacem4.fjs'))
i = st.sidebar.number_input("Iterations of MAB", 1, 100000)

if st.sidebar.button("Run MAB"):
    bdt = Bandit(exp_rate=f, lr=g, ucb=h, a=a, b=b, c1=c1, d=d, e=e)
    bdt.play(i)