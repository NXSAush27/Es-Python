"""
ALGORITMO LABIRINTO CON UN SOLO PERCORSO VINCENTE
Crea labirinti sfida con percorsi multipli ma solo una soluzione corretta
"""

import random
from collections import deque

def genera_labirinto_unico_percorso(dimensione=100, densita_ostacoli=0.35, complessita=0.7):
    """
    Genera un labirinto con UN SOLO percorso vincente dal punto di partenza alla fine
    
    Args:
        dimensione: dimensione del labirinto (NxN)
        densita_ostacoli: percentuale di ostacoli
        complessita: livello di complessità dei falsi percorsi
    
    Returns:
        labirinto: matrice NxN con esattamente un percorso vincente
    """
    
    # Inizializza con tutte celle libere per maggiore flessibilità
    labirinto = [[0 for _ in range(dimensione)] for _ in range(dimensione)]
    
    # Fase 1: Crea il percorso principale unico
    percorso_principale = crea_percorso_principale_unico(labirinto, dimensione)
    
    # Fase 2: Aggiungi falsi percorsi e vicoli ciechi PRIMA di chiudere
    aggiungi_falsi_percorsi(labirinto, percorso_principale, complessita)
    
    # Fase 3: Chiudi solo i percorsi che portano direttamente alla fine
    chiudi_percorsi_diretti(labirinto, percorso_principale)
    
    # Fase 4: Aggiungi ostacoli per creare labirinto bilanciato
    aggiungi_ostacoli_bilanciati(labirinto, densita_ostacoli)
    
    # Verifica che esista esattamente un percorso
    percorsi = trova_tutti_percorsi(labirinto)
    if len(percorsi) != 1:
        # Se non c'è esattamente un percorso, rigenera con parametri più conservativi
        return genera_labirinto_unico_percorso(dimensione, densita_ostacoli * 0.8, complessita * 0.7)
    
    return labirinto

def crea_percorso_principale_unico(labirinto, dimensione):
    """
    Crea un percorso principale serpente dal punto (0,0) alla fine
    """
    percorso = [(0, 0)]
    x, y = 0, 0
    
    # Assicura che l'inizio sia libero
    labirinto[0][0] = 0
    
    while (x, y) != (dimensione - 1, dimensione - 1):
        # Crea movimento serpente intelligente
        Direzioni_Possibili = []
        
        # Priorità verso la fine con movimento serpente
        if x < dimensione - 2:  # Non andare troppo a destra
            Direzioni_Possibili.append((1, 0))  # Destra
        if y < dimensione - 2:  # Non andare troppo in basso
            Direzioni_Possibili.append((0, 1))  # Giù
            
        # Movimento laterale per creare serpentina
        if random.random() < 0.4:
            if x > 1:
                Direzioni_Possibili.append((-1, 0))  # Sinistra
            if y > 1:
                Direzioni_Possibili.append((0, -1))  # Su
        
        if not Direzioni_Possibili:
            break
            
        dx, dy = random.choice(Direzioni_Possibili)
        nuovox, nuovoy = x + dx, y + dy
        
        # Verifica confini e evita loop
        if (0 <= nuovox < dimensione and 0 <= nuovoy < dimensione and 
            (nuovox, nuovoy) not in percorso):
            x, y = nuovox, nuovoy
            percorso.append((x, y))
            labirinto[y][x] = 0  # Assicura che sia libero
        else:
            # Movimento forzato verso la fine
            if x < dimensione - 1:
                x += 1
            elif y < dimensione - 1:
                y += 1
            percorso.append((x, y))
            labirinto[y][x] = 0
    
    # Assicura di raggiungere la fine
    if percorso[-1] != (dimensione - 1, dimensione - 1):
        ultimo_x, ultimo_y = percorso[-1]
        while ultimo_x < dimensione - 1:
            ultimo_x += 1
            percorso.append((ultimo_x, ultimo_y))
            labirinto[ultimo_y][ultimo_x] = 0
        while ultimo_y < dimensione - 1:
            ultimo_y += 1
            percorso.append((ultimo_x, ultimo_y))
            labirinto[ultimo_y][ultimo_x] = 0
    
    return percorso

def chiudi_percorsi_diretti(labirinto, percorso_principale):
    """
    Chiude solo i percorsi che portano direttamente alla fine bypassing il percorso principale
    """
    dimensione = len(labirinto)
    percorso_set = set(percorso_principale)
    
    # Chiudi solo le celle che potrebbero creare scorciatoie dirette
    for y in range(1, dimensione - 1):
        for x in range(1, dimensione - 1):
            if labirinto[y][x] == 0 and (x, y) not in percorso_set:
                # Se questa cella è vicina alla fine e ha molti vicini, potrebbe essere pericolosa
                if vicino_alla_fine(x, y, dimensione) and molti_vicini_liberi(labirinto, x, y, 3):
                    # Chiudi con una piccola probabilità
                    if random.random() < 0.3:
                        labirinto[y][x] = 1

def vicino_alla_fine(x, y, dimensione):
    """Verifica se una cella è vicina alla destinazione"""
    return x >= dimensione - 5 or y >= dimensione - 5

def molti_vicini_liberi(labirinto, x, y, soglia):
    """Conta se una cella ha molti vicini liberi"""
    count = 0
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]) and
            labirinto[ny][nx] == 0):
            count += 1
    return count >= soglia

def aggiungi_falsi_percorsi(labirinto, percorso_principale, complessita):
    """
    Aggiunge falsi percorsi che sembrano promettenti ma non portano alla fine
    """
    dimensione = len(labirinto)
    percorso_set = set(percorso_principale)
    
    # Più falsi percorsi per rendere il labirinto più interessante
    numero_falsi = int(len(percorso_principale) * complessita * 0.5)
    
    for _ in range(numero_falsi):
        # Scegli punto di partenza dal percorso principale
        punto_partenza = random.choice(percorso_principale)
        crea_falso_percorso(labirinto, punto_partenza, percorso_set)
    
    # Aggiungi anche alcuni falsi percorsi che partono da celle libere casuali
    numero_falsi_extra = int(numero_falsi * 0.3)
    for _ in range(numero_falsi_extra):
        punto_partenza = trova_cella_libera_casuale(labirinto, percorso_set)
        if punto_partenza:
            crea_falso_percorso(labirinto, punto_partenza, percorso_set)

def trova_cella_libera_casuale(labirinto, percorso_set):
    """Trova una cella libera casuale per iniziare un falso percorso"""
    dimensione = len(labirinto)
    for _ in range(50):  # Tentativi limitati
        x = random.randint(1, dimensione - 2)
        y = random.randint(1, dimensione - 2)
        if labirinto[y][x] == 0 and (x, y) not in percorso_set:
            return (x, y)
    return None

def crea_falso_percorso(labirinto, punto_partenza, percorso_set):
    """
    Crea un falso percorso che sembra portare verso la fine
    """
    x, y = punto_partenza
    dimensione = len(labirinto)
    
    lunghezza_falso = random.randint(5, 20)
    direzione = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    for _ in range(lunghezza_falso):
        nuovox, nuovoy = x + direzione[0], y + direzione[1]
        
        # Verifica confini e se la cella è già occupata
        if (0 <= nuovox < dimensione and 0 <= nuovoy < dimensione and 
            labirinto[nuovoy][nuovox] == 0 and
            (nuovox, nuovoy) not in percorso_set):
            
            x, y = nuovox, nuovoy
            
            # Occasionalmente crea rami dal falso percorso
            if random.random() < 0.3:
                crea_ramo_finto(labirinto, x, y, percorso_set)
            
            # Possibilità di curvare
            if random.random() < 0.4:
                nuove_direzioni = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if direzione in nuove_direzioni:
                    nuove_direzioni.remove(direzione)
                direzione = random.choice(nuove_direzioni)
        else:
            break

def crea_ramo_finto(labirinto, x, y, percorso_set):
    """
    Crea un piccolo ramo da un falso percorso
    """
    dimensione = len(labirinto)
    direzione = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    lunghezza = random.randint(2, 8)
    
    for _ in range(lunghezza):
        nuovox, nuovoy = x + direzione[0], y + direzione[1]
        
        if (0 <= nuovox < dimensione and 0 <= nuovoy < dimensione and 
            labirinto[nuovoy][nuovox] == 0 and
            (nuovox, nuovoy) not in percorso_set):
            
            x, y = nuovox, nuovoy
            
            # Termina occasionalmente per creare vicolo cieco
            if random.random() < 0.4:
                break
        else:
            break

def aggiungi_ostacoli_bilanciati(labirinto, densita):
    """
    Aggiunge ostacoli in modo bilanciato per creare un labirinto interessante
    """
    dimensione = len(labirinto)
    celle_libere_attuali = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    celle_totali = dimensione * dimensione
    
    # Calcola numero target di ostacoli per una densità bilanciata
    target_ostacoli = int(celle_totali * densita * 0.3)  # Molto meno aggressivo
    ostacoli_attuali = celle_totali - celle_libere_attuali
    ostacoli_da_aggiungere = max(0, target_ostacoli - ostacoli_attuali)
    
    for _ in range(ostacoli_da_aggiungere):
        x = random.randint(1, dimensione - 2)
        y = random.randint(1, dimensione - 2)
        
        if labirinto[y][x] == 0 and ostacolo_sicuro(labirinto, x, y):
            labirinto[y][x] = 1

def ostacolo_sicuro(labirinto, x, y):
    """
    Verifica se aggiungere un ostacolo è sicuro
    """
    # Non aggiungere ostacoli se isolano celle o creano percorsi alternativi
    vicini_liberi = 0
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]) and
            labirinto[ny][nx] == 0):
            vicini_liberi += 1
    
    # Più permissivo: permette ostacoli con almeno 2 vicini liberi
    return vicini_liberi >= 2

def trova_tutti_percorsi(labirinto, start=(0, 0), end=None):
    """
    Trova TUTTI i percorsi possibili dal start alla fine
    """
    if end is None:
        end = (len(labirinto) - 1, len(labirinto) - 1)
    
    if (labirinto[start[1]][start[0]] == 1 or 
        labirinto[end[1]][end[0]] == 1):
        return []
    
    paths = []
    visited = set()
    
    def dfs(x, y, current_path):
        if (x, y) == end:
            paths.append(current_path[:])
            return
        
        visited.add((x, y))
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]) and 
                labirinto[ny][nx] == 0 and (nx, ny) not in visited):
                current_path.append((nx, ny))
                dfs(nx, ny, current_path)
                current_path.pop()
        
        visited.remove((x, y))
    
    dfs(start[0], start[1], [start])
    return paths

def analizza_labirinto_unico(labirinto):
    """
    Analizza un labirinto per verificare che abbia un solo percorso
    """
    percorsi = trova_tutti_percorsi(labirinto)
    
    celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
    
    # Conta vicoli ciechi
    vicoli_ciechi = 0
    for y in range(1, len(labirinto) - 1):
        for x in range(1, len(labirinto[0]) - 1):
            if labirinto[y][x] == 0:
                vicini_liberi = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if labirinto[y + dy][x + dx] == 0:
                        vicini_liberi += 1
                
                if vicini_liberi == 1:
                    vicoli_ciechi += 1
    
    return {
        'celle_libere': celle_libere,
        'ostacoli': ostacoli,
        'vicoli_ciechi': vicoli_ciechi,
        'percentuale_ostacoli': round(ostacoli/(celle_libere+ostacoli)*100, 1),
        'numero_percorsi': len(percorsi),
        'lunghezza_percorso': len(percorsi[0]) if percorsi else 0,
        'unico_percorso': len(percorsi) == 1
    }

# Test dell'algoritmo
if __name__ == "__main__":
    print("=== GENERATORE LABIRINTI CON UN SOLO PERCORSO ===")
    
    for dim in [20, 30]:
        print(f"\n--- Labirinto {dim}x{dim} ---")
        labirinto = genera_labirinto_unico_percorso(dim, 0.3, 0.7)
        stats = analizza_labirinto_unico(labirinto)
        
        print(f"Celle libere: {stats['celle_libere']}")
        print(f"Ostacoli: {stats['ostacoli']} ({stats['percentuale_ostacoli']}%)")
        print(f"Vicoli ciechi: {stats['vicoli_ciechi']}")
        print(f"Numero percorsi totali: {stats['numero_percorsi']}")
        print(f"Lunghezza percorso vincente: {stats['lunghezza_percorso']}")
        print(f"Unico percorso: {'SI' if stats['unico_percorso'] else 'NO'}")
        
        # Mostra preview
        print("Preview (5x5):")
        for y in range(5):
            riga = ""
            for x in range(5):
                if x == 0 and y == 0:
                    riga += "S"  # Start
                elif x == dim-1 and y == dim-1:
                    riga += "E"  # End
                elif labirinto[y][x] == 1:
                    riga += "#"  # Ostacolo
                else:
                    riga += "."  # Libero
            print(f"  {riga}")
        print()