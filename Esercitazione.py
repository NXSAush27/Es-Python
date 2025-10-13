from typing import Any, Callable, List


# Test per le liste
def print_test(func: Callable, *args: List[Any]):
    func_str = func.__name__
    args_str = ', '.join(repr(arg) for arg in args)
    try:
        result = func(*args)
        result_str = repr(result)
        print(f'{func_str}({args_str}) => {result_str}')
    except BaseException as error:
        error_str = repr(error)
        print(f'ERROR: {func_str}({args_str}) => {error_str}')


################################################################################
# Funzioni
################################################################################
# Scrivere una funzione che prende un numero in virgola mobile, ne calcola la
# radice cubica, e la ritorna.
def cubic_root(n):
    if n < 0:
        return -cubic_root(-n)
    start = 0
    end = n
    precisione = 0.0001
    while True:
        mid = (start + end) / 2
        if abs(mid**3 - n) <= precisione:
            return mid
        if mid**3 < n:
            start = mid
        else:
            end = mid

# Scrivere una funzione che prende tre valori(`d`, `m`, `y`) e ritorna se la
# data è valida o no. Si possono ignorare gli anni bisestili. Ad esempio,
# ritorna `False` per `30/2/2017` e `True` per `1/1/1111`.
def check_date(d, m, y):
    if y < 0 or m < 1 or m > 12 or d < 1:
        return False
    giorniMese = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if d > giorniMese[m - 1]:
        return False
    return True


#Test funzioni
print_test(cubic_root, 8)
print_test(cubic_root, -1)
print_test(check_date, -1, 12, 2011)
print_test(check_date, 1, 14, 2011)
print_test(check_date, 1, 12, -1)
print_test(check_date, 31, 4, 2011)
print_test(check_date, 30, 4, 2011)

################################################################################
# Stringhe
################################################################################


# Scrivere una funzione che restituisce una stringa di saluto formata da
# `Ciao `, seguito dal nome come parametro, e poi da `Buona giornata!`
def make_hello(name: str) -> str:
    return 'Ciao ' + name + '. Buona giornata!'


# Scrivere una funzione che implenta la stessa funzionalità di `str.strip()`,
# che rimuove spazi all'inizio e alla fine della stringa.
# Usare solo costrutti del linguaggio e non librerie.
def strip_whitespace(string: str) -> str:
    inizio = 0
    fine = len(string) - 1
    while inizio <= fine and (string[inizio] == ' '):
        inizio += 1
    while fine >= inizio and (string[fine] == ' '):
        fine -= 1
    return string[inizio:fine + 1]


# Scrivere una funzione che implenta la stessa funzionalità di `str.split()`,
# rimuovendo uno dei caratteri presi in input. Non ritornare stringhe vuote.
# Usare solo costrutti del linguaggio e non librerie.
def split_string(string: str, characters: str = '') -> List[str]:
    risultato = []
    inizio = 0
    fine = len(string) - 1
    for i in range(len(string)):
        if string[i] in characters:
            if inizio < fine:
                risultato.append(string[inizio:fine + 1])
            inizio = i + 1
            fine = i + 1
        else:
            fine = i
    if inizio < fine:
        risultato.append(string[inizio:fine + 1])
    return risultato
        


# Scrivere una funziona che si comporta come `str.replace()`.
# Usare solo costrutti del linguaggio e non librerie.
def replace_substring(string: str, find: str, replace: str) -> str:
    risultato = ''
    i = 0
    while i < len(string):
        if string[i:i + len(find)] == find:
            risultato += replace
            i += len(find)
        else:
            risultato += string[i]
            i += 1
    return risultato

# Scrivere una funzione che codifica un messaggio con il cifrario di
# Cesare, che sostituisce ad ogni carattere il carattere che si
# trova ad un certo offset nell'alfabeto. Quando si applica l'offset,
# si riparte dall'inizio se necessario (pensate a cosa fa il modulo).
# La funzione permette anche di decrittare un messaggio applicando
# l'offset in negativo. Si può assumere che il testo è minuscolo e
# fatto delle sole lettere dell'alfabeto inglese e spazi che non sono crittati.
# Suggerimento: Sono utili le funzioni `ord()` e `chr()`.
def caesar_cypher(string: str, offset: int, decrypt: bool = False) -> str:
    risultato = ''
    if decrypt:
        offset = -offset
    for char in string:
        if char == ' ':
            risultato += ' '
        else:
            nuovo = (ord(char) - ord('a') + offset) % 26 + ord('a')
            risultato += chr(nuovo)
    return risultato


# Test funzioni
print_test(make_hello, 'Pippo')
print_test(strip_whitespace, '  Pippo  ')
print_test(strip_whitespace, '   ')
print_test(split_string, 'Pippo Pluto  ', ' \t\r\n')
print_test(split_string, 'Pippo   Pluto  ', ' \t\r\n')
print_test(replace_substring, 'Ciao Pippo. Ciao Pluto.', 'Ciao', 'Hello')
print_test(caesar_cypher, 'ciao pippo', 17, False)
print_test(caesar_cypher, 'tzrf gzggf', 17, True)

################################################################################
# Liste
################################################################################


# Scrivere una funzione che somma i quadrati degli elementi di una lista.
def sum_squares(elements: List[int]) -> int:
    totale = 0
    for elemento in elements:
        totale += elemento**2
    return totale


# Scrivere una funzione che ritorna il valore massimo degli elementi di una lista.
def max_element(elements: List[int]) -> int:
    if len(elements) == 0:
        print("Errore: lista vuota")
        return None
    massimo = elements[0]
    for elemento in elements:
        if elemento > massimo:
            massimo = elemento
    return massimo


# Scrivere una funzione che rimuove i duplicati da una lista.
# Commentare sul tempo di esecuzione.
def remove_duplicates(elements: list) -> list:
    risultato = []
    for elemento in elements:
        if elemento not in risultato:
            risultato.append(elemento)
    return risultato
    # Tempo di esecuzione: O(n^2) perché per ogni elemento della lista originale
    # si fa una ricerca lineare nella lista risultato.
# Scrivere una funzione che si comporta come `reverse()`.
# Usare solo costrutti del linguaggio e non librerie.
def reverse_list(elements: list) -> list:
    risultato = []
    for i in range(len(elements), 0, -1):
        risultato.append(elements[i - 1])
    return risultato

# Scrivere una funzione `flatten_list()` che prende una lista che contiene
# elementi o altre liste, e restituisce una lista contenente tutti gli elementi.
# Si può assumere che le liste contenute non contengono altre liste.
# Usare la funzione `isinstance()` per determinare se un elemento è una lista.
# Usare solo costrutti del linguaggio e non librerie.
def flatten_list(elements: list) -> list:
    risultato = []
    for elemento in elements:
        if isinstance(elemento, list):
            risultato += flatten_list(elemento) 
        else:
            risultato.append(elemento)
    return risultato


# Test funzioni
print_test(sum_squares, [1, 2, 3])
print_test(max_element, [1, 2, 3, -1, -2])
print_test(max_element, [-1, -2])
print_test(max_element, [])
print_test(remove_duplicates, [1, 2, 3, 2, 3])
print_test(reverse_list, [1, 2, 3])
print_test(flatten_list, [1, [2, 3]])
print_test(flatten_list, [1, [2, [3, 4]]])