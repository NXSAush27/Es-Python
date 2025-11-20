import os
import json
import requests

"""
### 🏋️ Esercizio 1: Contatore di Frequenza Parole

1.  Crea manualmente un file di testo (`input.txt`) e riempilo con del testo (almeno un paragrafo, con maiuscole e punteggiatura).
2.  Leggi l'intero contenuto del file in una singola stringa.
3.  Converti la stringa interamente in minuscolo.
4.  Identifica tutti i caratteri unici nel testo che *non* sono lettere dell'alfabeto.
5.  Crea una nuova versione della stringa in cui ogni carattere non alfabetico è stato sostituito da uno spazio.
6.  Dividi la stringa pulita in una lista di parole (gli spazi sono i delimitatori).
7.  Conta le occorrenze di ogni parola in questa lista e memorizza i risultati in un dizionario (dove la parola è la chiave e il conteggio è il valore).
8.  Crea un nuovo file (`conteggio.txt`) in modalità di scrittura.
9.  Scorri il dizionario dei conteggi e scrivi ogni coppia chiave-valore (parola e frequenza) nel nuovo file, una per riga.

---
"""
def esercizio1():
    with open('input1.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.lower()
    non_alpha_chars = set(char for char in text if not char.isalpha())
    for char in non_alpha_chars:
        text = text.replace(char, ' ')
    words = text.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    with open('conteggio.txt', 'w', encoding='utf-8') as f:
        for word, count in word_count.items():
            f.write(f"{word} {count}\n")

#esercizio1()

"""
### 🗂️ Esercizio 2: Gestore di Spese in JSON

1.  Scegli un nome per il file che memorizzerà i dati (es. `spese.json`).
2.  Tenta di aprire e leggere il file. Se il file esiste, decodifica il suo contenuto (che dovrebbe essere in formato JSON) in una lista Python.
3.  Se il file non esiste (il che provocherà un errore), gestisci l'errore e inizia invece con una lista Python vuota. Chiamiamo questa lista `dati_spese`.
4.  Avvia un ciclo che chiede all'utente di scegliere un'azione: "Aggiungi", "Lista" o "Esci".
5.  **Se "Aggiungi"**: Chiedi all'utente una descrizione per la spesa e un importo. Crea un dizionario con questi due valori. Aggiungi questo dizionario alla lista `dati_spese`. Dopodiché, salva l'intera lista `dati_spese` nel file (sovrascrivendolo), assicurandoti di formattare l'output JSON in modo che sia leggibile (indentato).
6.  **Se "Lista"**: Scorrila lista `dati_spese` e stampa ogni spesa (ogni dizionario) sullo schermo.
7.  **Se "Esci"**: Interrompi il ciclo.

---
"""

def esercizio2():
    filename = 'spese.json'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            dati_spese = json.load(f)
    except FileNotFoundError:
        dati_spese = []
    while True:
        action = input("Scegli un'azione (Aggiungi, Lista, Esci): ").strip().lower()
        if action == 'aggiungi':
            descrizione = input("Descrizione della spesa: ")
            importo = float(input("Importo della spesa: "))
            spesa = {'descrizione': descrizione, 'importo': importo}
            dati_spese.append(spesa)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dati_spese, f, indent=4)
        elif action == 'lista':
            for spesa in dati_spese:
                print(f"Descrizione: {spesa['descrizione']}, Importo: {spesa['importo']}")
        elif action == 'esci':
            break
        else:
            print("Azione non valida. Riprova.")

#esercizio2()
"""
### 🖥️ Esercizio 3: Scanner di File di Grandi Dimensioni

1.  Chiedi all'utente di inserire un percorso di una directory (se non inserisce nulla, usa la directory corrente come predefinita).
2.  Chiedi all'utente una dimensione minima in Megabyte (MB) che fungerà da filtro.
3.  Converti la dimensione inserita dall'utente da Megabyte a byte.
4.  Ottieni la lista di tutti gli elementi (file e cartelle) contenuti nella directory specificata.
5.  Per ogni elemento nella lista:
6.  Costruisci il percorso completo (percorso della directory + nome dell'elemento).
7.  Verifica se l'elemento è un file (e non una directory).
8.  Se è un file, ottieni le informazioni dal sistema operativo relative a quel file, in particolare la sua dimensione esatta in byte.
9.  Confronta la dimensione del file con la soglia in byte calcolata al punto 3.
10. Se la dimensione del file è superiore alla soglia, stampa il nome del file e la sua dimensione (meglio se riconvertita in MB per facilità di lettura).
---

"""

def esercizio3():
    """
    ### 🖥️ Esercizio 3: Scanner di File di Grandi Dimensioni

    1.  Chiedi all'utente di inserire un percorso di una directory (se non inserisce nulla, usa la directory corrente come predefinita).
    2.  Chiedi all'utente una dimensione minima in Megabyte (MB) che fungerà da filtro.
    3.  Converti la dimensione inserita dall'utente da Megabyte a byte.
    4.  Ottieni la lista di tutti gli elementi (file e cartelle) contenuti nella directory specificata.
    5.  Per ogni elemento nella lista:
    6.  Costruisci il percorso completo (percorso della directory + nome dell'elemento).
    7.  Verifica se l'elemento è un file (e non una directory).
    8.  Se è un file, ottieni le informazioni dal sistema operativo relative a quel file, in particolare la sua dimensione esatta in byte.
    9.  Confronta la dimensione del file con la soglia in byte calcolata al punto 3.
    10. Se la dimensione del file è superiore alla soglia, stampa il nome del file e la sua dimensione (meglio se riconvertita in MB per facilità di lettura).
    """
    try:
        directory = input("Inserisci il percorso della directory (lascia vuoto per la directory corrente): ").strip()
        if not directory:
            directory = '.'
        
        min_size_mb = float(input("Inserisci la dimensione minima in MB: "))
        min_size_bytes = min_size_mb * 1024 * 1024  # Convert MB to bytes
        
        print(f"\nCercando file più grandi di {min_size_mb} MB in '{directory}'...")
        
        if not os.path.exists(directory):
            print(f"La directory '{directory}' non esiste.")
            return
            
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                if file_size > min_size_bytes:
                    size_mb = file_size / (1024 * 1024)
                    print(f"{item}: {size_mb:.2f} MB ({file_size} bytes)")
                    
    except ValueError:
        print("Inserisci un valore numerico valido per la dimensione.")
    except Exception as e:
        print(f"Errore: {e}")

"""
### 🌐 Esercizio 4: Scaricare Dati API
1.  Definisci la stringa dell'URL di un'API che risponde con dati in formato JSON (es. `https://api.github.com`).
2.  Esegui una richiesta HTTP (tipo GET) a questo URL per ottenere i dati.
3.  Controlla il codice di stato della risposta per assicurarti che la richiesta sia andata a buon fine (ad esempio, codice 200).
4.  Se la richiesta ha avuto successo, prendi il testo della risposta e decodificalo dal formato JSON in una struttura dati Python (probabilmente un dizionario).
5.  Stampa a schermo uno o due valori presi da questa struttura dati per verificare che i dati siano stati ricevuti e interpretati correttamente.
6.  Apri un nuovo file locale (es. `api_github.json`) in modalità scrittura.
7.  Scrivi l'intera struttura dati Python in quel file, formattandola come JSON leggibile (indentato).

---
"""

def esercizio4():
    """
    ### 🌐 Esercizio 4: Scaricare Dati API

    1.  Definisci la stringa dell'URL di un'API che risponde con dati in formato JSON (es. `https://api.github.com`).
    2.  Esegui una richiesta HTTP (tipo GET) a questo URL per ottenere i dati.
    3.  Controlla il codice di stato della risposta per assicurarti che la richiesta sia andata a buon fine (ad esempio, codice 200).
    4.  Se la richiesta ha avuto successo, prendi il testo della risposta e decodificalo dal formato JSON in una struttura dati Python (probabilmente un dizionario).
    5.  Stampa a schermo uno o due valori presi da questa struttura dati per verificare che i dati siano stati ricevuti e interpretati correttamente.
    6.  Apri un nuovo file locale (es. `api_github.json`) in modalità scrittura.
    7.  Scrivi l'intera struttura dati Python in quel file, formattandola come JSON leggibile (indentato).
    """
    try:
        # Usa l'API GitHub pubblica come esempio
        url = "https://api.github.com"
        print(f"Richiesta a: {url}")
        
        # Esegui la richiesta HTTP GET
        response = requests.get(url, timeout=10)
        
        # Controlla il codice di stato
        print(f"Codice di stato: {response.status_code}")
        
        if response.status_code == 200:
            # Decodifica il JSON
            data = response.json()
            
            # Stampa alcuni valori per verificare i dati
            print(f"Chiavi disponibili: {list(data.keys())}")
            if 'current_user_url' in data:
                print(f"URL utente corrente: {data['current_user_url']}")
            if 'current_user_authorizations_html_url' in data:
                print(f"URL autorizzazioni: {data['current_user_authorizations_html_url']}")
            
            # Salva in un file JSON
            output_file = 'api_github.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Dati salvati in '{output_file}'")
            
        else:
            print(f"Errore nella richiesta. Codice di stato: {response.status_code}")
            print(f"Risposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")
    except Exception as e:
        print(f"Errore generale: {e}")

def esercizio5():
    """
    ### 📈 Esercizio 5 (Avanzato): Calcolatore TF-IDF Semplificato

    1.  Crea tre file di testo (doc1.txt, doc2.txt, doc3.txt) con contenuti brevi e parzialmente sovrapposti (es. "Python è bello", "Java è veloce", "Python e Java").
    2.  **Fase 1: Calcolo TF (Term Frequency)**
    3.  Crea un dizionario principale vuoto per contenere le frequenze di tutti i documenti.
    4.  Per ciascuno dei 3 file:
    5.  Leggilo, puliscilo (minuscolo, senza punteggiatura) e dividilo in una lista di parole (come nell'Esercizio 1).
    6.  Calcola la *frequenza percentuale* (TF) di ogni parola *in quel file* (occorrenze / parole totali nel file).
    7.  Salva il dizionario risultante (parola -> TF%) nel dizionario principale, usando il nome del file come chiave.
    8.  **Fase 2: Calcolo IDF (Inverse Document Frequency)**
    9.  Conta il numero totale di documenti (in questo caso, 3).
    10. Censisci tutte le parole uniche apparse in tutti i documenti e, per ciascuna, conta in quanti documenti è apparsa (DF - Document Frequency).
    11. Crea un dizionario IDF. Per ogni parola unica, calcola il suo punteggio IDF applicando la formula logaritmica: log(numero_totale_documenti / numero_documenti_in_cui_appare).
    12. **Fase 3: Query**
    13. Definisci una lista di parole da cercare (es. ['python', 'java']).
    14. Calcola un punteggio finale per ogni documento: per ogni parola nella tua lista di ricerca, moltiplica il suo TF (preso dalla Fase 1) per il suo IDF (preso dalla Fase 2). Somma i risultati di tutte le parole della ricerca.
    15. Stampa i punteggi finali per i 3 documenti, per vedere quale è considerato più rilevante per la tua ricerca.
    """
    import math
    import glob
    
    # Crea file di esempio se non esistono
    sample_docs = {
        'doc1.txt': 'Python è bello e versatile. Python è usato per machine learning.',
        'doc2.txt': 'Java è veloce e affidabile. Java è usato per applicazioni enterprise.',
        'doc3.txt': 'Python e Java sono linguaggi popolari. Python e Java hanno caratteristiche diverse.'
    }
    
    # Crea i file di esempio se non esistono
    for filename, content in sample_docs.items():
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Creato file di esempio: {filename}")
    
    # Trova tutti i file .txt (documenti)
    doc_files = glob.glob('doc*.txt')
    if not doc_files:
        print("Nessun file doc*.txt trovato. Creazione file di esempio...")
        for filename, content in sample_docs.items():
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        doc_files = list(sample_docs.keys())
    
    # Fase 1: Calcolo TF (Term Frequency)
    tf_scores = {}
    all_words = set()
    
    for doc_file in doc_files:
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                text = f.read().lower()
            
            # Pulisci il testo (come nell'esercizio 1)
            non_alpha_chars = set(char for char in text if not char.isalpha())
            for char in non_alpha_chars:
                text = text.replace(char, ' ')
            words = text.split()
            
            # Calcola TF per ogni parola nel documento
            word_count = {}
            total_words = len(words)
            
            for word in words:
                word_count[word] = word_count.get(word, 0) + 1
                all_words.add(word)
            
            # Calcola frequenza percentuale (TF)
            tf_doc = {}
            for word, count in word_count.items():
                tf_doc[word] = count / total_words
            
            tf_scores[doc_file] = tf_doc
            
        except FileNotFoundError:
            print(f"File {doc_file} non trovato.")
            continue
    
    # Fase 2: Calcolo IDF (Inverse Document Frequency)
    total_docs = len(tf_scores)
    idf_scores = {}
    
    for word in all_words:
        doc_frequency = 0
        for doc_file in tf_scores:
            if word in tf_scores[doc_file]:
                doc_frequency += 1
        
        # Calcola IDF: log(total_docs / doc_frequency)
        idf_scores[word] = math.log(total_docs / doc_frequency) if doc_frequency > 0 else 0
    
    # Fase 3: Query
    query_words = input("Inserisci parole da cercare (separate da spazio, es: python java): ").lower().split()
    
    print(f"\nPunteggi TF-IDF per la query: {query_words}")
    print("-" * 50)
    
    final_scores = {}
    for doc_file in tf_scores:
        score = 0
        for word in query_words:
            tf = tf_scores[doc_file].get(word, 0)  # TF della parola nel documento
            idf = idf_scores.get(word, 0)  # IDF della parola
            tfidf = tf * idf  # Punteggio TF-IDF
            score += tfidf
        final_scores[doc_file] = score
        print(f"{doc_file}: {score:.4f}")
    
    # Trova il documento più rilevante
    if final_scores:
        best_doc = max(final_scores, key=final_scores.get)
        print(f"\nDocumento più rilevante: {best_doc} (punteggio: {final_scores[best_doc]:.4f})")
        
        # Mostra i dettagli del documento migliore
        print(f"\nContenuto di {best_doc}:")
        try:
            with open(best_doc, 'r', encoding='utf-8') as f:
                print(f.read())
        except FileNotFoundError:
            print("Contenuto non disponibile.")
    else:
        print("Nessun documento da analizzare.")

def main():
    """Funzione principale per testare tutti gli esercizi."""
    print("=== ESERCITAZIONE PYTHON ===")
    print("Esercizi disponibili:")
    print("1. Contatore di Frequenza Parole")
    print("2. Gestore di Spese in JSON")
    print("3. Scanner di File di Grandi Dimensioni")
    print("4. Scaricare Dati API")
    print("5. Calcolatore TF-IDF Semplificato")
    
    while True:
        try:
            choice = input("\nSeleziona un esercizio (1-5) o 'esci' per terminare: ").strip().lower()
            
            if choice == 'esci' or choice == 'exit':
                print("Arrivederci!")
                break
            elif choice == '1':
                esercizio1()
            elif choice == '2':
                esercizio2()
            elif choice == '3':
                esercizio3()
            elif choice == '4':
                esercizio4()
            elif choice == '5':
                esercizio5()
            else:
                print("Scelta non valida. Riprova.")
                
        except KeyboardInterrupt:
            print("\nArrivederci!")
            break
        except Exception as e:
            print(f"Errore: {e}")

if __name__ == "__main__":
    main()