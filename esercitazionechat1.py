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
# ESERCIZI
# ====================================================

# 1️⃣ Scrivere una funzione che calcola il numero di vocali in una stringa.
# Deve ignorare maiuscole/minuscole e restituire il numero di vocali trovate.
def count_vowels(s: str) -> int:
    counter = 0
    for char in s:
        if char in 'aeiou':
            counter += 1
    return counter


# 2️⃣ Scrivere una funzione che data una lista di interi
# restituisce una nuova lista con i numeri pari raddoppiati
# e i numeri dispari dimezzati (usare // per divisione intera).
def transform_list(nums: list) -> list:
    result = []
    for num in nums:
        if num % 2: # è dispari
            result.append(num//2)
        else: # è pari
            result.append(num*2)
    return result


# 3️⃣ Scrivere una funzione che riceve una lista di parole
# e restituisce la parola più lunga.
# Se ci sono più parole con la stessa lunghezza, restituisci la prima.
def longest_word(words: list) -> str:
    longest = ""
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest

# 4️⃣ Scrivere una funzione che riceve un numero intero positivo n
# e restituisce True se è un numero primo, False altrimenti.
# (Un numero è primo se è divisibile solo per 1 e se stesso)
def is_prime(n: int) -> bool:
    if n == 1:
        return True
    for i in range(2, n//2): # cerco in tutti i numeri che potrebbero essere divisori (tolgo i numeri maggiori della metà perchè impossibili divisori)
        if n % i == 0:
            return False # non è primo
    return True # è primo

# 5️⃣ Scrivere una funzione che riceve una lista di tuple (nome, voto)
# e restituisce il nome dello studente con il voto più alto.
# Se più studenti hanno lo stesso voto massimo, restituisci il primo.
def best_student(students: list) -> str:
    nomeBest = ""
    votoBest = 0
    for student in students:
        if student[1] > votoBest:
            votoBest = student[1]
            nomeBest = student[0]
    return nomeBest


# ====================================================
# TEST
# ====================================================

check_test(count_vowels, 5, "Educazione")
check_test(count_vowels, 1, "Python")
check_test(count_vowels, 0, "xyz")

check_test(transform_list, [0, 4, 1, 12], [1, 2, 3, 6])
check_test(transform_list, [4, 1, 8], [2, 3, 4])

check_test(longest_word, "cocomero", ["pera", "cocomero", "uva"])
check_test(longest_word, "ciao", ["ciao", "test", "ok"])
check_test(longest_word, "", [])

check_test(is_prime, True, 7)
check_test(is_prime, False, 9)
check_test(is_prime, True, 1)
check_test(is_prime, True, 2)

check_test(best_student, "Luca", [("Anna", 27), ("Luca", 30), ("Gianni", 18)])
check_test(best_student, "Anna", [("Anna", 30), ("Luca", 30), ("Gianni", 29)])
check_test(best_student, "", [])
