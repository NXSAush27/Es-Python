

import albero

'''
    Es 12: 3 punti
    Un albero si dice binario completo se tutti i suoi nodi interni hanno esattamente 2 
    figli e tutte le foglie si trovano allo stesso livello.
    Si definisca la funzione es12(k ) ricorsiva (o che fa uso di funzioni o 
    metodi ricorsive/i) che:
    - riceve come argomenti  un intero k 
    - costruisce un albero binario completo di altezza k composta da nodi del tipo  
      Nodo definito nella libreria albero.py allegata. Gli identificatore delle foglie, 
      letti da sinistra a destra sono i 2^k-interi che vanno da 1 a 2^k (nota che 
      un albero binario completo di altezza k ha sempre 2^k foglie). Gli identificatori 
      dei nodi interni sono dati dalla somma degli identificatori dei due loro figli. 
    - torna come risultato la radice dell'albero costruito. 
    Esempio: 
    - es12(2)  crea e restituisce l'albero a sinistra 
    - es12(3) crea e restituisce l'albero a destra


                    10                                  36               
             _______|______                      _______|______         
            |              |                    |              |        
            3              7                   10             26        
         ___|___        ___|__               ___|___        ___|__      
        |       |      |      |             |       |      |      |     
        1       2      3      4             3       7     11     15     
                                           _|_     _|_    _|_    _|_    
                                          |   |   |   |  |   |  |   |   
                                          1   2   3   4  5   6  7   8   
                                                                   
    '''


def es1(k):
    albero_radice, _ = costruisci_albero(k, 1)
    return albero_radice


def costruisci_albero(k, start):
    if k == 0: 
        return albero.Nodo(start), start + 1
    # Costruisci il sottoalbero sinistro
    left_child, next_start = costruisci_albero(k - 1, start)
    # Costruisci il sottoalbero destro
    right_child, next_start = costruisci_albero(k - 1, next_start)
    # Crea il nodo genitore con la somma dei valori dei figli
    parent_value = left_child.id + right_child.id
    # Crea il nodo genitore
    parent_node = albero.Nodo(parent_value)
    # Assegna i figli al nodo genitore
    parent_node.f = [left_child, right_child]
    return parent_node, next_start