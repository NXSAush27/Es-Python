# Esercizi di programmazione con matrici e elaborazione di immagini
# Ignorare le righe fino alla 31
from typing import Any, Callable, List, Tuple, Dict, Union
import sys
from unittest import result
import images

# Classe per gestire i colori del terminale per output formattato
class bcolors:
    HEADER = '\033[95m'      # Colore magenta per intestazioni
    OKBLUE = '\033[94m'      # Colore blu per informazioni
    OKCYAN = '\033[96m'      # Colore ciano
    OKGREEN = '\033[92m'     # Colore verde per successi
    WARNING = '\033[93m'     # Colore giallo per avvertimenti
    FAIL = '\033[91m'        # Colore rosso per errori
    ENDC = '\033[0m'         # Reset colore
    BOLD = '\033[1m'         # Testo in grassetto
    UNDERLINE = '\033[4m'    # Testo sottolineato

# Funzione per eseguire test automatizzati e controllare i risultati
def check_test(func: Callable, expected: Any, *args: List[Any]):
    """
    Esegue un test su una funzione e confronta il risultato con il valore atteso.
    
    Args:
        func: Funzione da testare
        expected: Valore atteso dal test
        *args: Argomenti da passare alla funzione
    """
    func_str = func.__name__  # Nome della funzione da testare
    args_str = ', '.join(repr(arg) for arg in args)  # Rappresentazione stringa degli argomenti
    try:
        result = func(*args)  # Esegue la funzione con gli argomenti forniti
        result_str = repr(result)  # Rappresentazione stringa del risultato
        expected_str = repr(expected)  # Rappresentazione stringa del valore atteso
        test_outcome = "succeeded" if (result == expected) else "failed"  # Determina l'esito del test
        color = bcolors.OKGREEN if (result == expected) else bcolors.FAIL  # Colore per il risultato
        # Stampa il risultato del test con colori formattati
        print(f'{color}Test on {func_str} on input {args_str} {test_outcome}. Output: {result_str} Expected: {expected_str}')
    except BaseException as error:
        error_str = repr(error)  # Rappresentazione stringa dell'errore
        print(f'{bcolors.FAIL}ERROR: {func_str}({args_str}) => {error_str}')  # Stampa l'errore


# FUNZIONI PER OPERAZIONI SU MATRICI

# Funzione per calcolare la matrice trasposta
# Scambia righe e colonne della matrice originale
def transpose(m: List[List[int]]) -> List[List[int]]:
    """
    Calcola la trasposta di una matrice di interi.
    
    Args:
        m: Matrice di input come lista di liste di interi
        
    Returns:
        Matrice trasposta (righe e colonne invertite)
        
    Example:
        [[5, 2], [3, 1]] -> [[5, 3], [2, 1]]
    """
    # Crea una matrice risultante con dimensioni invertite (righe=colonne originali, colonne=righe originali)
    result = [[0 for _ in range(len(m))] for _ in range(len(m[0]))]
    # Copia gli elementi dalla matrice originale a quella trasposta
    for i in range(len(m)):
        for j in range(len(m[0])):
            result[j][i] = m[i][j]  # L'elemento alla posizione [i][j] va in posizione [j][i]
    return result

# Funzione per sommare due matrici elemento per elemento
def matrix_matrix_sum(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Somma due matrici elemento per elemento.
    
    Args:
        A: Prima matrice
        B: Seconda matrice
        
    Returns:
        Matrice somma se le dimensioni sono compatibili, altrimenti None
        
    Example:
        [[1, 0], [2, 1]] + [[1, 2], [2, 3]] = [[2, 2], [4, 4]]
    """
    # Controlla se le matrici hanno le stesse dimensioni
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return None  # Restituisce None se le dimensioni non sono compatibili
    # Crea una matrice risultante della stessa dimensione delle matrici di input
    result = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
    # Somma elemento per elemento
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j] + B[i][j]
    return result

# Funzione per moltiplicare due matrici
def matrix_matrix_mul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Moltiplica due matrici secondo la regola standard del prodotto matriciale.
    
    Args:
        A: Prima matrice (m x n)
        B: Seconda matrice (n x p)
        
    Returns:
        Matrice prodotto (m x p) se le dimensioni sono compatibili, altrimenti None
        
    Note:
        Il numero di colonne di A deve essere uguale al numero di righe di B
        Elemento [i][j] della matrice risultante = somma_k (A[i][k] * B[k][j])
    """
    # Controlla se le matrici sono compatibili per la moltiplicazione
    if len(A[0]) != len(B):
        return None  # Restituisce None se le dimensioni non sono compatibili
    # Crea una matrice risultante (righe di A x colonne di B)
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    # Algoritmo di moltiplicazione matriciale standard
    for i in range(len(A)):  # Per ogni riga di A
        for j in range(len(B[0])):  # Per ogni colonna di B
            for k in range(len(B)):  # Per ogni elemento da sommare
                result[i][j] += A[i][k] * B[k][j]  # Aggiunge il prodotto degli elementi
    return result

# FUNZIONI PER ELABORAZIONE DI IMMAGINI

def img_rotate_right_and_flip_v(img_in: str, img_out: str):
    """
    Ruota un'immagine di 90 gradi in senso orario e la specchia verticalmente.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        img_out: Nome del file di output dove salvare l'immagine elaborata
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    # Ruota di 90 gradi a destra (senso orario)
    rotated = [[img[len(img)-1-j][i] for j in range(len(img))] for i in range(len(img[0]))]
    # Inverte rispetto all'asse orizzontale (specchio verticalmente)
    flipped = [rotated[len(rotated)-1-i] for i in range(len(rotated))]
    images.visd_matplotlib(flipped, img_out)  # Salva l'immagine elaborata
    return

def img_invert_channels(img_in: str, img_out: str):
    """
    Inverte i canali rosso e blu di un'immagine.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        img_out: Nome del file di output dove salvare l'immagine elaborata
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    # Inverte i canali RGB: (R, G, B) -> (B, G, R)
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j] = (img[i][j][2], img[i][j][1], img[i][j][0])  # Scambia R e B
    images.visd_matplotlib(img, img_out)  # Salva l'immagine elaborata


def img_solo_blu(img_in: str, img_out: str):
    """
    Inverte i canali rosso e blu di un'immagine.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        img_out: Nome del file di output dove salvare l'immagine elaborata
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    # Inverte i canali RGB: (R, G, B) -> (B, G, R)
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j] = (0, 0, img[i][j][2])  # Scambia R e B
    images.visd_matplotlib(img, img_out)  # Salva l'immagine elaborata

def img_quantize(img_in: str, img_out: str):
    """
    Quantizza ogni canale dell'immagine su 128 valori invece di 256.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        img_out: Nome del file di output dove salvare l'immagine elaborata
        
    Note:
        Riduce la risoluzione di colore dividendo ogni valore per 2
        Esempio: (21, 126, 3) -> (10, 63, 2)
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    # Quantizza ogni canale RGB dividendo per 2 (256 valori -> 128 valori)
    for i in range(len(img)):
        for j in range(len(img[0])):
            r = img[i][j][0] // 2  # Quantizza canale rosso
            g = img[i][j][1] // 2  # Quantizza canale verde
            b = img[i][j][2] // 2  # Quantizza canale blu
            img[i][j] = (r, g, b)  # Assegna i valori quantizzati
    images.visd_matplotlib(img, img_out)  # Salva l'immagine elaborata

def img_quantize_up(img_in: str, img_out: str):
    """
    Quantizza ogni canale dell'immagine su 128 valori invece di 256.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        img_out: Nome del file di output dove salvare l'immagine elaborata
        
    Note:
        Riduce la risoluzione di colore dividendo ogni valore per 2
        Esempio: (21, 126, 3) -> (10, 63, 2)
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    # Quantizza ogni canale RGB dividendo per 2 (256 valori -> 128 valori)
    for i in range(len(img)):
        for j in range(len(img[0])):
            r = img[i][j][0] * 2  # Quantizza canale rosso
            g = img[i][j][1] * 2  # Quantizza canale verde
            b = img[i][j][2] * 2  # Quantizza canale blu
            img[i][j] = (min(r, 255), min(g, 255), min(b, 255))  # Assegna i valori quantizzati
    images.visd_matplotlib(img, img_out)  # Salva l'immagine elaborata


def img_invert_half(img_in: str, img_out: str):
    """
    Scambia la metà sinistra dell'immagine con la metà destra.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        img_out: Nome del file di output dove salvare l'immagine elaborata
        
    Note:
        Assume che la larghezza dell'immagine sia divisibile per 2
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    mid = len(img[0]) // 2  # Calcola il punto medio orizzontale
    # Scambia le colonne della metà sinistra con quelle della metà destra
    for i in range(len(img)):  # Per ogni riga
        for j in range(mid):  # Per ogni colonna della metà sinistra
            img[i][j], img[i][j + mid] = img[i][j + mid], img[i][j]  # Scambia gli elementi
    images.visd_matplotlib(img, img_out)  # Salva l'immagine elaborata

# SEZIONE DI TEST AUTOMATIZZATI

# Test della funzione transpose con diversi input
check_test(transpose, [[5, 3], [2, 1]], [[5, 2], [3, 1]])  # Test matrice 2x2
check_test(transpose, [[5, 3], [2, 1], [9, 0]], [[5, 2, 9], [3, 1, 0]])  # Test matrice 2x3
check_test(transpose, [[5, 3]], [[5], [3]])  # Test matrice colonna 2x1
check_test(transpose, [[5], [3]], [[5, 3]])  # Test matrice riga 1x2

# Test della funzione matrix_matrix_sum con diversi scenari
check_test(matrix_matrix_sum, [[2, 2, 2], [4, 4, 2], [4, 3, 3], [2, 3, 5]],
           [[1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 1, 2]], [[1, 2, 1], [2, 3, 1], [4, 2, 2], [1, 2, 3]])  # Somma valida
check_test(matrix_matrix_sum, None, [[1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 1, 2]], [[1, 2], [2, 3], [4, 2], [1, 2]])  # Dimensioni incompatibili
check_test(matrix_matrix_sum, None, [[1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 1, 2]], [[1, 2, 1], [2, 3, 1], [4, 2, 2]])  # Numero righe diverse

# Test della funzione matrix_matrix_mul con diversi scenari
check_test(matrix_matrix_mul, [[5, 4, 3], [8, 9, 5], [6, 5, 3], [11, 9, 6]],
           [[1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 1, 2]], [[1, 2, 1], [2, 3, 1], [4, 2, 2]])  # Moltiplicazione valida 4x3 x 3x3
check_test(matrix_matrix_mul, [[5], [8], [6], [11]],
           [[1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 1, 2]], [[1], [2], [4]])  # Moltiplicazione valida 4x3 x 3x1
check_test(matrix_matrix_mul, None, [[1, 0, 1], [2, 1, 1], [0, 1, 1], [1, 1, 2]], [[1, 2, 1], [2, 3, 1]])  # Dimensioni incompatibili

# Test delle funzioni di elaborazione immagini
# Generano file PNG elaborati per verifica visiva (non test automatici)
#img_solo_blu("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_solo_blu.png")  # Test canale blu
#img_rotate_right_and_flip_v("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_rotate_flip.png")  # Test rotazione + flip
#img_invert_channels("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_invert_channels.png")  # Test inversione canali RGB
#img_quantize_up("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_quantized_up.png")  # Test quantizzazione in su
#img_quantize("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_quantized.png")  # Test quantizzazione
img_invert_half("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_inverted_half.png")  # Test inversione metà immagine