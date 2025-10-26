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
# SIMULAZIONE D’ESAME – SET 3
# ====================================================

# 1️⃣ Scrivere una funzione che riceve una lista di numeri (positivi e negativi)
# e restituisce un dizionario con due chiavi:
#   {"positivi": [lista dei positivi], "negativi": [lista dei negativi]}
# La funzione deve ignorare i valori non numerici, gestendo l’errore con try/except.
def split_numbers(values: list) -> dict:
    positivi = []
    negativi = []
    for v in values:
        try:
            num = int(v)
            if num>=0:
                positivi.append(num)
            else:
                negativi.append(num)
        except:
            continue
    return {"positivi": positivi, "negativi": negativi}


# 2️⃣ Scrivere una funzione che riceve una stringa e restituisce un dizionario
# con la frequenza delle lettere (solo alfabetiche, ignora spazi e simboli).
# Le lettere devono essere considerate *case-insensitive* (es. "A" == "a").
# Il dizionario deve essere ordinato alfabeticamente per chiave.
# Esempio: "Ciao a te" -> {"a": 2, "c": 1, "e": 1, "i": 1, "o": 1, "t": 1}
def letter_frequency(s: str) -> dict:
    freq= {}
    for char in s.lower():
        if char.isalpha():
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
    return dict(sorted(freq.items()))


# 3️⃣ Scrivere una funzione che riceve una lista di tuple (nome, eta)
# e restituisce il nome della persona più giovane.
# Se la lista è vuota, restituisce la stringa "Nessuno".
# Se due persone hanno la stessa età minima, restituisce la prima trovata.
def youngest(people: list) -> str:
    if not people:
        return "Nessuno"
    min_age = 99999
    youngest_name = ""
    for name, age in people:
        if age < min_age:
            min_age = age
            youngest_name = name
    return youngest_name


# 4️⃣ Scrivere una funzione che riceve una lista di numeri interi
# e restituisce True se la lista contiene *almeno due numeri consecutivi uguali*.
# Esempio: [1, 2, 2, 3] → True, [1, 2, 3] → False
def has_adjacent_equal(nums: list) -> bool:
    for i in range(len(nums)-1):
        if nums[i] == nums[i+1]:
            return True
    return False


# 5️⃣ Scrivere una funzione che prende in input una lista di parole
# e restituisce una nuova lista ordinata per lunghezza *crescente*.
# In caso di parole della stessa lunghezza, ordinare alfabeticamente.
# (Non usare sorted con key complesse, ma usa una lambda per esercitarti)
def sort_words(words: list) -> list:
    return sorted(words, key=lambda w: (len(w), w))


# 6️⃣ Scrivere una funzione che riceve una lista di dizionari con chiavi "nome" e "punteggio".
# Deve restituire un set con i nomi di chi ha ottenuto un punteggio >= della media.
# Gestire eventuali valori non numerici ignorandoli.
def top_scorers(records: list) -> set:
    total = 0
    count = 0
    for record in records:
        try:
            score = int(record["punteggio"])
            total += score
            count += 1
        except:
            continue
    if count == 0:
        return set()
    average = total / count
    result = set()
    for record in records:
        try:
            score = int(record["punteggio"])
            if score > average:
                result.add(record["nome"])
        except:
            continue
    return result


# 7️⃣ Scrivere una funzione che prende in input una lista di numeri
# e restituisce una *funzione lambda* che, data una funzione f(x),
# restituisce una nuova lista con f applicata solo ai numeri pari.
# Esempio:
#   f = selective_apply([1,2,3,4])
#   f(lambda x: x*10) → [20, 40]
def selective_apply(nums: list) -> Callable:
    return lambda func: [func(num) for num in nums if num % 2 == 0]


# ====================================================
# TEST
# ====================================================

check_test(split_numbers, {"positivi":[5, 2], "negativi":[-1]}, [5, -1, 2, "errore"])
check_test(split_numbers, {"positivi":[], "negativi":[]}, ["a", None])

check_test(letter_frequency, {"a":2, "c":1, "e":1, "i":1, "o":1, "t":1}, "Ciao a te")
check_test(letter_frequency, {}, "123 !")

check_test(youngest, "Luca", [("Anna", 25), ("Luca", 20), ("Marta", 21)])
check_test(youngest, "Nessuno", [])
check_test(youngest, "Anna", [("Anna", 18), ("Luca", 18)])

check_test(has_adjacent_equal, True, [1, 2, 2, 3])
check_test(has_adjacent_equal, False, [1, 2, 3, 4])
check_test(has_adjacent_equal, False, [])

check_test(sort_words, ["a", "te", "ciao", "zebra"], ["ciao", "zebra", "a", "te"])

check_test(top_scorers, {"Anna", "Luca"}, [
    {"nome": "Anna", "punteggio": 30},
    {"nome": "Luca", "punteggio": 28},
    {"nome": "Marco", "punteggio": 20},
    {"nome": "Errore", "punteggio": "xx"}
])

f = selective_apply([1, 2, 3, 4])
check_test(lambda func: func(lambda x: x*10), [20, 40], f)
check_test(lambda func: func(lambda x: x+1), [3, 5], f)
