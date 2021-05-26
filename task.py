# coding: utf-8

from random import randint

#classe que define uma tarefa do escalonamento e seus dados e métodos
class Task:

    current_id = 1

    def __init__(self, R, C, T):
        self.Ri = R #primeiro instante de liberação
        self.C = C  #tempo de execução
        self.T = T  #intervalo mínimo entre execuções
        self.R = R  #próximo instante de liberação 
        self.D = self.Ri + self.T #deadline
        self.execucoes = []
        
        if self.C == 0: 
            self.to_do = 10000000000000
            self.id = 0
        else:
            self.to_do = C #tempo a ser executado
            self.id = Task.current_id
            Task.current_id += 1

    def idText(self):
        if self.id == 0:
            return 'Ociosa'
        else:
            return str(self.id)

    def toDoText(self):
        if self.id == 0:
            return 'Infinito'
        else:
            return str(self.to_do)
   
    def calculaR(self):
        aleatorio = randint(0, self.T)
        self.R = self.R + self.T + aleatorio #próxima liberação vai ser no mínimo T instantes depois da última e no máximo 2T
    
    def end(self):
        self.calculaR()
        self.D = self.R + self.T
        self.to_do = self.C
    
    def __repr__(self):
        return '('+str(self.R)+','+str(self.C)+','+str(self.T)+')'
