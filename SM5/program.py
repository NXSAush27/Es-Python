#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
################################################################################
################################################################################

""" Operazioni da fare PRIMA DI TUTTO:
 1) Salvare questo file col nome program.py
 2) Assegnare le variabili sottostanti con il tuo
      NOME, COGNOME, NUMERO DI MATRICOLA

Per superare la prova è necessario:
    - !!!riempire le informazioni personali nelle variabili qui sotto!!!
    - AND ottenere un punteggio maggiore o uguale a 18 (o 15 se DSA)

Il punteggio finale della prova è la somma dei punteggi dei problemi risolti.
Per i DSA il punteggio viene scalato opportunamente (32*X/26).
"""
nome       = "Eric"
cognome    = "Bordeianu"
matricola  = "2258456"

################################################################################
################################################################################
################################################################################
# ------------------------ SUGGERIMENTI PER IL DEBUG --------------------------- #
# Per eseguire solo alcuni dei test, puoi commentare le righe della lista
# 'tests' alla fine di grade.py
#
# Per facilitare il debug delle funzioni ricorsive, puoi disattivare
# il test ricorsivo impostando DEBUG=True nel file grade.py
#
# DEBUG=True attiva anche il TRACE DELLO STACK che ti permette di sapere quale
# numero di riga in program.py ha generato l'errore.
################################################################################

# Helper function to automatically handle file paths
import os

def get_correct_path(relative_path):
    """
    Automatically detects and adjusts file paths to work from any location.
    
    This function checks if the given relative path exists from the current working directory.
    If not, it tries the SM5 subdirectory and adjusts the path accordingly.
    
    Args:
        relative_path (str): The relative path to adjust
        
    Returns:
        str: The correct absolute path that works from any directory
    """
    # If the path already exists from current directory, use it as-is
    if os.path.exists(relative_path):
        return relative_path
    
    # If the file doesn't exist, try with SM5 prefix
    sm5_path = os.path.join('SM5', relative_path)
    if os.path.exists(sm5_path):
        return sm5_path
    
    # If still not found, return the original path (will raise an error when trying to use it)
    return relative_path

# %% ----------------------------------- FUNC.1 ----------------------------------- #
"""
Func 1: 2 punti

Implementa la funzione func1(testo : str, K : int) -> set[str] 
che riceve come argomenti:
- testo: una stringa contenente parole separate da caratteri non alfabetici
- K: un intero
e che ritorna l'insieme delle parole che appaiono esattamente K volte nel testo.

Esempio:
K = 2
testo = '''sopra la panca la capra camps, sotto la panca la capra crepa!'''
expected = {'capra', 'panca'}

"""
import re
def func1(testo : str, K : int) -> set[str]:
    # Rimuovi la punteggiatura e dividi in parole
    parole = re.findall(r'\b[a-zA-Z]+\b', testo.lower())
    
    # Conta le occorrenze di ogni parola
    from collections import Counter
    contatore = Counter(parole)
    
    # Ritorna le parole che appaiono esattamente K volte
    return {parola for parola, count in contatore.items() if count == K}


# %% ----------------------------------- FUNC.2 ----------------------------------- #
"""
Func 2: 2 punti

Implementa la funzione   func2(parole : list[str]) -> dict[str, list[str]]
che riceve come argomenti:
    - parole: una lista di parole
e che ritorna un dizionario che ha come chiavi le lettere iniziali delle parole,
e come valori la lista della parole che hanno quella iniziale, 
ordinate per lunghezza crescente e in caso parità in ordine alfabetico decrescente.

Esempio:
parole = ['sei','sicuro','che','sopra','la','panca','le','capre','campino?',
          'certamente,','mentre','sotto','la','panca','le','capre','crepano!']
expected = {'s': ['sei', 'sotto', 'sopra', 'sicuro'], 
            'c': ['che', 'capre', 'capre', 'crepano!', 'campino?', 'certamente,'], 
            'l': ['le', 'le', 'la', 'la'], 
            'p': ['panca', 'panca'], 
            'm': ['mentre']}
"""
def func2(parole : list[str]) -> dict[str, list[str]]:
    risultato = {}
    
    for parola in parole:
        iniziale = parola[0].lower()
        if iniziale not in risultato:
            risultato[iniziale] = []
        risultato[iniziale].append(parola)
    
    # Ordina ogni lista per lunghezza crescente e in caso di parità per ordine alfabetico decrescente
    for chiave in risultato:
        risultato[chiave].sort(key=lambda x: (len(x), -ord(x[0]) if x else 0))
    
    return risultato



# %% ----------------------------------- FUNC.3 ----------------------------------- #
"""
Func 3: 2 punti

Implementa la funzione    func3(D1 : dict[str,list[int]], D2 : dict[int,list[str]]) -> dict[str, list[str]] 
che riceve come argomenti:
    - D1: un dizionario che ha come chiavi delle parole e come valori liste di interi DIVERSI tra loro
    - D2: un dizionario che ha come chiavi degli interi e come valori liste di parole
e che ritorna un dizionario che ha come chiavi delle parole e come valori liste di parole.
Le chiavi sono le sole chiavi di D1 che hanno almeno uno degli interi ad esse associati che è una chiave di D2.
Tutte le parole associate in D2 a tali interi devono apparire nella lista associata a quella chiave nel risultato.
L'ordinamento delle parole nei valori del risultato è per dimensioni decrescenti 
e in caso di parità in ordine alfabetico crescente.

Esempio:
D1 = { 'a':[1,2,3], 'b':[3,4,5] }
D2 = { 1:['a','bb','ccc'], 3:['qq','z'], 5:['b','fff'] }
expected = {'a': ['a', 'z', 'bb', 'qq', 'ccc'], 'b': ['b', 'z', 'qq', 'fff']}
"""
def func3(D1 : dict[str,list[int]], D2 : dict[int,list[str]]) -> dict[str, list[str]]:
    risultato = {}
    
    for parola, numeri in D1.items():
        # Trova i numeri che sono chiavi in D2
        numeri_comuni = [n for n in numeri if n in D2]
        
        if numeri_comuni:
            # Raccogli tutte le parole associate a questi numeri
            parole_raccolte = []
            for num in numeri_comuni:
                parole_raccolte.extend(D2[num])
            
            # Rimuovi duplicati mantenendo l'ordine
            parole_uniche = list(dict.fromkeys(parole_raccolte))
            
            # Ordina per lunghezza decrescente e poi alfabeticamente crescente
            parole_uniche.sort(key=lambda x: (-len(x), x))
            
            risultato[parola] = parole_uniche
    
    return risultato


# %% ----------------------------------- FUNC.4 ----------------------------------- #
"""
Func 4: 6 punti

Implementa la funzione    func4(path_in : str, path_out : str, K : int) -> dict[str, list[int]]
che riceve come argomenti:
    - path_in:  un percorso ad un file di testo da leggere
    - path_out: un percorso ad un file di testo da scrivere
    - K: un intero
La funzione deve leggere il file di testo al percorso path_in
e ritornare un dizionario che ha come chiavi le parole presenti nel file almeno K volte
e come valori le liste degli interi che rappresentano il numero della riga in cui appare la parola.

Successivamente la funzione deve scrivere su file path_out su ogni riga 
la parola ed il numero di righe in cui essa appare, separati da spazio.
Le righe del file path_out devono essere ordinate 
- per numero di righe in cui sono apparse le parole in ordine decrescente 
- e in caso di parità in ordine alfabetico crescente.

Esempio:
path_in = 'func4/in_1.txt'
path_out = 'func4/out_1.txt'
k = 2
Il file in_1.txt contiene:
    a b c b a a
    aa ba ca aa ba ca
    a b
    aa b
Il file out_1.txt conterrà:
    b 3
    a 2
    aa 2
e la funzione restituirà:
    {'a': [0, 2], 'b': [0, 2, 3], 'aa': [1, 3]}
"""
import re
from collections import defaultdict

def func4(path_in : str, path_out : str, K : int) -> dict[str, list[int]]:
    # Use the helper function to get the correct path
    correct_path_in = get_correct_path(path_in)
    correct_path_out = get_correct_path(path_out)
    
    # Leggi il file
    with open(correct_path_in, 'r') as f:
        righe = f.readlines()
    
    # Dizionario per memorizzare le righe in cui appare ogni parola
    parole_righe = defaultdict(list)
    
    for num_riga, riga in enumerate(righe):
        # Estrai solo le parole (caratteri alfabetici)
        parole = re.findall(r'\b[a-zA-Z]+\b', riga.lower())
        
        # Aggiungi il numero di riga per ogni parola unica in quella riga
        parole_uniche = set(parole)
        for parola in parole_uniche:
            parole_righe[parola].append(num_riga)
    
    # Filtra le parole che appaiono almeno K volte
    risultato = {parola: righe for parola, righe in parole_righe.items() if len(righe) >= K}
    
    # Scrivi il file di output
    with open(correct_path_out, 'w') as f:
        # Ordina per numero di righe decrescente, poi alfabeticamente
        parole_ordinate = sorted(risultato.items(), key=lambda x: (-len(x[1]), x[0]))
        
        for parola, righe in parole_ordinate:
            f.write(f"{parola} {len(righe)}\n")
    
    return risultato


# %% ----------------------------------- FUNC.5 ----------------------------------- #
"""
Func 5: 8 punti

Implementa la funzione      func5(path_png_in : str) -> dict[str, set[tuple[int,int]]]
che riceve come argomenti:
    - path_png_in:  un percorso ad un file PNG da leggere
Il file PNG path_png_in contiene un'immagine a sfondo nero con dei quadretti colorati di varie dimensioni.

ASSUMETE che nessuno dei quadrati si appoggi sul bordo della immagine o tocchi un altro quadrato.

La funzione deve leggere il file PNG al percorso path_png_in e cercare tutte le posizioni
in cui compare un quadrato 2x2 di pixel tutti dello stesso colore.
(si intende la posizione x,y del pixel in alto a sinistra del quadrato 2x2)
La funzione deve ritornare come risultato un dizionario che ha come chiavi i colori dei quadrati 2x2
e come valori l'insieme delle posizioni dei quadrati 2x2 di quel colore.

Esempio:
path_png_in = 'func5/in_1.png'
expected = {'a': [0, 2], 'b': [0, 2, 3], 'aa': [1, 3]}
"""
import images

def func5(path_png_in : str) -> dict[tuple[int,int,int], set[tuple[int,int]]]:
    # Use the helper function to get the correct path
    correct_path_png_in = get_correct_path(path_png_in)
    
    # Carica l'immagine
    img = images.load(correct_path_png_in)
    altezza = len(img)
    larghezza = len(img[0]) if altezza > 0 else 0
    
    # Dizionario per memorizzare le posizioni per ogni colore
    risultato = {}
    
    # Scorri tutti i possibili quadrati 2x2
    for y in range(altezza - 1):
        for x in range(larghezza - 1):
            # Ottieni i 4 pixel del quadrato
            colore1 = img[y][x]
            colore2 = img[y][x + 1]
            colore3 = img[y + 1][x]
            colore4 = img[y + 1][x + 1]
            
            # Controlla se tutti e 4 i pixel hanno lo stesso colore
            if colore1 == colore2 == colore3 == colore4:
                # Converti il colore in una rappresentazione hashable (tupla)
                if isinstance(colore1, (list, tuple)) and len(colore1) >= 3:
                    colore_chiave = tuple(colore1[:3])  # Prendi solo RGB
                else:
                    colore_chiave = colore1
                
                # Aggiungi la posizione al risultato
                if colore_chiave not in risultato:
                    risultato[colore_chiave] = set()
                risultato[colore_chiave].add((x, y))
    
    return risultato


# %% ----------------------------------- EX.1 ----------------------------------- #
"""
Ex 1: 6 punti

Implementa la funzione    ex1(radice : tree.BinaryTree, lista_pesi:list[int]) -> tree.BinaryTree
che riceve come argomento:
- radice: un albero binario formato da nodi tree.BinaryTree
- lista_pesi: una lista di interi
e che da esso costruisce ricorsivamente o usando funzioni o metodi ricorsivi
un secondo albero binario che ha la stessa struttura del primo con i valori dei nodi moltiplicati 
ciascuno per l'n-esimo valore di lista_pesi, dove n è la profondità del nodo nell'albero
(considerando la radice a profondità 0).

ATTENZIONE: l'albero originale deve rimanere inalterato.

Esempio:
Se l'albero in input è:
   ___1___
   |     |
 __2__   3___         
 |   |      |
 4   5      6
e lista_pesi = [2,7,3,1]
l'albero in output sarà:
   ___2___
   |     |
 __14_   21__
 |   |      |
12   15    18
"""
import tree

def ex1(radice : tree.BinaryTree, lista_pesi:list[int]) -> tree.BinaryTree:
    def costruisci_albero(nodo, profondita):
        if nodo is None:
            return None
        
        # Calcola il nuovo valore per questo nodo
        peso = lista_pesi[profondita] if profondita < len(lista_pesi) else 1
        nuovo_valore = nodo.value * peso
        
        # Crea il nuovo nodo
        nuovo_nodo = tree.BinaryTree(nuovo_valore)
        
        # Costruisci ricorsivamente i figli
        nuovo_nodo.left = costruisci_albero(nodo.left, profondita + 1)
        nuovo_nodo.right = costruisci_albero(nodo.right, profondita + 1)
        
        return nuovo_nodo
    
    return costruisci_albero(radice, 0)


# %% ----------------------------------- EX.2 ----------------------------------- #
"""
Ex 2: 6 punti

Implementa la funzione    ex2(path : str, lista_estensioni : list[str]) -> dict[str, set[str]]
che riceve come argomento:
- path: il path di una directory
- lista_estensioni: una lista di estensioni di file (stringhe)
e che esplora ricorsivamente o usando funzioni o metodi ricorsivi la directory path
e tutte le sue sottodirectory e ritorna un dizionario che ha come chiavi le estensioni
e come valori l'insieme delle directory che contengono quel tipo di file.

ATTENZIONE: è proibito usare la funzione os.walk
NOTA: potete usare le funzioni os.listdir, os.path.isdir, os.path.isfile ...
NOTA: usate il carattere '/' per separare i path, che funziona sia su Windows che Linux

Esempio:
    directory  = 'ex2/A'
    extensions = ["txt", "pdf", "png", "gif"]
    expected   = {'txt': {'ex2/A/C', 'ex2/A', 'ex2/A/B'}, 'pdf': {'ex2/A/C', 'ex2/A'}, 'png': {'ex2/A/C'}, 'gif': {'ex2/A/C'}}
"""
import os

def ex2(path : str, lista_estensioni : list[str]) -> dict[str, set[str]]:
    # Use the helper function to get the correct path for directory exploration
    correct_path = get_correct_path(path)
    
    # Inizializza il risultato
    risultato = {est: set() for est in lista_estensioni}
    
    # Simple logic: if corrected path contains SM5, we need to strip it
    needs_strip = 'SM5' in correct_path and 'SM5' not in path
    
    def esplora_directory(dir_path):
        try:
            # Lista tutti i file e directory nella directory corrente
            elementi = os.listdir(dir_path)
            
            # Processa ogni elemento
            for elemento in elementi:
                elemento_path = os.path.join(dir_path, elemento)
                
                if os.path.isfile(elemento_path):
                    # È un file, controlla l'estensione
                    if '.' in elemento:
                        estensione = elemento.split('.')[-1].lower()
                        if estensione in lista_estensioni:
                            # Calculate the path to return
                            return_path = dir_path
                            if needs_strip:
                                # Remove SM5 prefix and normalize
                                if 'SM5' in dir_path:
                                    return_path = dir_path.replace('\\', '/')
                                    # Remove SM5 prefix and leading slash
                                    if return_path.startswith('SM5/'):
                                        return_path = return_path[4:]
                                    elif '/SM5/' in return_path:
                                        return_path = return_path.replace('/SM5/', '/')
                                    # Remove leading slash if any
                                    if return_path.startswith('/'):
                                        return_path = return_path[1:]
                            
                            # Normalizza il path per usare forward slash
                            normalized_path = return_path.replace('\\', '/')
                            # Aggiungi la directory corrente al risultato per questa estensione
                            risultato[estensione].add(normalized_path)
                
                elif os.path.isdir(elemento_path):
                    # È una directory, esplora ricorsivamente
                    esplora_directory(elemento_path)
        
        except (PermissionError, OSError):
            # Ignora errori di permessi o altri errori del sistema
            pass
    
    # Avvia l'esplorazione dalla directory iniziale
    esplora_directory(correct_path)
    
    return risultato


######################################################################################

if __name__ == '__main__':
    # Scrivi qui i tuoi test addizionali, attenzione a non sovrascrivere
    # gli EXPECTED!
    print('*' * 50)
    print('ITA\nDevi eseguire il grade.py se vuoi debuggare con il grader incorporato.')
    print(
        'Altrimenii puoi inserire qui del codice per testare le tue funzioni ma devi scriverti i casi che vuoi testare')
    print('*' * 50)
