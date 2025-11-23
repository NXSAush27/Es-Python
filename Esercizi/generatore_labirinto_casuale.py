"""
Algoritmo per generare labirinti casuali con percorso garantito
Crea un labirinto NxN che ha sempre almeno un percorso dal punto di partenza alla destinazione
"""

import random
from collections import deque

def genera_labirinto_con_percorso_garantito(dimensione=100, densita_ostacoli=0.3):
    """
    Genera un labirinto casuale che garantisce un percorso da (0,0) a (dimensione-1, dimensione-1)
    
    Args:
        dimensione: dimensione del labirinto (NxN)
        densita_ostacoli: percentuale di ostacoli aggiuntivi (0.0 - 1.0)
    
    Returns:
        labirinto: matrice NxN con 0 (libero) e 1 (ostacolo)
    """
    
    # Inizializza la matrice con tutti liberi
    labirinto = [[0 for _ in range(dimensione)] for _ in range(dimensione)]
    
    # Crea un percorso principale dal punto di partenza alla destinazione
    percorso_principale = crea_percorso_principale(dimensione)
    
    # Assicurati che il percorso principale sia costituito da celle libere
    for x, y in percorso_principale:
        labirinto[y][x] = 0
    
    # Aggiungi ostacoli casuali mantenendo il percorso libero
    aggiungi_ostacoli_mantenendo_percorso(labirinto, densita_ostacoli, percorso_principale)
    
    # Verifica che il percorso esista (debug)
    if not verifica_percorso_esiste(labirinto):
        print("ATTENZIONE: Percorso non trovato, rigenerazione...")
        return genera_labirinto_con_percorso_garantito(dimensione, densita_ostacoli)
    
    return labirinto

def crea_percorso_principale(dimensione):
    """
    Crea un percorso principale dal punto (0,0) al punto (dimensione-1, dimensione-1)
    usando un algoritmo che garantisce la connessione
    """
    percorso = [(0, 0)]
    x, y = 0, 0
    
    while (x, y) != (dimensione - 1, dimensione - 1):
        # Se siamo vicini alla fine, vai direttamente
        if x == dimensione - 2 and y == dimensione - 2:
            percorso.append((dimensione - 1, dimensione - 1))
            break
        
        Direzioni_Possibili = []
        
        # Dà priorità alle direzioni che ci avvicinano alla destinazione
        if x < dimensione - 1:
            Direzioni_Possibili.extend([(1, 0)] * 3)  # destra (più probabile)
        if y < dimensione - 1:
            Direzioni_Possibili.extend([(0, 1)] * 3)  # giù (più probabile)
            
        # Con piccola probabilità, movimento laterale per varietà
        if random.random() < 0.2 and x > 0:
            Direzioni_Possibili.append((-1, 0))  # sinistra
        if random.random() < 0.2 and y > 0:
            Direzioni_Possibili.append((0, -1))  # su
            
        if not Direzioni_Possibili:
            # Se non ci sono direzioni possibili, forza la direzione verso la fine
            if x < dimensione - 1:
                Direzioni_Possibili.append((1, 0))
            elif y < dimensione - 1:
                Direzioni_Possibili.append((0, 1))
            else:
                break
                
        # Scegli una direzione casuale dalle possibili
        dx, dy = random.choice(Direzioni_Possibili)
        
        # Calcola la nuova posizione
        nuovox, nuovoy = x + dx, y + dy
        
        # Assicurati di non uscire dai confini
        if 0 <= nuovox < dimensione and 0 <= nuovoy < dimensione:
            # Evita loop controllando se siamo già stati qui
            if (nuovox, nuovoy) not in percorso:
                x, y = nuovox, nuovoy
                percorso.append((x, y))
            else:
                # Se siamo in loop, forza movimento verso la destinazione
                if x < dimensione - 1:
                    x += 1
                elif y < dimensione - 1:
                    y += 1
                percorso.append((x, y))
        else:
            break
    
    # Assicurati che il percorso raggiunga la destinazione
    if percorso[-1] != (dimensione - 1, dimensione - 1):
        # Aggiungi un percorso diretto alla fine
        ultimo_x, ultimo_y = percorso[-1]
        while ultimo_x < dimensione - 1:
            ultimo_x += 1
            percorso.append((ultimo_x, ultimo_y))
        while ultimo_y < dimensione - 1:
            ultimo_y += 1
            percorso.append((ultimo_x, ultimo_y))
    
    return percorso

def aggiungi_percorsi_alternativi(labirinto, dimensione, densita):
    """
    Aggiunge percorsi alternativi casuali per rendere il labirinto più interessante
    """
    numero_percorsi = int(dimensione * 0.5)  # Circa mezzo percorso per ogni riga
    
    for _ in range(numero_percorsi):
        # Inizia da una cella casuale del percorso principale
        start_x = random.randint(0, dimensione - 1)
        start_y = random.randint(0, dimensione - 1)
        
        # Assicurati che la cella di partenza sia libera
        if labirinto[start_y][start_x] == 0:
            # Crea un piccolo percorso alternativo
            crea_percorso_alternativo(labirinto, start_x, start_y, densita)

def crea_percorso_alternativo(labirinto, start_x, start_y, densita):
    """
    Crea un piccolo percorso alternativo partendo da una posizione data
    """
    x, y = start_x, start_y
    lunghezza_max = random.randint(3, 8)
    
    for _ in range(lunghezza_max):
        Direzioni = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(Direzioni)
        
        mosso = False
        for dx, dy in Direzioni:
            nuovox, nuovoy = x + dx, y + dy
            
            if (0 <= nuovox < len(labirinto) and 0 <= nuovoy < len(labirinto[0]) and 
                labirinto[nuovoy][nuovox] == 1):  # Solo se è un ostacolo
                
                # Con una probabilità basata sulla densità, rendi questa cella libera
                if random.random() < (1 - densita):
                    labirinto[nuovoy][nuovox] = 0
                    x, y = nuovox, nuovoy
                    mosso = True
                    break
        
        if not mosso:
            break

def aggiungi_ostacoli_mantenendo_percorso(labirinto, densita_ostacoli, percorso_principale):
    """
    Aggiunge ostacoli casuali mantenendo sempre libero il percorso principale
    """
    dimensione = len(labirinto)
    
    # Crea un set delle coordinate del percorso principale per controllo veloce
    percorso_set = set(percorso_principale)
    
    for y in range(dimensione):
        for x in range(dimensione):
            # Non aggiungere ostacoli nelle celle del percorso principale
            if (x, y) in percorso_set:
                continue
                
            # Aggiungi ostacoli con la densità specificata
            if random.random() < densita_ostacoli:
                labirinto[y][x] = 1

def verifica_non_blocco(labirinto, x, y):
    """
    Verifica che l'aggiunta di un ostacolo in (x,y) non blocchi completamente i percorsi
    """
    # Semplice verifica: non aggiungere ostacoli se isolano una cella libera
    dimensione = len(labirinto)
    
    # Conta le celle libere adiacenti
    celle_libere_ad = 0
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < dimensione and 0 <= ny < dimensione:
            if labirinto[ny][nx] == 0:
                celle_libere_ad += 1
    
    # Non aggiungere ostacoli se la cella ha meno di 2 vicini liberi
    return celle_libere_ad >= 2

def verifica_percorso_esiste(labirinto, start=(0, 0), end=None):
    """
    Verifica se esiste un percorso dal punto start al punto end usando BFS
    """
    if end is None:
        end = (len(labirinto) - 1, len(labirinto) - 1)
    
    dimensione = len(labirinto)
    queue = deque([start])
    visited = set([start])
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == end:
            return True
            
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < dimensione and 0 <= ny < dimensione and 
                labirinto[ny][nx] == 0 and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny))
    
    return False

def stampa_statistiche_labirinto(labirinto):
    """
    Stampa le statistiche del labirinto
    """
    celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
    dimensione = len(labirinto)
    
    print(f"Dimensioni: {dimensione}x{dimensione}")
    print(f"Celle libere (0): {celle_libere}")
    print(f"Ostacoli (1): {ostacoli}")
    print(f"Percentuale ostacoli: {ostacoli/(celle_libere+ostacoli)*100:.1f}%")
    
    # Verifica che esista un percorso
    percorso_ok = verifica_percorso_esiste(labirinto)
    print(f"Percorso garantito: {'Sì' if percorso_ok else 'No'}")

# Esempio di utilizzo
if __name__ == "__main__":
    print("Generazione di labirinti casuali con percorso garantito...")
    
    # Genera diversi labirinti con diverse densità
    for densita in [0.1, 0.2, 0.3]:
        print(f"\n=== Labirinto con densità ostacoli {densita} ===")
        labirinto = genera_labirinto_con_percorso_garantito(dimensione=20, densita_ostacoli=densita)
        stampa_statistiche_labirinto(labirinto)