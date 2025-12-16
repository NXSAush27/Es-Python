#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
################################################################################
################################################################################

""" PREREQUISITI:
 1) Salva il file come program.py
 2) Assegna le variabili sottostanti con il tuo
      NOME, COGNOME, NUMERO_MATRICOLA

Per superare l'esame, è necessario ottenere un punteggio maggiore o uguale a 18 (15 per studenti DSA)

Il voto finale è la somma dei punteggi dei problemi risolti.

Attenzione! DEBUG=True in grade.py per migliorare il debug.
Tuttavia, per testare correttamente la ricorsione, DEBUG=False è necessario.

"""
name       = "Eric"
surname    = "Bordeianu"
student_id = "2258456"



################################################################################
# ---------------------------- SUGGERIMENTI PER IL DEBUG --------------------- #
# Per eseguire solo alcuni dei test, puoi commentare le voci
# corrispondenti ai test che non vuoi eseguire all'interno della lista `test`
# ALLA FINE di `grade.py`.
#
# Per il debug delle funzioni ricorsive, puoi disabilitare il test di ricorsione
# impostando `DEBUG=True` all'interno del file `grade.py`.
#
# L'impostazione di DEBUG=True attiva anche la stampa a terminale dello STACK
# TRACE degli errori, che ti permette di conoscere il numero di riga in `program.py`
# che ha generato un errore.
################################################################################


# %% -------------------------------- FUNC.1 -------------------------------- #
''' func1: 4 punti
Definisci la funzione func1(embedding_list1, embedding_list2) che prende come argomenti due liste di tuple. 
Ogni tupla rappresenta una parola e il suo embedding vettoriale: `(stringa_parola, [float1, float2, ...])`.
La funzione cerca la coppia di parole più simili. La somiglianza è calcolata usando la funzione di supporto
 `cosine_similarity` sugli embedding corrispondenti a due parole.
La funzione deve restituire una tupla `(parola1, parola2, punteggio_somiglianza)`, dove `parola1` proviene 
da `embedding_list1`, `parola2` proviene da `embedding_list2`, e `punteggio_somiglianza` è la somiglianza coseno.
Se più coppie hanno la stessa somiglianza, restituisci quella in cui `parola1` è alfabeticamente minore, ed in
 seconda istanza, `parola2` è alfabeticamente minore.

Esempio:
  embeddings1 = [('king', [0.1, 0.2]), ('queen', [0.3, 0.4])]
  embeddings2 = [('man', [0.05, 0.15]), ('woman', [0.25, 0.35])]
  # Per semplicità, se (queen, woman) ha la somiglianza più alta.
  func1(embeddings1, embeddings2) potrebbe restituire ('queen', 'woman', 0.9997)
'''
import math
def func1(embedding_list1, embedding_list2):
    # Funzione di supporto per la somiglianza coseno
    def cosine_similarity(vec1, vec2):
        dot_product = sum(a*b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a**2 for a in vec1))
        magnitude2 = math.sqrt(sum(b**2 for b in vec2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return round(dot_product / (magnitude1 * magnitude2), 4)
    candidato_emb1 = None
    candidato_emb2 = None
    maxSim = -1
    for element in embedding_list1:
      for element2 in embedding_list2:
        similarita = cosine_similarity(element[1], element2[1])
        if maxSim < similarita:
          maxSim = similarita
          candidato_emb1 = element[0]
          candidato_emb2 = element2[0]
        elif maxSim == similarita:
          if element[0] < candidato_emb1:
            maxSim = similarita
            candidato_emb1 = element[0]
            candidato_emb2 = element2[0]
          elif element[0] == candidato_emb1:
            if element2[0] < candidato_emb2:
              maxSim = similarita
              candidato_emb1 = element[0]
              candidato_emb2 = element2[0]
    return (candidato_emb1, candidato_emb2, maxSim)



# %% -------------------------------- FUNC.2 -------------------------------- #
''' func2: 4 punti
Definisci la funzione func2(text_corpus, sentiment_lexicon, top_k_sentences) che prende:
  - `text_corpus`: una lista di stringhe, dove ogni stringa è una frase.
  - `sentiment_lexicon`: un dizionario, che mappa parole (stringhe, minuscole) ai loro punteggi di sentimento (float, es. da -1.0 a 1.0).
  - `top_k_sentences`: un intero, il numero delle frasi più positive da riportare.

Dividi ogni frase in `text_corpus` in parole (token minuscoli) usando la funzione di supporto `tokenize_alphabetic`.
Calcola il punteggio di sentimento della frase sommando i punteggi di tutte le sue parole trovate nel lessico.
Le parole non presenti nel lessico hanno sentimento 0. Arrotonda tutti i valori di sentimento a 2 cifre decimali.

La funzione deve restituire un dizionario con la seguente struttura:
  - `overall_sentiment`: float, il punteggio di sentimento medio di tutte le frasi.
  - `top_positive_sentences`: una lista di K tuple `(punteggio, stringa_frase)` di frasi con sentimento positivo (>0),
    ordinate per punteggio decrescente. Se esistono meno di `top_k_sentences` con sentimento positivo, includi tutte quelle disponibili.
    In caso di parità, includi quelle con la frase maggiore in ordine lessicografico.
  - `total_sentences_analyzed`: intero, il numero totale di frasi elaborate.

Esempio:
  text_corpus = ["This is a great movie!", "It was terrible.", "What a lovely day."]
  sentiment_lexicon =  {'great': 0.8, 'terrible': -0.9, 'lovely': 0.7}
  func2(text_corpus, sentiment_lexicon, 1) should return (order of sentences might vary for same score):
  {
      'overall_sentiment': 0.20,
      'top_positive_sentences': [(0.80, 'This is a great movie!')],
      'total_sentences_analyzed': 3
  }
'''
import re

def tokenize_alphabetic(text):
    """
    Tokenizza il testo di input in una lista di parole alfabetiche.
    Ignora la punteggiatura e i caratteri non alfabetici.

    Args:
        text (str): La stringa di input da tokenizzare.

    Returns:
        list: Una lista di parole alfabetiche.
    """
    return re.findall(r'[a-z]+', text.lower())


def func2(text_corpus, sentiment_lexicon, top_k_sentences):
    punteggi_frasi = []
    somma_sentimenti = 0.0
    for frase in text_corpus:
      parole = tokenize_alphabetic(frase)
      punteggio_frase = 0.0
      for parola in parole:
        if parola in sentiment_lexicon:
          punteggio_frase += sentiment_lexicon[parola]
      punteggio_frase = round(punteggio_frase, 2)
      somma_sentimenti += punteggio_frase
      punteggi_frasi.append((punteggio_frase, frase))
    overall_sentiment = round(somma_sentimenti / len(text_corpus), 2) if len(text_corpus) > 0 else 0.0
    frasi_positive = [item for item in punteggi_frasi if item[0] > 0]
    frasi_positive.sort(key=lambda x: (-x[0], x[1]))
    top_positive_sentences = frasi_positive[:top_k_sentences]
    return {
        'overall_sentiment': overall_sentiment,
        'top_positive_sentences': top_positive_sentences,
        'total_sentences_analyzed': len(text_corpus)
    }

# %% -------------------------------- FUNC.3 -------------------------------- #
''' func3: 4 punti
Definisci la funzione func3(sentence_list, forbidden_words) che prende come argomenti
una lista di stringhe `sentence_list` (che rappresentano frasi) e un set di `forbidden_words` (stringhe).
La funzione dovrebbe identificare e rimuovere qualsiasi frase da `sentence_list` (modificandola in-place)
che contiene almeno una parola dal set `forbidden_words` (case-insensitive).
Le parole nelle frasi sono definite come sequenze di caratteri alfabetici (puoi usare la funzione di supporto
`tokenize_alphabetic` per tokenizzare le frasi).
La funzione dovrebbe restituire il conteggio totale delle frasi rimosse.

Esempio:
    sentence_list = ["This is a test sentence.", "Bad words here.", "Another one for good measure."]
    forbidden_words = {"bad", "terrible", "forbidden"}
    dopo aver chiamato func3(sentence_list, forbidden_words),
    sentence_list dovrebbe essere ["This is a test sentence.", "Another one for good measure."]
    e la funzione dovrebbe restituire 1.

IMPORTANTE: la lista `sentence_list` deve essere modificata alla fine dell'esecuzione della funzione.
'''
def func3(sentence_list: list, forbidden_words):
  contatoreRimosse = 0
  i = 0
  while i < len(sentence_list):
    lista_parole = tokenize_alphabetic(sentence_list[i])
    sentinella = True
    for parola in lista_parole:
      if parola in forbidden_words:
        sentinella = False
        break
    if not sentinella:
      sentence_list.pop(i)
      contatoreRimosse += 1
    else:
      i += 1
  return contatoreRimosse

# %% -------------------------------- FUNC.4 -------------------------------- #
''' func4: 4 punti
Definisci la funzione func4(text, n) che prende una stringa `text` e un intero `n`.
La funzione deve tokenizzare il testo in parole alfabetiche (usando `tokenize_alphabetic`),
contare la frequenza di ogni parola e restituire una lista delle `n` parole più frequenti
insieme ai loro conteggi. La lista deve essere ordinata per conteggio decrescente, dopodiché alfabeticamente
per parola in caso di parità.

Esempio:
  text = "The quick brown fox jumps over the lazy dog. The fox is quick."
  func4_a(text, 2) dovrebbe restituire [('the', 3), ('fox', 2)]
  func4_a(text, 3) dovrebbe restituire [('the', 3), ('fox', 2), ('quick', 2)]
'''
def func4(text, n):
  testo_tokenizzato = tokenize_alphabetic(text)
  dizionario_frequenze = {}
  for parola in testo_tokenizzato:
    if parola in dizionario_frequenze:
      dizionario_frequenze[parola] += 1
    else:
      dizionario_frequenze[parola] = 1
  lista_frequenze = list(dizionario_frequenze.items())
  lista_frequenze.sort(key=lambda x: (-x[1], x[0]))
  return lista_frequenze[:n]

# %% -------------------------------- FUNC.5 -------------------------------- #
''' func5: 4 punti
Definisci la funzione func5(word_list) che prende una lista di stringhe `word_list`.
La funzione dovrebbe trovare tutti i gruppi di anagrammi all'interno di `word_list`.
Due parole sono anagrammi se contengono gli stessi caratteri, indipendentemente dall'ordine o dalla maiuscole/minuscole.
La funzione deve restituire un dizionario in cui le chiavi sono la "forma canonica" di un gruppo di anagrammi
(cioè, la parola in minuscolo con le sue lettere ordinate alfabeticamente), e i valori sono
set di parole uniche da `word_list` che appartengono a quel gruppo di anagrammi (preservando le maiuscole/minuscole originali).

Esempio:
  word_list = ["listen", "silent", "Enlist", "apple", "Banana", "apPLe"]
  func5(word_list) dovrebbe restituire (l'ordine delle chiavi potrebbe variare):
  {
      'eilnst': {'listen', 'silent', 'Enlist'},
      'aelpp': {'apple', 'apPLe'},
      'aaabnn': {'Banana'}
  }
'''
def func5(word_list):
  dizionario_anagrammi = {}
  for parola in word_list:
    forma_canonica = ''.join(sorted(parola.lower()))
    if forma_canonica in dizionario_anagrammi:
      dizionario_anagrammi[forma_canonica].add(parola)
    else:
      dizionario_anagrammi[forma_canonica] = {parola}
  return dizionario_anagrammi


# %% --------------------------------- EX.1 --------------------------------- #
''' Ex1: 6 punti
**Questa funzione deve essere risolta usando un approccio ricorsivo.**
**La funzione ricorsiva deve essere top-level (cioè, non definita all'interno di un'altra funzione).**

Implementa la funzione ex1(root, result, target_value), che prende tre argomenti:
- root: La radice di un albero binario.
- result: Una lista vuota, deve essere popolata in-place con il percorso al nodo target.
- target_value: Il valore del nodo da trovare.

Registra il percorso dalla radice all'occorrenza più profonda di target_value nella lista `result`.
Se ci sono più occorrenze di target_value alla stessa profondità massima, scegli quella più a sinistra.
La funzione non deve restituire alcun valore. Invece, deve popolare la lista `result` in-place con la lista
dei valori dei nodi che rappresentano il percorso dalla radice al nodo target scelto. Se target_value non viene trovato nell'albero,
la lista `result` deve rimanere vuota.

Esempio:
  Albero:
       1
     /   \ 
    2     3
   / \   / \ 
  4   5 4   9
 / \ 
8   9
Se target_value è 5, result sarà [1, 2, 5].
Se target_value è 9, result sarà [1, 2, 4, 9] (più profonda).
Se target_value è 4, result sarà [1, 2, 4] (più a sinistra).

Si puo' usare la classe BinaryTree del modulo tree.py
'''
def ex1(root, result: list, target_value):
  percorso = []
  max_depth = [-1]  # Lista per evitare problemi con l'assegnazione in funzioni annidate
  trova_percorso(root, 0, target_value, percorso, result, max_depth)

def trova_percorso(nodo, profondita, target_value, percorso_corrente, result, max_depth):
    if nodo is None:
        return
    percorso_corrente.append(nodo.value)
    if nodo.value == target_value:
        if profondita > max_depth[0]:
            max_depth[0] = profondita
            result.clear()
            result.extend(percorso_corrente)
    trova_percorso(nodo.left, profondita + 1, target_value, percorso_corrente, result, max_depth)
    trova_percorso(nodo.right, profondita + 1, target_value, percorso_corrente, result, max_depth)
    percorso_corrente.pop()


# %% --------------------------------- EX.2 --------------------------------- #
import os
import images

''' Ex2: 6 punti
**Questa funzione deve essere risolta usando un approccio ricorsivo.**
**La funzione ricorsiva deve essere top-level (cioè, non definita all'interno di un'altra funzione).**

Implementa la funzione ex2(in_path, out_fpath, x, y, replacement_color), che prende i seguenti argomenti:
- in_path, out_fpath: i percorsi delle immagini PNG di input e output.
- x, y (int): La coordinata x e y di partenza.
- replacement_color (tupla di 3 interi): Il nuovo colore di riempimento.
Partendo dal pixel alle coordinate (x, y) di colore c, coloralo con `replacement_color`. Ricorsivamente, riempi la
regione di pixel vicini di colore c con il nuovo colore. Considera i pixel a sinistra, destra, sopra e sotto
rispetto al pixel corrente come vicini.

Si possono usare le funzioni load e save del modulo images.py
'''

# Helper function to automatically handle file paths
def get_correct_path(relative_path):
    """
    Automatically detects and adjusts file paths to work from any location.
    
    This function tries multiple strategies to find the correct file path:
    1. Check if the path exists as-is from current directory
    2. Look for the struggling-student directory in the parent directory
    3. Check if the path exists from the script's directory
    4. Check various possible directory structures
    
    Args:
        relative_path (str): The relative path to adjust
        
    Returns:
        str: The correct absolute path that works from any directory
    """
    # Strategy 1: Check if the path exists as-is
    if os.path.exists(relative_path):
        return relative_path
    
    # Strategy 2: Try current directory with struggling-student prefix
    possible_paths = [
        os.path.join('struggling-student PythonExercises main Esami-2024-2025_2025-07-21', relative_path),
        relative_path,
    ]
    
    # Strategy 3: Look for the script directory (where this program.py is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths.append(os.path.join(script_dir, relative_path))
    
    # Strategy 4: Try parent directory structure
    parent_dir = os.path.dirname(script_dir)
    possible_paths.append(os.path.join(parent_dir, 'struggling-student PythonExercises main Esami-2024-2025_2025-07-21', relative_path))
    
    # Strategy 5: Check for any directory containing "struggling-student" in the path
    base_path = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(base_path):
        if 'struggling-student' in root:
            test_path = os.path.join(root, relative_path)
            if os.path.exists(test_path):
                return test_path
    
    # Strategy 6: Check from current working directory if we're in a subdirectory
    cwd = os.getcwd()
    if 'struggling-student' in cwd:
        test_path = os.path.join(cwd, relative_path)
        if os.path.exists(test_path):
            return test_path
    
    # Strategy 7: Try to find the directory by walking up from current directory
    current_dir = os.getcwd()
    for i in range(5):  # Check up to 5 levels up
        test_path = os.path.join(current_dir, 'struggling-student PythonExercises main Esami-2024-2025_2025-07-21', relative_path)
        if os.path.exists(test_path):
            return test_path
        # Go up one level
        parent = os.path.dirname(current_dir)
        if parent == current_dir:  # Reached filesystem root
            break
        current_dir = parent
    
    # If none of the strategies work, return the original path
    # This will cause an error when trying to load, which is better than silently failing
    return relative_path

from images import load, save

def ex2(in_path, out_fpath, x, y, replacement_color):
    # Use the helper function to get the correct path
    correct_in_path = get_correct_path(in_path)
    correct_out_path = get_correct_path(out_fpath)
    
    img = load(correct_in_path)
    altezza = len(img)
    larghezza = len(img[0]) if altezza > 0 else 0
    colore_originale = img[y][x]
    flood_fill(x, y, img, altezza, larghezza, colore_originale, replacement_color)
    save(img, correct_out_path)

def flood_fill(x, y, img, altezza, larghezza, colore_originale, replacement_color):
    if x < 0 or x >= larghezza or y < 0 or y >= altezza:
        return
    if img[y][x] != colore_originale or img[y][x] == replacement_color:
        return
    img[y][x] = replacement_color
    flood_fill(x + 1, y, img, altezza, larghezza, colore_originale, replacement_color)
    flood_fill(x - 1, y, img, altezza, larghezza, colore_originale, replacement_color)
    flood_fill(x, y + 1, img, altezza, larghezza, colore_originale, replacement_color)
    flood_fill(x, y - 1, img, altezza, larghezza, colore_originale, replacement_color)


###################################################################################
if __name__ == '__main__':
    print('*' * 50)
    print('Eseguire grade.py per effettuare il debug con grader incorporato.')
    print('Altrimenti, inserire codice qui per verificare le funzioni con test propri')
    print('*' * 50)
