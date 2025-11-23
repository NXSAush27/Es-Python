"""
Algoritmo avanzato per generazione labirinti realistici con vicoli ciechi e percorsi multipli
Crea labirinti complessi e meno prevedibili mantenendo il percorso garantito
"""

import random
from collections import deque
import copy

def genera_labirinto_realistico(dimensione=100, densita_ostacoli=0.35, complessita=0.7):
    """
    Genera un labirinto realistico con percorsi multipli e vicoli ciechi
    
    Args:
        dimensione: dimensione del labirinto (NxN)
        densita_ostacoli: percentuale di ostacoli (0.0 - 1.0)
        complessita: livello di complessità dei vicoli ciechi (0.0 - 1.0)
    
    Returns:
        labirinto: matrice NxN con 0 (libero) e 1 (ostacolo)
    """
    
    # Inizializza il labirinto con tutte celle libere
    labirinto = [[0 for _ in range(dimensione)] for _ in range(dimensione)]
    
    # Fase 1: Genera il percorso principale serpente
    percorso_principale = genera_percorso_serpente(dimensione)
    
    # Fase 2: Crea il sistema di corridoi principali
    crea_corridoi_principali(labirinto, percorso_principale)
    
    # Fase 3: Aggiungi rami e vicoli ciechi estesi
    aggiungi_rami_e_vicoli_ciechi(labirinto, percorso_principale, complessita)
    
    # Fase 4: Aggiungi ostacoli selettivi per creare sfide
    aggiungi_ostacoli_selettivi(labirinto, densita_ostacoli)
    
    # Fase 5: Crea zone più complesse
    crea_zone_labirintiche(labirinto, complessita)
    
    # Fase 5: Verifica e ottimizza
    if not verifica_percorso_esiste(labirinto):
        # Se non c'è percorso, rigenera con minore complessità
        return genera_labirinto_realistico(dimensione, densita_ostacoli * 0.8, complessita * 0.7)
    
    return labirinto

def genera_percorso_serpente(dimensione):
    """
    Genera un percorso principale serpente più complesso e meno prevedibile
    """
    percorso = [(0, 0)]
    x, y = 0, 0
    
    while (x, y) != (dimensione - 1, dimensione - 1):
        Direzioni_Possibili = []
        
        # Direzioni principali verso la destinazione
        if x < dimensione - 1:
            Direzioni_Possibili.extend([(1, 0)] * 2)  # Destra più probabile
        if y < dimensione - 1:
            Direzioni_Possibili.extend([(0, 1)] * 2)  # Giù più probabile
            
        # Movimenti laterali per creare serpentina
        if random.random() < 0.4 and x > 1:
            Direzioni_Possibili.append((-1, 0))  # Sinistra
        if random.random() < 0.4 and y > 1:
            Direzioni_Possibili.append((0, -1))  # Su
            
        # Movimenti casuali per varietà
        if random.random() < 0.2:
            Direzioni_Possibili.extend([(1, 0), (0, 1)])
            
        if not Direzioni_Possibili:
            break
            
        # Scegli direzione
        dx, dy = random.choice(Direzioni_Possibili)
        nuovox, nuovoy = x + dx, y + dy
        
        # Verifica confini
        if 0 <= nuovox < dimensione and 0 <= nuovoy < dimensione:
            # Evita loop
            if (nuovox, nuovoy) not in percorso:
                x, y = nuovox, nuovoy
                percorso.append((x, y))
            else:
                # Se in loop, cerca un'uscita
                if x < dimensione - 1:
                    x += 1
                elif y < dimensione - 1:
                    y += 1
                percorso.append((x, y))
    
    # Assicura di raggiungere la fine
    if percorso[-1] != (dimensione - 1, dimensione - 1):
        ultimo_x, ultimo_y = percorso[-1]
        while ultimo_x < dimensione - 1:
            ultimo_x += 1
            percorso.append((ultimo_x, ultimo_y))
        while ultimo_y < dimensione - 1:
            ultimo_y += 1
            percorso.append((ultimo_x, ultimo_y))
    
    return percorso

def crea_corridoi_principali(labirinto, percorso_principale):
    """
    Crea il sistema di corridoi principali con larghezza variabile
    """
    for x, y in percorso_principale:
        # Assicurati che la cella principale sia libera
        labirinto[y][x] = 0
        
        # Crea corridoi più larghi per i percorsi principali
        if random.random() < 0.7:  # 70% di probabilità di allargare
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]) and 
                    random.random() < 0.6):  # 60% di probabilità di allargare
                    labirinto[ny][nx] = 0

def aggiungi_rami_e_vicoli_ciechi(labirinto, percorso_principale, complessita):
    """
    Aggiunge rami secondari e vicoli ciechi dal percorso principale
    """
    dimensione = len(labirinto)
    percorso_set = set(percorso_principale)
    
    # Aumenta significativamente il numero di rami
    numero_rami = int(len(percorso_principale) * complessita * 0.5)  # Più rami
    
    for _ in range(numero_rami):
        # Più varietà nei punti di partenza
        if random.random() < 0.5:  # 50% dal percorso principale
            punto_partenza = random.choice(percorso_principale)
        elif random.random() < 0.5:  # 25% da celle libere adiacenti
            punto_partenza = trova_cella_libera_casuale(labirinto, percorso_set)
        else:  # 25% crea rami in aree aperte
            punto_partenza = trova_area_aperta_per_ramo(labirinto)
            
        if punto_partenza:
            # Crea rami più lunghi e complessi
            for _ in range(random.randint(1, 3)):  # 1-3 rami per punto di partenza
                crea_vicolo_cieco_esteso(labirinto, punto_partenza, complessita)

def trova_cella_libera_casuale(labirinto, percorso_set):
    """
    Trova una cella libera casuale per iniziare un vicolo cieco
    """
    dimensione = len(labirinto)
    tentativi = 0
    while tentativi < 50:
        x = random.randint(1, dimensione - 2)
        y = random.randint(1, dimensione - 2)
        
        if labirinto[y][x] == 0 and (x, y) not in percorso_set:
            return (x, y)
        tentativi += 1
    
    return None

def crea_vicolo_cieco(labirinto, punto_partenza, complessita):
    """
    Crea un vicolo cieco che parte da un punto dato
    """
    x, y = punto_partenza
    dimensione = len(labirinto)
    
    lunghezza_vicolo = random.randint(2, int(10 * complessita) + 2)
    direzione = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    for _ in range(lunghezza_vicolo):
        # Calcola nuova posizione
        nuovox, nuovoy = x + direzione[0], y + direzione[1]
        
        # Verifica confini e ostacoli
        if (0 <= nuovox < dimensione and 0 <= nuovoy < dimensione and 
            labirinto[nuovoy][nuovox] == 1):
            
            labirinto[nuovoy][nuovox] = 0
            x, y = nuovox, nuovoy
            
            # Possibilità di curvare il vicolo
            if random.random() < 0.3:
                nuove_direzioni = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                nuove_direzioni.remove(direzione)  # Rimuovi direzione corrente
                direzione = random.choice(nuove_direzioni)
        else:
            break

def aggiungi_ostacoli_selettivi(labirinto, densita_ostacoli):
    """
    Aggiunge ostacoli selettivi per creare sfide senza bloccare i percorsi
    """
    dimensione = len(labirinto)
    numero_ostacoli = int(dimensione * dimensione * densita_ostacoli * 0.05)  # Molto meno aggressivo
    
    for _ in range(numero_ostacoli):
        x = random.randint(1, dimensione - 2)
        y = random.randint(1, dimensione - 2)
        
        # Aggiungi ostacoli solo se non isolano celle
        if labirinto[y][x] == 0 and puo_diventare_ostacolo(labirinto, x, y):
            labirinto[y][x] = 1

def crea_zone_labirintiche(labirinto, complessita):
    """
    Crea zone più labirintiche con pattern complessi
    """
    dimensione = len(labirinto)
    numero_zone = int(dimensione * complessita * 0.02)
    
    for _ in range(numero_zone):
        centro_x = random.randint(3, dimensione - 4)
        centro_y = random.randint(3, dimensione - 4)
        grandezza = random.randint(2, 5)
        
        crea_parete_labirintica(labirinto, centro_x, centro_y, grandezza, complessita)

def trova_area_aperta_per_ramo(labirinto):
    """
    Trova un'area aperta con molte celle libere per iniziare un ramo
    """
    dimensione = len(labirinto)
    migliore_punteggio = 0
    migliore_posizione = None
    
    for y in range(2, dimensione - 2):
        for x in range(2, dimensione - 2):
            if labirinto[y][x] == 0:
                punteggio = conta_celle_libere_vicino(labirinto, x, y)
                if punteggio >= 3 and punteggio > migliore_punteggio:
                    migliore_punteggio = punteggio
                    migliore_posizione = (x, y)
    
    return migliore_posizione

def crea_vicolo_cieco_esteso(labirinto, punto_partenza, complessita):
    """
    Crea un vicolo cieco più complesso e ramificato
    """
    x, y = punto_partenza
    dimensione = len(labirinto)
    
    # Lunghezza variabile del vicolo
    lunghezza_vicolo = random.randint(3, int(15 * complessita) + 3)
    direzione = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    for _ in range(lunghezza_vicolo):
        nuovox, nuovoy = x + direzione[0], y + direzione[1]
        
        if (0 <= nuovox < dimensione and 0 <= nuovoy < dimensione and 
            labirinto[nuovoy][nuovox] == 0):
            
            x, y = nuovox, nuovoy
            
            # Possibilità di creare rami secondari
            if random.random() < 0.4:
                crea_ramo_secondario(labirinto, x, y, complessita)
            
            # Possibilità di curvare
            if random.random() < 0.5:
                nuove_direzioni = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if direzione in nuove_direzioni:
                    nuove_direzioni.remove(direzione)
                direzione = random.choice(nuove_direzioni)
        else:
            break

def crea_ramo_secondario(labirinto, x, y, complessita):
    """
    Crea un piccolo ramo secondario dal vicolo principale
    """
    dimensione = len(labirinto)
    direzione = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    lunghezza = random.randint(1, int(5 * complessita) + 1)
    
    for _ in range(lunghezza):
        nuovox, nuovoy = x + direzione[0], y + direzione[1]
        
        if (0 <= nuovox < dimensione and 0 <= nuovoy < dimensione and 
            labirinto[nuovoy][nuovox] == 0):
            
            x, y = nuovox, nuovoy
            
            # Termina il ramo occasionalmente per creare vicoli ciechi
            if random.random() < 0.3:
                break
        else:
            break

def puo_diventare_ostacolo(labirinto, x, y):
    """
    Verifica se una cella può diventare ostacolo senza isolare l'area
    """
    dimensione = len(labirinto)
    celle_libere_vicino = 0
    
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < dimensione and 0 <= ny < dimensione and
            labirinto[ny][nx] == 0):
            celle_libere_vicino += 1
    
    # Può diventare ostacolo se ha almeno 3 vicini liberi
    return celle_libere_vicino >= 3

def conta_celle_libere_vicino(labirinto, x, y):
    """
    Conta le celle libere adiacenti
    """
    dimensione = len(labirinto)
    count = 0
    
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < dimensione and 0 <= ny < dimensione and
            labirinto[ny][nx] == 0):
            count += 1
    
    return count

def crea_parete_labirintica(labirinto, centro_x, centro_y, grandezza, complessita):
    """
    Crea pattern labirintici con pareti e corridoi
    """
    dimensione = len(labirinto)
    
    # Crea una piccola sezione labirintica
    for dy in range(-grandezza, grandezza + 1):
        for dx in range(-grandezza, grandezza + 1):
            x, y = centro_x + dx, centro_y + dy
            
            if (0 <= x < dimensione and 0 <= y < dimensione and
                labirinto[y][x] == 0):
                
                # Pattern labirintico: create ostacoli in pattern
                if (dx + dy) % 3 == 0 and random.random() < 0.6:
                    labirinto[y][x] = 1
                elif (dx * dy) % 2 == 0 and random.random() < 0.3:
                    labirinto[y][x] = 1

def verifica_percorso_esiste(labirinto, start=(0, 0), end=None):
    """
    Verifica se esiste un percorso usando BFS
    """
    if end is None:
        end = (len(labirinto) - 1, len(labirinto) - 1)
    
    if labirinto[start[1]][start[0]] == 1 or labirinto[end[1]][end[0]] == 1:
        return False
    
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

def conta_vicoli_ciechi(labirinto):
    """
    Conta il numero di vicoli ciechi (celle libere con 1 solo vicino libero)
    """
    vicoli_ciechi = 0
    dimensione = len(labirinto)
    
    for y in range(1, dimensione - 1):
        for x in range(1, dimensione - 1):
            if labirinto[y][x] == 0:  # Se è una cella libera
                celle_libere_vicino = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if labirinto[ny][nx] == 0:
                        celle_libere_vicino += 1
                
                if celle_libere_vicino == 1:  # Vicolo cieco
                    vicoli_ciechi += 1
    
    return vicoli_ciechi

def analizza_complessita_labirinto(labirinto):
    """
    Analizza la complessità del labirinto
    """
    celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
    vicoli_ciechi = conta_vicoli_ciechi(labirinto)
    
    # Calcola connettività (quante celle libere sono connesse)
    celle_connesse = 0
    if verifica_percorso_esiste(labirinto):
        # BFS per contare celle connesse al punto di partenza
        dimensione = len(labirinto)
        queue = deque([(0, 0)])
        visited = set([(0, 0)])
        
        while queue:
            x, y = queue.popleft()
            celle_connesse += 1
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < dimensione and 0 <= ny < dimensione and 
                    labirinto[ny][nx] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    
    return {
        'celle_libere': celle_libere,
        'ostacoli': ostacoli,
        'vicoli_ciechi': vicoli_ciechi,
        'percentuale_ostacoli': round(ostacoli/(celle_libere+ostacoli)*100, 1),
        'percentuale_connesse': round(celle_connesse/celle_libere*100, 1) if celle_libere > 0 else 0,
        'percorsi_multipli': 'Sì' if celle_connesse > celle_libere * 0.8 else 'No'
    }

# Test dell'algoritmo migliorato
if __name__ == "__main__":
    print("=== GENERATORE LABIRINTI REALISTICI AVANZATO ===")
    
    for complessita in [0.3, 0.6, 0.9]:
        print(f"\n--- Complessità: {complessita} ---")
        labirinto = genera_labirinto_realistico(dimensione=30, densita_ostacoli=0.35, complessita=complessita)
        
        stats = analizza_complessita_labirinto(labirinto)
        print(f"Dimensioni: 30x30")
        print(f"Celle libere: {stats['celle_libere']}")
        print(f"Ostacoli: {stats['ostacoli']} ({stats['percentuale_ostacoli']}%)")
        print(f"Vicoli ciechi: {stats['vicoli_ciechi']}")
        print(f"Celle connesse: {stats['percentuale_connesse']}%")
        print(f"Percorsi multipli: {stats['percorsi_multipli']}")
        print(f"Percorso garantito: {'Sì' if verifica_percorso_esiste(labirinto) else 'No'}")