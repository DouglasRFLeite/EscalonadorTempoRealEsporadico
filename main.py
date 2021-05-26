#!/usr/bin/env python
# coding: utf-8

from entrada import Entrada
from task import Task
from graficogantt import GraficoGantt
from escalonamento import Escalonamento

if __name__ == '__main__':

    try:

        #obter entrada        
        tasks, escalonador = Entrada.getInput()
        #criar tasks a partir de tuplas
        tasks = list(map(lambda a: Task(*a), tasks))
        #ordenar tasks de acordo com algoritmo RM ou EDF
        tasks = Escalonamento.ordena(tasks, escalonador)

        if Escalonamento.is_Escalonavel(tasks):

            print('\nAs tarefas são escalonáveis.\n')
            
            #limite de tempo que será simulado
            limite = Escalonamento.limiteTemporal(tasks)

            #simulação
            tasks, next_t = Escalonamento.simular(tasks, limite, escalonador)

            #fim do cálculo do escalonamento
            #parte gráfica
            grafico = GraficoGantt()
            grafico.gerarGantt(tasks, next_t, escalonador)
                        
        else:
            print('As tarefas não são escalonáveis.')
    
    except KeyboardInterrupt:
        pass
