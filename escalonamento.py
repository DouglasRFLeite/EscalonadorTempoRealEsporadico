# coding: utf-8

from math import ceil
from functools import reduce

from task import Task

class Escalonamento:

    @staticmethod   
    def ordena(tasks, algoritmo):
        idle_task = tasks[len(tasks)-1]
        tasks.remove(idle_task)
        
        #RM
        if algoritmo == 1:
            tasks = sorted(tasks, key=lambda task: 1/task.T, reverse = True)
        #EDF
        else: 
            tasks = sorted(tasks, key=lambda task: task.D)    
        
        tasks.append(idle_task)
        return tasks
    
    @staticmethod
    def LUB(n):
        return n*(2**(1/n) - 1)

    @staticmethod
    def U(tasks):
        U = 0
        
        for task in tasks:
            U = U + (task.C / task.T)
            
        return U

    @staticmethod
    def Rk(Ci, hp):
        R0 = Ci
        while(True):
            R = Ci
            for task in hp:
                R = R + ceil(R0/task.T)*task.C
            if R == R0:
                print('R = ',R)
                return R
            else:
                R0 = R

    @classmethod
    def ATF(cls, tasks):
        for task in tasks:
            hp=[]
            for i in range(tasks.index(task)):
                hp.append(tasks[i])
            
            if cls.Rk(task.C, hp) > task.T:
                return False
        
        return True

    @classmethod
    def is_Escalonavel(cls, tasks):
        #teste por LUB
        n = len(tasks)
        lub = cls.LUB(n)
        print('LUB = ',lub)
        u = cls.U(tasks)
        print('U = ', u)
        if lub > u:
            return True
        else:
            return cls.ATF(tasks)

    @staticmethod
    def getTimes(tasks):
        times=[]
        for task in tasks:
            times.append(task.R)
        times.sort()
        return times

    @staticmethod
    def limiteTemporal(tasks):

        #dez vezes o maior periodo
        return 10 * reduce(lambda a, b: max(a, b), map(lambda x: x.T, tasks))

    @classmethod
    def simular(cls, tasks, limite, escalonador):

        t = 0
        ocupado = False
        ativo = -1
        idle_task = Task(0,0,0)
        tasks.append(idle_task)
        
        while(t<limite):
            
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
            tasks[ativo].execucoes.append((t, next_t-t))
            print('Tempo =',t,'; Seguinte =',next_t,'; A Fazer =',tasks[ativo].toDoText(), '; Atividade = Tarefa', tasks[ativo].idText(), '; Tarefas =', tasks[:-1], end='\n\n')    
            
            if tasks[ativo].to_do <= 0:
                
                tasks[ativo].end()
                
                tasks = cls.ordena(tasks, escalonador)       
                
            t = next_t

        return tasks, next_t
