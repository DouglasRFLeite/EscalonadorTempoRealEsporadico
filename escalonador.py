#!/usr/bin/env python
# coding: utf-8

# In[1]:


from random import *
from math import ceil

string = '{(1,2,3), (4,5,6)}'

b = string.replace('{', '').replace('}', '').replace('(','').replace(')','').replace(' ','').split(',')
print(b)

escalonador = 1 #1 para RM e 2 para EDF


# In[6]:


class Task:
    def __init__(self, R, C, T):
        self.Ri = R #primeiro instante de liberação
        self.C = C  #tempo de execução
        self.T = T  #intervalo mínimo entre execuções
        self.R = R  #próximo instante de liberação 
        self.D = self.Ri + self.T #deadline
        self.to_do = C #tempo a ser executado
        
        if self.C == 0: self.to_do = 10000000000000

        
    def calculaR(self):
        aleatorio = randint(0, self.T)
        self.R = self.R + self.T + aleatorio #próxima liberação vai ser no mínimo T instantes depois da última e no máximo 2T
    
    def end(self):
        self.calculaR()
        self.D = self.R + self.T
        self.to_do = self.C
    
    def __repr__(self):
        return "("+str(self.R)+","+str(self.C)+","+str(self.T)+")"
        


    
    
def ordena(tasks, string = 'RM'):
    idle_task = tasks[len(tasks)-1]
    tasks.remove(idle_task)
    
    if string == 'RM':
        tasks = sorted(tasks, key=lambda task: 1/task.T, reverse = True)
    else: 
        tasks = sorted(tasks, key=lambda task: task.D)    
    
    tasks.append(idle_task)
    return tasks
    
    
def LUB(n):
    return n*(2**(1/n) - 1)

def U(tasks):
    U = 0
    
    for task in tasks:
        U = U + (task.C / task.T)
        
    return U

def Rk(Ci, hp):
    #print('ok2')
    R0 = Ci
    while(True):
        R = Ci
        for task in hp:
            #print('ok3')
            R = R + ceil(R0/task.T)*task.C
        if R == R0:
            print('R = ',R)
            return R
        else:
            R0 = R

def ATF(tasks):
    #print('ok1')
    for task in tasks:
        hp=[]
        for i in range(tasks.index(task)):
            hp.append(tasks[i])
        
        #print(hp)
        if Rk(task.C, hp) > task.T:
            return False
    
    return True

def is_Escalonavel(tasks):
    #teste por LUB
    n = len(tasks)
    lub = LUB(n)
    print('LUB = ',lub)
    u = U(tasks)
    print('U = ', u)
    if lub > u:
        return True
    else:
        return ATF(tasks)

def getTimes(tasks):
    times=[]
    for task in tasks:
        times.append(task.R)
    times.sort()
    return times

def getInput():
    n = int(input("Digite o valor de n: "))
    string = input("Agora insira as n tarefas no formato (r_i, Ci, Ti): ")
    
    if string=='':
        string = '{(0,2,7),(1,2,5),(2, 3, 14)}'
    
    print(string)
    values = string.replace('{', '').replace('}', '').replace('(','').replace(')','').replace(' ','').split(',')
    tasks = []
    
    for i in range(n):
        R = int(values[i*3])
        C = int(values[i*3 + 1])
        T = int(values[i*3 + 2])
        tasks.append(Task(R,C,T))
    
    escalonador = input("Qual será o algoritmo de escalonamento? Escolha entre RM e EDF: ")
    
    if escalonador == '':
        escalonador = 'RM'
    
    tasks = ordena(tasks, escalonador)
    
    return tasks
        


# In[8]:


tasks = getInput()

if is_Escalonavel(tasks):
    print("As tarefas são escalonáveis!")
    t = 0
    ocupado = False
    ativo = -1
    idle_task = Task(0,0,0)
    tasks.append(idle_task)
    
    while(t<50):
        
        ativo = tasks.index(idle_task)
        
        next_t = 100000000
        for task in tasks:            
            if task.R <= t:
                ativo = tasks.index(task)
                next_t = t + task.to_do
                break
        for task in tasks:
            if task.R>t and task.R<next_t:
                next_t = task.R
        
        steady_time = next_t - t
        tasks[ativo].to_do = tasks[ativo].to_do - steady_time
        print("t = ",t,' \tnext_t = ',next_t,' \tto_do = ',tasks[ativo].to_do, ' \ttarefa_ativa = ', tasks[ativo])
        
        
        
        if tasks[ativo].to_do <= 0:
            
            tasks[ativo].end()
            
            tasks = ordena(tasks, escalonador)
            
        print("t = ",t,' \tnext_t = ',next_t, '\ttarefas = ', tasks, end='\n\n')            
            
        t = next_t
                
                
            
                
    
    
else:
    print("As tarefas não são escalonáveis...")


# In[ ]:


testes = [1,2,3]

for x in testes:
    print(x)
    testes.append(x+3)
    if x>50:
        break


# In[ ]:




