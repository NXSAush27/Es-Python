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


# 1️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce una nuova lista con ciascun numero elevato al quadrato
# usando una list comprehension.
def squares(nums: list) -> list:
    return [num**2 for num in nums]


# 2️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce una nuova lista contenente solo i numeri pari,
# usando filter() e una lambda function.
def even_numbers(nums: list) -> list:
    return list(filter(lambda x: x%2 == 0, nums))


# 3️⃣ Scrivere una funzione che, data una lista di stringhe,
# restituisce una nuova lista con la lunghezza di ciascuna stringa,
# usando map() e una lambda function.
def lengths(words: list) -> list:
    return list(map(lambda x: len(x), words))


# 4️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce la somma di tutti gli elementi
# usando reduce() e una lambda function.
def total_sum(nums: list) -> int:
    return reduce(lambda x, y: x + y, nums, 0)


# 5️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce una lista di stringhe "pari"/"dispari" corrispondenti a ciascun elemento.
# Usare una list comprehension e un operatore ternario.
def parity_list(nums: list) -> list:
    return ["pari" if num % 2 == 0 else "dispari" for num in nums]


# 6️⃣ Scrivere una funzione che, data una lista di parole,
# restituisce una nuova lista con solo le parole lunghe almeno 4 lettere.
# Usare filter() e lambda.
def long_words(words: list) -> list:
    return list(filter(lambda x: len(x) >= 4, words))


# 7️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce una nuova lista contenente ciascun numero moltiplicato per 2,
# ma solo se il numero è maggiore di 5.
# Usare list comprehension.
def double_if_greater_than_five(nums: list) -> list:
    return [num * 2 for num in nums if num > 5]


# 8️⃣ Scrivere una funzione che, data una lista di stringhe,
# restituisce una sola stringa formata da tutte le parole in maiuscolo separate da "-".
# Usare map() e join().
def join_upper(words: list) -> str:
    return "-".join(map(lambda w: w.upper(), words))


# 9️⃣ Scrivere una funzione che, data una lista di tuple (nome, voto),
# restituisce una lista con solo i nomi degli studenti che hanno voto >= 28.
# Usare list comprehension o filter() + lambda.
def top_students(students: list) -> list:
    return [student[0] for student in students if student[1] >= 28]


# 🔟 Scrivere una funzione che, data una lista di numeri,
# restituisce il prodotto di tutti i numeri dispari.
# Usare reduce() e una lambda function.
def product_of_odds(nums: list) -> int:
    return reduce(lambda x, y: x * y, filter(lambda x: x % 2 != 0, nums), 1)



# ✅ TEST FUNZIONI

check_test(squares, [1, 4, 9, 16], [1, 2, 3, 4])
check_test(squares, [], [])

check_test(even_numbers, [2, 4, 6], [1, 2, 3, 4, 5, 6])
check_test(even_numbers, [], [1, 3, 5])

check_test(lengths, [3, 4, 5], ["uno", "cane", "maree"])
check_test(lengths, [], [])

check_test(total_sum, 10, [1, 2, 3, 4])
check_test(total_sum, 0, [])

check_test(parity_list, ["dispari", "pari", "dispari", "pari"], [1, 2, 3, 4])
check_test(parity_list, [], [])

check_test(long_words, ["cane", "tavolo"], ["a", "cane", "tavolo"])
check_test(long_words, [], ["io", "tu", "va"])

check_test(double_if_greater_than_five, [12, 14], [3, 6, 7])
check_test(double_if_greater_than_five, [], [1, 2, 3])

check_test(join_upper, "CIAO-MONDO", ["ciao", "mondo"])
check_test(join_upper, "", [])

check_test(top_students, ["Luca", "Giulia"], [("Luca", 30), ("Giulia", 28), ("Marco", 25)])
check_test(top_students, [], [("Paolo", 20)])

check_test(product_of_odds, 15, [1, 2, 3, 4, 5])
check_test(product_of_odds, 1, [2, 4, 6])
