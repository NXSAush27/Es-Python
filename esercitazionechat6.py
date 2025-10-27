# Ignorare le righe fino alla 31

from typing import Any, Callable, List
import sys
from functools import reduce

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Esegue un test e controlla il risultato
def check_test(func: Callable, expected: Any, *args: List[Any]):
    func_str = func.__name__
    args_str = ', '.join(repr(arg) for arg in args)
    try:
        result = func(*args)
        result_str = repr(result)
        expected_str = repr(expected)
        test_outcome = "succeeded" if (result == expected) else "failed"
        color = bcolors.OKGREEN if (result == expected) else bcolors.FAIL
        print(f'{color}Test on {func_str}({args_str}) {test_outcome}. Output: {result_str} Expected: {expected_str}{bcolors.ENDC}')
    except BaseException as error:
        error_str = repr(error)
        print(f'{bcolors.FAIL}ERROR: {func_str}({args_str}) => {error_str}{bcolors.ENDC}')


# ===============================================
# NUOVI ESERCIZI DI RIPASSO (lambda e list comprehension)
# ===============================================

# 1️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce una nuova lista contenente i cubi dei numeri dispari.

def cube_odds(a: list) -> list:
    return [num**3 for num in a if num%2]


# 2️⃣ Scrivere una funzione che, data una lista di stringhe,
# restituisce una lista contenente solo le stringhe
# che contengono almeno una lettera maiuscola.

def has_uppercase(a: list) -> list:
    return [word for word in a if any(char.isupper() for char in word)]


# 3️⃣ Scrivere una funzione che calcola la media
# dei numeri pari presenti nella lista.

def avg_even(a: list) -> float:
    even = [num for num in a if num % 2 == 0]
    return (sum(even)/len(even))


# 4️⃣ Scrivere una funzione che prende in input una lista di tuple (x, y)
# e restituisce una nuova lista contenente x*y solo per le tuple dove y è pari.

def multiply_if_even(a: list) -> list:
    y_even = [tup for tup in a if tup[1] % 2 == 0]
    return [nums[0] * nums[1] for nums in y_even]


# 5️⃣ Scrivere una funzione che restituisce un dizionario
# che associa a ciascuna parola la sua lunghezza.

def word_length_dict(words: list) -> dict:
    result = {}
    for word in words:
        result[word] = len(word)
    return result


# 6️⃣ Scrivere una funzione che verifica se tutti i numeri
# in una lista sono multipli di 3.

def all_multiple_of_three(a: list) -> bool:
    for num in a:
        if num % 3:
            return False
    return True


# 7️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce una nuova lista in cui ciascun elemento
# è il valore assoluto del corrispondente elemento della lista originale.

def abs_list(a: list) -> list:
    return [abs(num) for num in a]


# 8️⃣ Scrivere una funzione che, data una lista di stringhe,
# restituisce una lista con le stringhe che terminano con una vocale.

def ends_with_vowel(a: list) -> list:
    vocali = "aeiou"
    return [word for word in a if word[len(word)-1].lower() in vocali]


# 9️⃣ Scrivere una funzione che restituisce True
# se almeno un numero nella lista è negativo e dispari.

def has_negative_odd(a: list) -> bool:
    for num in a:
        if num <0 and abs(num) % 2: # è dispari e negativo
            return True
    return False


# 🔟 Scrivere una funzione che, data una lista di interi,
# restituisce una lista con i numeri maggiori di 10 divisi per 2.

def half_above_10(a: list) -> list:
    return [num/2 for num in a if num > 10]


# ===============================================
# TEST
# ===============================================

check_test(cube_odds, [1, 27, 125], [1, 2, 3, 4, 5])
check_test(has_uppercase, ['Ciao', 'Python'], ['ciao', 'Ciao', 'python', 'Python'])
check_test(avg_even, 5.0, [2, 4, 6, 8, 9])
check_test(multiply_if_even, [4, 18], [(2, 2), (3, 5), (6, 3), (9, 2)])
check_test(word_length_dict, {'ciao': 4, 'python': 6}, ['ciao', 'python'])
check_test(all_multiple_of_three, True, [3, 6, 9])
check_test(all_multiple_of_three, False, [3, 4, 9])
check_test(abs_list, [1, 2, 3], [-1, -2, 3])
check_test(ends_with_vowel, ['mare', 'vento', 'sole'], ['mare', 'vento', 'sole', 'mont'])
check_test(has_negative_odd, True, [2, -3, 4])
check_test(has_negative_odd, False, [2, -4, 8])
check_test(half_above_10, [6.5, 7.0, 10.0], [5, 13, 14, 20])
