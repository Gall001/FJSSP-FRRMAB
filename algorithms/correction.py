#job 3:
#min = 5
#max = 10

#solucao x
#3list = [(1, 1), (1, 2), (1, 3), (5, 5), (3, 7), (3, 6), (2, 4), (1, 8), (3, 9), (4, 10), (5, 11), (1, 12)]


def correction(min, max, list):
    """Um algoritmo que ordena uma lista de tuplas a partir do valor min e maximo dado,
       utilizando o segundo filho da tupla

    Args:
        min (Int): primeira operacao no job
        max (Int): ultima operacao no job
        list (list): uma solucao gerada por crossover + mutacao

    Returns:
        list: uma solucao factivel 
    """
    atual = min
    for key in list:
        #print(key[1])
        #ordencao sentinela
        if key[1] >= atual and key[1] <= max and key[1] != atual:
            list.sort(key=lambda tup: tup[1])
            #print('order needed: ', list)
            return list
        elif key[1] == atual and atual<max:
            atual = atual+1
    #print('order not needed: ', list)
    return list

#correction(min,max,list)

