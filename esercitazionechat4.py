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


# 1️⃣ Scrivere una funzione che, data una lista di numeri interi,
# restituisca una nuova lista con solo i numeri dispari moltiplicati per 3.
def odd_times_three(nums: list) -> list:
    return [num*3 for num in nums if num%2]


# 2️⃣ Scrivere una funzione che riceve una stringa e restituisce
# un dizionario con il conteggio di vocali e consonanti.
# Non contare spazi, numeri o simboli.
def count_letters(s: str) -> dict:
    vocali = "aeiou"
    vocaliCount = 0
    consonantiCount = 0
    for char in s:
        if char.lower() in vocali:
            vocaliCount += 1
        elif char.isalpha():
            consonantiCount += 1
    return {"vocali": vocaliCount, "consonanti": consonantiCount}
    


# 3️⃣ Scrivere una funzione che riceve una tupla di tre elementi (nome, età, città)
# e restituisce una stringa nel formato "Nome ha X anni e vive a Città".
def format_info(t: tuple) -> str:
    nome, eta, città = t
    return f"{nome} ha {eta} anni e vive a {città}"


# 4️⃣ Scrivere una funzione che riceve due liste e restituisce True
# se hanno almeno un elemento in comune, False altrimenti.
def has_common(a: list, b: list) -> bool:
    set_a = set(a)
    set_b = set(b)
    if set_a.intersection(set_b):
        return True
    return False


# 5️⃣ Scrivere una funzione che, data una lista di interi,
# restituisce la somma dei numeri che si trovano in posizione pari (indice 0, 2, 4, …)
def sum_even_positions(a: list) -> int:
    sum = 0
    pari = a[::2]
    for paro in pari:
        sum += paro
    return sum


# 6️⃣ Scrivere una funzione che, data una lista di numeri,
# restituisce True se la somma di tutti i numeri è pari, False altrimenti.
def sum_is_even(a: list) -> bool:
    sum = 0
    for obj in a:
        sum += obj
    if obj % 2: # dispari
        return False
    return True # pari


# 7️⃣ Scrivere una funzione che riceve una lista di parole
# e restituisce una nuova lista con solo le parole che iniziano con una vocale.
def starts_with_vowel(words: list) -> list:
    vocali = "aeiou"
    result = []
    for word in words:
        if word and word[0].lower() in vocali:
            result.append(word)
    return result


# 8️⃣ Scrivere una funzione che riceve una lista di numeri
# e restituisce una lista con i numeri unici (che compaiono una sola volta).
def unique_numbers(nums: list) -> list:
    result = []
    numeripassati = []
    for num in nums:
        if not (num in numeripassati):
            result.append(num)
            numeripassati.append(num)
        elif num in result:
            result.remove(num)
    return result


# 9️⃣ Scrivere una funzione che riceve una stringa e restituisce
# la stessa stringa ma con le lettere alternate maiuscole/minuscole.
# Esempio: "ciao" → "CiAo"
def alternate_case(s: str) -> str:
    result = ""
    for i in range(len(s)):
        if i % 2 == 0:
            result += s[i].upper()
        else:
            result += s[i].lower()
    return result


# 🔟 Scrivere una funzione che riceve una lista di tuple (nome, voto)
# e restituisce la media dei voti degli studenti.
def average_grade(students: list) -> float:
    if not students:
        return 0.0
    totale = 0
    for student in students:
        totale += student[1]
    return totale / len(students)



# ✅ TEST FUNZIONI

check_test(odd_times_three, [9, 27, 15], [2, 3, 9, 4, 5])
check_test(odd_times_three, [], [2, 4, 6])

check_test(count_letters, {'vocali': 4, 'consonanti': 2}, "Ciao te")
check_test(count_letters, {'vocali': 0, 'consonanti': 0}, "123 !!!")

check_test(format_info, "Luca ha 25 anni e vive a Roma", ("Luca", 25, "Roma"))
check_test(format_info, "Sara ha 19 anni e vive a Napoli", ("Sara", 19, "Napoli"))

check_test(has_common, True, [1, 2, 3], [4, 5, 2])
check_test(has_common, False, [1, 2, 3], [7, 8, 9])

check_test(sum_even_positions, 9, [2, 5, 7])
check_test(sum_even_positions, 15, [10, 1, 5])

check_test(sum_is_even, True, [1, 1, 2])
check_test(sum_is_even, False, [1, 2, 3])

check_test(starts_with_vowel, ["amico", "ora"], ["amico", "cane", "ora", "tavolo"])
check_test(starts_with_vowel, [], ["cane", "tavolo"])

check_test(unique_numbers, [1, 4], [1, 2, 2, 3, 3, 4])
check_test(unique_numbers, [], [5, 5, 5])

check_test(alternate_case, "CiAo", "ciao")
check_test(alternate_case, "PyThOn", "python")

check_test(average_grade, 27.5, [("Luca", 30), ("Sara", 25)])
check_test(average_grade, 0.0, [])
