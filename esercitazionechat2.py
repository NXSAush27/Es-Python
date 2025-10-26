# Ignorare le righe fino alla 31
from typing import Any, Callable, List
import sys

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

def check_test(func: Callable, expected: Any, *args: List[Any]):
    func_str = func.__name__
    args_str = ', '.join(repr(arg) for arg in args)
    try:
        result = func(*args)
        result_str = repr(result)
        expected_str = repr(expected)
        test_outcome = "succeeded" if (result==expected) else "failed"
        color = bcolors.OKGREEN if (result==expected) else bcolors.FAIL
        print(f'{color}Test on {func_str} on input {args_str} {test_outcome}. Output: {result_str} Expected: {expected_str}')
    except BaseException as error:
        error_str = repr(error)
        print(f'{bcolors.FAIL}ERROR: {func_str}({args_str}) => {error_str}')

# ====================================================
# ESERCIZI LIVELLO AVANZATO
# ====================================================

# 1️⃣ Scrivere una funzione che data una lista di stringhe,
# restituisce un dizionario che mappa ciascuna parola
# alla sua lunghezza.
# Esempio: ["ciao", "a", "tutti"] -> {"ciao":4, "a":1, "tutti":5}
def word_lengths(words: list) -> dict:
    result = {}
    for word in words:
        result[word] = len(word)
    return result


# 2️⃣ Scrivere una funzione che riceve due liste e restituisce
# un insieme contenente solo gli elementi unici presenti
# in *entrambe* le liste.
# Esempio: [1, 2, 3], [2, 3, 4] -> {2, 3}
def common_elements(a: list, b: list) -> set:
    set_a = set(a)
    set_b = set(b)
    return set_a.intersection(set_b)


# 3️⃣ Scrivere una funzione che riceve un dizionario {nome: voto}
# e restituisce la media dei voti.
# Se il dizionario è vuoto, deve restituire 0.
# Gestire eventuali eccezioni (es. valori non numerici) ignorando i voti non validi.
def average_grades(grades: dict) -> float:
    if len(grades) == 0:
        return 0
    total = 0
    count = 0
    for grade in grades.values():
        try:
            total += float(grade)
            count += 1
        except:
            continue
    if count == 0:
        return 0
    return total / count


# 4️⃣ Scrivere una funzione che riceve una lista di numeri
# e restituisce una nuova lista contenente solo i numeri positivi
# moltiplicati per 2. Utilizzare *filter* e *map* o list conpreention.
def double_positive(nums: list) -> list:
    return [num*2 for num in nums if num > 0]


# 5️⃣ Scrivere una funzione che prende in input una lista di numeri
# e restituisce una funzione *lambda* che, data una soglia n,
# restituisce quanti numeri della lista sono maggiori di n.
# Esempio:
#   f = threshold_counter([1, 5, 10])
#   f(4) => 2   (perché 5 e 10 > 4)
def threshold_counter(nums: list) -> Callable:
    return lambda n: len([num for num in nums if num > n])


# ====================================================
# TEST
# ====================================================

check_test(word_lengths, {"ciao": 4, "a": 1, "tutti": 5}, ["ciao", "a", "tutti"])
check_test(word_lengths, {}, [])

check_test(common_elements, {2, 3}, [1, 2, 3], [2, 3, 4])
check_test(common_elements, set(), [1, 2], [3, 4])
check_test(common_elements, {1}, [1, 1, 1], [1])

check_test(average_grades, 26.0, {"Anna": 30, "Luca": 22, "Gianni": 26})
check_test(average_grades, 0, {})
check_test(average_grades, 25.0, {"A": 25, "B": "errore", "C": 25})

check_test(double_positive, [4, 6], [-1, 2, 3, 0])
check_test(double_positive, [], [-5, -3, 0])
check_test(double_positive, [10, 200], [5, 100])

f = threshold_counter([1, 5, 10])
check_test(lambda func: func(4), 2, f)
check_test(lambda func: func(10), 0, f)
check_test(lambda func: func(0), 3, f)
