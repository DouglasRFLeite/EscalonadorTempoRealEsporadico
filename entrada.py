# coding: utf-8

from sys import stdin

#classe que lida apenas com entrada e saida e formatacao de dados
#não possui funcionalidade de escalonamento
class Entrada:

    @staticmethod
    def getLineInput():
        return tuple(map(lambda x: int(x), stdin.readline().rstrip().split()))

    @staticmethod
    def getInput():
        ok = False
        while not ok:
            try:
                print('Informe o número de tarefas: ')
                n = Entrada.getLineInput()[0]
                ok = True
            except ValueError:
                print('Erro: Favor fornecer números inteiros como entrada.')

        ok = False
        while not ok:
            try:
                tasks = []
                print('Formato de entrada: instante_de_liberação tempo_de_computação período')
                for i in range(n):
                    print('Informe os parâmetros da tarefa %d: ' % (i+1))
                    tasks.append(Entrada.getLineInput())
                ok = True
            except ValueError:
                print('Erro: Favor fornecer números inteiros como entrada.')
        
        escalonador = -1
        while not escalonador in [1, 2]:
            print('Informe o algoritmo de escalonamento? (Escolhas: 1 = RM; 2 = EDF): ')
            try:
                escalonador = Entrada.getLineInput()[0]
            except ValueError:
                pass
        
        print()
        
        return tasks, escalonador
