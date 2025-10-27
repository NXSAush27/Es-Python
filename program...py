#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
################################################################################
################################################################################

""" Operazioni da fare PRIMA DI TUTTO:
 1) Assegnare le variabili sottostanti con il tuo
    NOME, COGNOME, NUMERO DI MATRICOLA

Per superare l'esame e' necessario:
    - ottenere un punteggio maggiore o uguale a 18

Il voto finale e' la somma dei punteggi dei problemi risolti.

Attenzione! DEBUG=True nel grade.py per migliorare il debugging.
"""

nome = 'Eric'
cognome = 'Bordeianu'
matricola = "2258456"


# %% --------------------------------- Func1 ------------------------- #
# func1: 7.5 punti
# Crea una funzione che formatta in una stringa lo stato di un tabellone del
# gioco "Battaglia Navale". Il tabellone è rappresentato da un dizionario
# `board`, dove ciascuna chiave è una tupla di coordinate (x, y), e ciascun
# valore è:
# - "S" se la cella contiene una nave,
# - "X" se il colpo ha colpito una nave,
# - "O" se il colpo ha mancato il bersaglio.
# Il parametro `side` indica la lunghezza del lato del tabellone. Assumi che
# le coordinate siano valide, ossia che nessuna sia esterna ad un tabellone
# quadrato di dimensione `side`x`side`.
# Separa le righe con un carattere a capo `\n` ed affianca alle celle in
# ogni colonna il carattere pipe `|`.
#
# Per esempio, per `board` = {(0, 0): "S", (1, 1): "X", (2, 9): "O"} e
# `side` = 10, l'output è la stringa:
#
#    "|S| | | | | | | | | |\n"
#    "| |X| | | | | | | | |\n"
#    "| | | | | | | | | |O|\n"
#    "| | | | | | | | | | |\n"
#    "| | | | | | | | | | |\n"
#    "| | | | | | | | | | |\n"
#    "| | | | | | | | | | |\n"
#    "| | | | | | | | | | |\n"
#    "| | | | | | | | | | |\n"
#    "| | | | | | | | | | |"

coordinate = tuple[int,int]

def func1(board : dict[coordinate, str], side : int) -> str :
    result = ""
    for i in range(side):
        row = "|"
        for j in range(side):
            if (i,j) in board:
                row += board[(i,j)] + "|"
            else:
                row += " |"
        result += row + "\n"
    return result

# test 
print(func1({(0, 0): "S", (1, 1): "X", (2, 9): "O"}, 10))


# %% --------------------------------- Func2 ------------------------- #
# func2: 7.5 punti
# Scrivi una funzione che estragga da una stringa di input la posizione di una
# o più navi. Il formato atteso della stringa in input è
# "nave1:posizione1:orientamento1,
# lunghezza1;nave2:posizione2:orientamento2:lunghezza2;...".
#
# Esempio di input: "Fregata:2,3:H:4;Fregata:3,3:H:4"
#
# Restituisci una lista di dizionari, dove ciascun dizionario corrisponde ai
# dati di una nave. La lista dev'essere ordinata lessicograficamente in maniera
# crescente a seconda del suo nome.
#
# Per esempio, la funzione chiamata sulla stringa precedente dovrebbe
# restituire: [{'nome': 'Fregata', 'posizione': '2, 3', 'orientamento': 'H',
# 'lunghezza': '4'}, {'nome': 'Fregata', 'posizione': '3, 3', 'orientamento':
# 'H', 'lunghezza': '4'}]
def func2(input_string : str) -> list[dict[str,str]] :
    lista_navi = input_string.split(";")
    result = []
    for nave in lista_navi:
        dati_nave = nave.split(":")
        nave_dict = {
            "name": dati_nave[0],
            "posizione": dati_nave[1],
            "orientamento": dati_nave[2],
            "lunghezza": dati_nave[3]
        }
        result.append(nave_dict)
    result.sort(key=lambda x: x["name"])
    return result
    
# test
for nave in func2("Fregata:2,3:H:4;Fregata:3,3:H:4"):
    print(nave)
    
# test edge case
for nave in func2("Torpediniere:5,5:V:2;Fregata:1,1:H:4;Cacciatorpediniere:0,0:V:5"):
    print(nave)

# %% --------------------------------- Func3 ------------------------- #
# func3: 7.5 punti
# Controlla che una lista di navi sia compatibile con le regole del gioco
# della Battaglia Navale. Le navi sono codificate come dizionari nel
# formato:
# {'nome': 'TipoNave', 'posizione': (x, y), 'orientamento': 'H',
# 'lunghezza': n}
#  Le regole prevedono che ciascun tabellone contenga le seguenti navi:
#     - 1x Fregata
#     - 2x Sottomarino
#     - 2x Torpediniere
#     - 1x Cacciatorpediniere
#     - 1x Portaerei
#
# La funzione restituisce True se la lista di navi è compatibile con le regole,
# False altrimenti.

from typing import Union

Nave = dict[str, Union[str,coordinate,int]]

def func3(lista_navi : list[Nave]) -> bool :
    counts = [0,0,0,0,0]
    for nave in lista_navi:
        if nave["nome"] not in ["Fregata", "Sottomarino", "Torpediniere", "Cacciatorpediniere", "Portaerei"]:
            return False
        if nave["nome"] == "Fregata":
            counts[0] += 1
        elif nave["nome"] == "Sottomarino":
            counts[1] += 1
        elif nave["nome"] == "Torpediniere":
            counts[2] += 1
        elif nave["nome"] == "Cacciatorpediniere":
            counts[3] += 1
        elif nave["nome"] == "Portaerei":
            counts[4] += 1
    return counts == [1,2,2,1,1]

# test
navi_test = [
    {"nome": "Fregata", "posizione": (0, 0), "orientamento": "H", "lunghezza": 4},
    {"nome": "Sottomarino", "posizione": (1, 0), "orientamento": "V", "lunghezza": 3},
    {"nome": "Sottomarino", "posizione": (2, 0), "orientamento": "V", "lunghezza": 3},
    {"nome": "Torpediniere", "posizione": (3, 0), "orientamento": "H", "lunghezza": 2},
    {"nome": "Torpediniere", "posizione": (4, 0), "orientamento": "H", "lunghezza": 2},
    {"nome": "Cacciatorpediniere", "posizione": (5, 0), "orientamento": "V", "lunghezza": 5},
    {"nome": "Portaerei", "posizione": (6, 0), "orientamento": "H", "lunghezza": 5}
]
print(func3(navi_test))  # Output: True

# test false
navi_test_false = [
    {"nome": "Fregata", "posizione": (0, 0), "orientamento": "H", "lunghezza": 4},
    {"nome": "Sottomarino", "posizione": (1, 0), "orientamento": "V", "lunghezza": 3},
    {"nome": "Sottomarino", "posizione": (2, 0), "orientamento": "V", "lunghezza": 3},
    {"nome": "Torpediniere", "posizione": (3, 0), "orientamento": "H", "lunghezza": 2},
    {"nome": "Cacciatorpediniere", "posizione": (5, 0), "orientamento": "V", "lunghezza": 5},
    {"nome": "Portaerei", "posizione": (6, 0), "orientamento": "H", "lunghezza": 5}
]
print(func3(navi_test_false))  # Output: False

# %% --------------------------------- func4 ------------------------- #
# func4: 7.5 punti
# Definisci una funzione che riceva come input una lista di navi, ciascuna
# rappresentata con un dizionario. La `posizione` di una nave indica la sua
# coordinata in alto a sinistra, l'`orientamento` se è disposta in verticale (
# "V") od orizzontale ("H"), e la `lunghezza` quante celle occupa.
#
# Per esempio, la nave {"nome": "Sottomarino", "posizione": (1, 1),
#                      "orientamento": "V", "lunghezza": 3}
# occupa le posizioni (1, 1), (2, 1), (3, 1).
#
# Restituisci il set delle posizioni in cui le navi si sovrappongono.
#
# Esempio di input: [{"nome": "Sottomarino", "posizione": (1, 1),
#                     "orientamento": "V", "lunghezza": 3},
#                    {"nome": "Fregata", "posizione": (0, 1), "orientamento":
#                    "V", "lunghezza": 3}]
# Output: {(1, 1), (2, 1)}
def func4(lista_navi : list[Nave]) -> set[coordinate]:        
    occupate = []
    sovrapposte = set()
    for nave in lista_navi:
        x,y = nave["posizione"]
        for i in range(nave["lunghezza"]):
            if nave["orientamento"] == "H":
                pos = (x, y + i)
            else:
                pos = (x + i, y)
            if pos in occupate and pos not in sovrapposte:
                sovrapposte.add(pos)
            else:
                occupate.append(pos)
    return sovrapposte

# test
navi_test = [
    {"nome": "Sottomarino", "posizione": (1, 1), "orientamento": "V", "lunghezza": 3},
    {"nome": "Fregata", "posizione": (0, 1), "orientamento": "V", "lunghezza": 3}
]
print(func4(navi_test))  # Output: {(1, 1), (2, 1)}

# test no overlap
navi_test_no_overlap = [
    {"nome": "Sottomarino", "posizione": (1, 1), "orientamento": "V", "lunghezza": 3},
    {"nome": "Fregata", "posizione": (0, 3), "orientamento": "V", "lunghezza": 3}
]
print(func4(navi_test_no_overlap))  # Output: set()
