#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from math import sqrt
from tree import BinaryTree
from nary_tree import NaryTree

################################################################################
################################################################################
################################################################################

""" Operazioni da fare PRIMA DI TUTTO:
 1) Assegnare le variabili sottostanti con il tuo
    NOME, COGNOME, NUMERO DI MATRICOLA
"""
nome       = "F"
cognome    = "L"
matricola  = "69"
################################################################################
################################################################################
################################################################################
# %% ----------------------------------- EX.1 ----------------------------------- #
"""
Ex1: 6 punti
Implementate la funzione ex1(N) che, dato un intero N positivo o nullo, 
restituisce l'N-esimo termine della successione di Lucas del primo tipo, U(N, P, Q), definita come segue:
    U(0, *, *) = 0
    U(1, *, *) = 1
    U(n, P, Q) = P * U(n-1, P, Q) - Q * U(n-2, P, Q) per n >= 2.

La funzione deve essere ricorsiva, oppure chiamare una funzione ricorsiva top-level, ossia definita esternamente 
ed al suo stesso livello nel file corrente. 
"""
def ex1(N, P, Q):
    if N == 0:
        return 0
    if N == 1:
        return 1
    return P * ex1(N-1, P, Q) - Q * ex1(N-2, P, Q)

# %% ----------------------------------- EX.2 ----------------------------------- #
'''
Ex2: 8 punti

Implementa la funzione ex2(root) che riceve in ingresso root, un'istanza di albero binario, così come definito
nella classe BinaryTree del modulo tree. 
La funzione deve trovare e restituire il massimo valore che si ottiene, per ciascun nodo dell'albero,
calcolando la differenza in valore assoluto tra:
-   la somma dei valori dei nodi del sottoalbero sinistro
- e la somma dei valori dei nodi del sottoalbero destro 
Per un nodo foglia, la differenza è 0. 

La funzione deve essere ricorsiva, oppure chiamare una funzione ricorsiva top-level, ossia definita esternamente 
ed al suo stesso livello nel file corrente. 
'''

def _ex2_helper(node, max_diff):
    if node is None:
        return 0, max_diff
    
    left_sum, max_diff = _ex2_helper(node.left, max_diff)
    right_sum, max_diff = _ex2_helper(node.right, max_diff)
    
    subtree_sum = node.value + left_sum + right_sum
    
    diff = abs(left_sum - right_sum)
    if diff > max_diff:
        max_diff = diff
    
    return subtree_sum, max_diff

def ex2(root: BinaryTree):
    _, max_diff = _ex2_helper(root, 0)
    return max_diff


# %% ----------------------------------- EX.3 ----------------------------------- #
'''
Ex3: 8 points 
Implementa la funzione ex3(dirin, K, extensions) che, dato il percorso di una directory dirin, 
un intero K e una lista di estensioni target (es. ['txt', 'pdf']), deve trovare tutte 
le directory che contengono un numero sufficiente di file con una delle estensioni specificate.

Restituisci un dizionario che ha:
  - Come chiavi: il path completo (stringa) di ogni directory (usando '/' come separatore).
  - Come valori: il numero totale di file (conteggiati ricorsivamente in tutti i sottolivelli) 
    la cui estensione è presente nella lista extensions.
Il dizionario deve includere solo le directory in cui il conteggio totale di tali file è strettamente maggiore di K.

La funzione deve essere ricorsiva, oppure chiamare una funzione ricorsiva top-level, ossia definita esternamente 
ed al suo stesso livello nel file corrente. 
'''

import os

def _ex3_helper(path, extensions):
    """
    Recursively counts files with specific extensions in a directory tree.
    
    This helper function traverses a directory and all its subdirectories,
    counting files that have extensions matching those provided in the
    extensions parameter.
    
    Args:
        path (str): The root directory path to start searching from.
        extensions (list or set): A collection of file extensions to match
                                 (without the leading dot, e.g., ['txt', 'pdf']).
    
    Returns:
        int: The total count of files matching the specified extensions
             found in the directory tree rooted at path.
    
    Example:
        >>> count = _ex3_helper('/home/user/documents', {'txt', 'doc', 'pdf'})
        >>> print(count)  # Number of txt, doc, and pdf files in documents and subdirs
        42
    
    Note:
        - The function removes the leading dot from file extensions before comparing.
        - Files without extensions (no dot in filename) are ignored.
        - The search is performed recursively through all subdirectories.
    """
    count = 0
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            count += _ex3_helper(entry_path, extensions)
        else:
            _, ext = os.path.splitext(entry)
            if ext:
                ext = ext[1:]  # remove the dot
                if ext in extensions:
                    count += 1
    return count

def ex3(dirin, K, extensions):
    result = {}
    for root, dirs, files in os.walk(dirin):
        root_norm = root.replace(os.sep, '/')
        count = _ex3_helper(root, extensions)
        if count > K:
            result[root_norm] = count
    return result

# %% ----------------------------------- EX.4 ----------------------------------- #
'''
Ex4: 8 punti

Implementa la funzione ex4(root), ricorsiva o utilizzando funzioni ricorsive, 
che riceve l'argomento:  
    - root: la radice di un albero binario;
    
L'albero è composto da istanze della classe BinaryTree definita in tree.py. 
La funzione deve costruire e ritornare una lista, in mode che
ogni elemento alla posizione i-esima alla fine dovrà contenere la somma di tutti i nodi 
che si trovano alla profondità i (la radice dell'albero è alla profondità 0).

    Esempio:
                                                                        Profondità
        ______5______                        ______2______                   0
       |             |                      |             |
       8__        ___2___                __ 7__        ___5___               1
          |      |       |              |      |      |       |
          3      9       1             _4_     3_    _0_     _5_             2
                                      |   |      |  |   |   |   |
                                      2   -1     1  8   3   2   9            3

    Per l'albero di sinistra il risultato sarà [5, 10, 13]
    Per l'albero di destra   il risultato sarà [2, 12, 12, 24]
'''

from tree import BinaryTree

def _ex4_helper(node, depth, result):
    if node is None:
        return
    
    if depth >= len(result):
        result.append(0)
    
    result[depth] += node.value
    
    _ex4_helper(node.left, depth + 1, result)
    _ex4_helper(node.right, depth + 1, result)

def ex4(root):
    result = []
    _ex4_helper(root, 0, result)
    return result


######################################################################################

if __name__ == '__main__':
    # Puoi provare qui le tue implementazioni senza che interferiscano con il grader
    pass
