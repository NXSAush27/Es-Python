# === Esercizi Simulazione ===

nome = "Eric"
cognome = "Bordeianu"
matricola = "2258456"

"""
Si definisca la funzione func1(file_in : str) -> list[str] che prende
in ingresso una stringa che indica il percorso ad un file di testo e
restituisce una lista di stringhe.

La funzione apre il file di testo da cui si estraggono tutte le parole
portandole tutte a minuscole.

La funzione restituisce una lista delle parole uniche trovate nel file di
testo, ordinate in ordine alfabetico.

Esempio:
se file_in punta a 'txt/in_01.txt' la funzione restituisce
expected = ['bat', 'car', 'cat', 'condor', 'rat']

N.B. per estrarre le parole considerate solo i caratteri alfabetici;
esempi:
- la stringa '7od842m3m\t7gbe' diventa 4 parole ['od', 'm', 'm', 'gbe']
- la stringa 'E io a lui: "Poeta, io ti richeggio'
  diventa ['e', 'io', 'a', 'lui', 'poeta', 'io', 'ti', 'richeggio']
"""

def func1(file_in) -> list[str]:
    with open(file_in, 'r', encoding='utf-8') as f:
        text = f.read()
        parole = set()
        parola_corrente = ''
        for char in text:
            if char.isalpha():
                parola_corrente += char.lower()
            else:
                if parola_corrente:
                    parole.add(parola_corrente)
                    parola_corrente = ''
    return sorted(parole)
"""
Si definisca la funzione func2(file_in_a : str, file_in_b : str) ->
list[str] che riceve come argomenti 2 stringhe che puntano a due file di
testo e restituisce una lista di stringhe.  

La funzione apre i due file di testo e trova tutti i caratteri unici contenuti 
in ciascuno dei due file tranne a capo, tabulazioni e spazi.

La funzione restituisce una lista di stringhe dove nella prima parte della lista 
sono inseriti i caratteri unici del primo file che non appaiono nel secondo, 
ordinati in ordine alfabetico; mentre nella seconda parte sono inseriti i caratteri 
unici del secondo file che non compaiono nel primo sempre ordinati alfabeticamente.

Esempio:
come input 'txt/in_01.txt' e 'txt/in_03.txt'
la funzione restituisce

['B', 'D', 'E', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'P',
'S', 'U', 'V', 'Y', 'e', 'g', 'h', 'i', 'l', 'm', 'p', 's', 'u',
'v', 'w', 'y', '😌']
"""

def func2(file_in_a, file_in_b):
    with open(file_in_a, 'r', encoding='utf-8') as f:
        text_a = f.read()
    with open(file_in_b, 'r', encoding='utf-8') as f:
        text_b = f.read()
    chars_a = set(text_a) - {'\n', '\t', ' '}
    chars_b = set(text_b) - {'\n', '\t', ' '}
    unique_a = sorted(chars_a - chars_b)
    unique_b = sorted(chars_b - chars_a)
    return unique_a + unique_b
"""
Implementare la func3(lists : list[list[str]], listi :
list[list[int]], out : str) -> int: 
che riceve come argomenti: 
- una lista di liste di stringhe, di nome lists 
- una lista di liste di interi di nome listi 
- una stringa out, che indica a che percorso la funzione
deve scrivere un file di testo 
La funzione ritorna un intero.

Per ogni lista di parole contenuta in lists si scrive una riga del file
in out.  
L'ordine di scrittura delle parole su ciascuna riga e' pero' specificato 
dalla lista degli interi corrispondenti in listi, che vanno considerati
come posizioni delle parole da leggere dalle liste per scriverle nel file.

La funzione ritorna il numero totale di parole scritte nel file out.

Esempio se:
lists = [["monkey", "cat",], 
         ["panda", "alligator"], 
         ["zoo", 'zuu','zotero']] 
listi=  [[1, 0],	# prima la parola 1 e poi la 0
         [0, 1],	# prima la 0 e poi la 1
         [2, 1, 0]]	# prima la 2 poi la 1 poi la 0
valore di ritorno e' 7 e nel file out viene scritto:

cat monkey
panda alligator
zotero zuu zoo
"""

def func3(lists, listi, out):
    total_words = 0
    with open(out, 'w', encoding='utf-8') as f:
        for word_list, index_list in zip(lists, listi):
            ordered_words = [word_list[i] for i in index_list]
            f.write(' '.join(ordered_words) + '\n')
            total_words += len(ordered_words)
    return total_words

"""
Si scriva una funzione func4(input_file, output_file) che prende in
ingresso due stringhe, 'input_file' e 'output_file' che rappresentano
i percorsi a due file.  All'interno del file indicato da 'input_file'
sono presenti su una sola riga una serie di parole (composte da
caratteri alfabetici) separate da virgole, spazi, punti e virgole e da
punti.
La funzione deve individuare tutte le parole contenute nel file
indicate da 'input_file' e scriverle all'interno di un nuovo file
indicato da 'output_file'.  Le parole devono essere scritte
all'interno del file su una sola riga terminata dal carattere di
a capo, separate da uno spazio e con il seguente ordine:
    - numero di caratteri crescente,
    - in caso di parità, in ordine alfabetico, indipendentemente da
      maiuscole e minuscole
    - in caso di parole identiche, in ordine lessicografico.
La funzione deve restituire il numero di parole scritte nel file in
output.

Esempio: se il contenuto del file 'input_file' è il seguente
Dog,cat,dog;Cat.bird car

l'invocazione di func4('input_file', 'output_file') dovrà scrivere nel
file 'output_file' la seguente riga
car Cat cat Dog dog bird

e ritornare il valore 6.
"""

def func4(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
        words = []
        current_word = ''
        for char in text:
            if char.isalpha():
                current_word += char
            else:
                if current_word:
                    words.append(current_word)
                    current_word = ''
        if current_word:
            words.append(current_word)
    words.sort(key=lambda w: (len(w), w.lower(), w))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(' '.join(words) + '\n')
    return len(words)


"""
Si definisca una funzione func5(input_filename, output_filename, length) 
che riceve come argomenti due stringhe che rappresentano due nomi di file 
e un intero.
Il file input_filename contiene una serie di stringhe separate da spazi,
tabulazioni o a capo.
La funzione deve creare un nuovo file di testo con nome output_filename
contenente tutte le stringhe di lunghezza length presenti nel file
input_filename organizzate per righe.
Le righe devono essere in ordine alfabetico.
Le parole di ogni riga:
    - hanno la stessa lettera iniziale, senza distinzione fra maiuscole e
      minuscole
    - sono separate da uno spazio
    - sono ordinate in base all'ordine alfabetico, senza distinzione fra
      maiuscole e minuscole. In caso di parole uguali, in ordine alfabetico.

La funzione deve ritornare il numero di stringhe della lunghezza
richiesta trovate nel file in input.

Esempio
Se nel file 'func4_test1.txt' sono presenti le seguenti tre righe
cat bat    rat
Condor baT
Cat cAr CAR

la funzione func5('func5_test1.txt', 'func5_out1.txt', 3) dovrà scrivere
nel file 'func5_out1.txt' le seguenti 3 righe:
baT bat
CAR cAr Cat cat
rat

e ritornare il valore 7.
"""

def func5(input_filename : str, output_filename : str, length : int) -> int:
    with open(input_filename, 'r', encoding="utf-8") as f:
        text = f.read()
    words = []
    current_word = ''
    for char in text:
        if char.isalpha():
            current_word += char
        else:
            if current_word:
                if len(current_word) == length:
                    words.append(current_word)
                current_word = ''
            
    if current_word and len(current_word) == length:
        words.append(current_word)
    dictionario = {}
    for word in words:
        iniziale = word[0].lower()
        if iniziale in dictionario:
            dictionario[iniziale].append(word)
        else:
            dictionario[iniziale] = list()
            dictionario[iniziale].append(word)
    list_keys = list(dictionario.keys())
    list_keys.sort(key=lambda k: k)
    result = []
    for key in list_keys:
        values = dictionario[key]
        values.sort(key=lambda v: (v.lower(), v))
        result.append(' '.join(values) + "\n")
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.writelines(result)
    return len(words)