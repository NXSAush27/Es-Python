"""
Algoritmo di generazione labirinti bilanciato con percorsi complessi e vicoli ciechi
Basato su algoritmi classici di maze generation con miglioramenti per vicoli ciechi
"""

import random
from collections import deque

def genera_labirinto_bilanciato(dimensione=100, densita_ostacoli=0.35, complessita=0.7):
    """
    Genera un labirinto bilanciato con percorsi multipli e vicoli ciechi
    """
    # Inizializza tutto come ostacoli (stile Recursive Division)
    labirinto = [[1 for _ in range(dimensione)] for _ in range(dimensione)]
    
    # Fase 1: Crea il sistema base di corridoi
    crea_sistema_corridoi_base(labirinto, densita_ostacoli)
    
    # Fase 2: Aggiungi il percorso principale garantito
    percorso_principale = crea_percorso_garantito(labirinto)
    
    # Fase 3: Espandi e crea vicoli ciechi
    espandi_e_complica_labirinto(labirinto, percorso_principale, complessita)
    
    # Fase 4: Aggiungi ostacoli strategici finali
    aggiungi_ostacoli_finali(labirinto, densita_ostacoli * 0.5)
    
    # Verifica e correggi se necessario
    if not verifica_percorso_esiste(labirinto):
        return genera_labirinto_bilanciato(dimensione, densita_ostacoli * 0.8, complessita * 0.8)
    
    return labirinto

def crea_sistema_corridoi_base(labirinto, densita_ostacoli):
    """
    Crea il sistema base di corridoi con pattern serpentino
    """
    dimensione = len(labirinto)
    
    # Crea corridoi orizzontali e verticali
    for y in range(0, dimensione, 2):  # Ogni 2 righe
        for x in range(0, dimensione):
            if random.random() < 0.7:  # 70% di probabilità
                labirinto[y][x] = 0
    
    for x in range(0, dimensione, 2):  # Ogni 2 colonne
        for y in range(0, dimensione):
            if random.random() < 0.7:  # 70% di probabilità
                labirinto[y][x] = 0
    
    # Aggiungi connessioni casuali tra i corridoi
    for y in range(1, dimensione - 1):
        for x in range(1, dimensione - 1):
            if labirinto[y][x] == 1 and random.random() < 0.1:  # 10% connessioni
                # Crea connessioni che mantengono连通性
                vicini_liberi = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < dimensione and 0 <= ny < dimensione:
                        if labirinto[ny][nx] == 0:
                            vicini_liberi += 1
                
                if vicini_liberi >= 2:
                    labirinto[y][x] = 0

def crea_percorso_garantito(labirinto):
    """
    Crea un percorso garantito dal punto (0,0) alla destinazione
    """
    dimensione = len(labirinto)
    percorso = [(0, 0)]
    labirinto[0][0] = 0  # Assicura che l'inizio sia libero
    
    x, y = 0, 0
    
    # Algoritmo che garantisce un percorso verso la destinazione
    while (x, y) != (dimensione - 1, dimensione - 1):
        Direzioni_Preferite = []
        
        # Priorità alle direzioni verso la destinazione
        if x < dimensione - 1 and labirinto[y][x + 1] == 0:
            Direzioni_Preferite.append((1, 0))
        if y < dimensione - 1 and labirinto[y + 1][x] == 0:
            Direzioni_Preferite.append((0, 1))
        
        # Se non ci sono direzioni verso celle libere, creane una
        if not Direzioni_Preferite:
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < dimensione and 0 <= ny < dimensione:
                    if labirinto[ny][nx] == 1:
                        labirinto[ny][nx] = 0  # Libera la cella
                        Direzioni_Preferite.append((dx, dy))
                        break
        
        if not Direzioni_Preferite:
            break
            
        dx, dy = random.choice(Direzioni_Preferite)
        x += dx
        y += dy
        percorso.append((x, y))
    
    # Assicura di raggiungere la destinazione
    if (x, y) != (dimensione - 1, dimensione - 1):
        # Libera il percorso diretto alla fine
        while x < dimensione - 1:
            x += 1
            labirinto[y][x] = 0
            percorso.append((x, y))
        while y < dimensione - 1:
            y += 1
            labirinto[x][y] = 0
            percorso.append((x, y))
    
    return percorso

def espandi_e_complica_labirinto(labirinto, percorso_principale, complessita):
    """
    Espande il labirinto aggiungendo rami e vicoli ciechi
    """
    dimensione = len(labirinto)
    percorso_set = set(percorso_principale)
    
    # Numero di rami basato sulla complessità
    numero_rami = int(dimensione * dimensione * complessita * 0.02)
    
    for _ in range(numero_rami):
        # Seleziona punto di partenza
        if random.random() < 0.6:  # 60% dal percorso principale
            punto_partenza = random.choice(percorso_principale)
        else:  # 40% da celle libere casuali
            punto_partenza = trova_cella_libera_casuale(labirinto)
        
        if punto_partenza:
            crea_ramo_complesso(labirinto, punto_partenza, complessita)

def trova_cella_libera_casuale(labirinto):
    """
    Trova una cella libera casuale nel labirinto
    """
    dimensione = len(labirinto)
    celle_libere = []
    
    for y in range(1, dimensione - 1):
        for x in range(1, dimensione - 1):
            if labirinto[y][x] == 0:
                celle_libere.append((x, y))
    
    return random.choice(celle_libere) if celle_libere else None

def crea_ramo_complesso(labirinto, punto_partenza, complessita):
    """
    Crea un ramo complesso che può diventare vicolo cieco
    """
    x, y = punto_partenza
    dimensione = len(labirinto)
    
    # Scegli direzione casuale che porta verso aree non esplorate
    direzioni = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(direzioni)
    
    lunghezza_ramo = random.randint(3, int(10 * complessita) + 5)
    
    for lunghezza in range(lunghezza_ramo):
        # Trova una direzione che porta a una cella non ancora libera
        direzione_trovata = False
        for dx, dy in direzioni:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < dimensione and 0 <= ny < dimensione and 
                labirinto[ny][nx] == 1):  # Solo se è un ostacolo
                
                # Libera la cella
                labirinto[ny][nx] = 0
                x, y = nx, ny
                direzione_trovata = True
                
                # Possibilità di creare rami secondari
                if random.random() < 0.3:
                    crea_ramo_secondario(labirinto, x, y, complessita)
                
                break
        
        if not direzione_trovata:
            # Se non troviamo direzione, probabilmente siamo in un'area già esplorata
            # Termina il ramo per creare un vicolo cieco
            break

def crea_ramo_secondario(labirinto, x, y, complessita):
    """
    Crea un piccolo ramo secondario che diventerà vicolo cieco
    """
    dimensione = len(labirinto)
    direzione = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    lunghezza = random.randint(1, int(5 * complessita) + 2)
    
    for _ in range(lunghezza):
        nx, ny = x + direzione[0], y + direzione[1]
        
        if (0 <= nx < dimensione and 0 <= ny < dimensione and 
            labirinto[ny][nx] == 1):
            
            labirinto[ny][nx] = 0
            x, y = nx, ny
        else:
            break  # Fine del vicolo cieco

def aggiungi_ostacoli_finali(labirinto, densita):
    """
    Aggiunge ostacoli finali in modo molto selettivo
    """
    dimensione = len(labirinto)
    
    # Numero molto limitato di ostacoli aggiuntivi
    numero_ostacoli = int(dimensione * dimensione * densita * 0.01)
    
    for _ in range(numero_ostacoli):
        for _ in range(10):  # Tentativi limitati
            x = random.randint(1, dimensione - 2)
            y = random.randint(1, dimensione - 2)
            
            if labirinto[y][x] == 0 and ostacolo_sicuro(labirinto, x, y):
                labirinto[y][x] = 1
                break

def ostacolo_sicuro(labirinto, x, y):
    """
    Verifica se aggiungere un ostacolo è sicuro (non isola aree)
    """
    dimensione = len(labirinto)
    
    # Non aggiungere ostacoli se ha meno di 3 vicini liberi
    vicini_liberi = 0
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < dimensione and 0 <= ny < dimensione and
            labirinto[ny][nx] == 0):
            vicini_liberi += 1
    
    return vicini_liberi >= 3

def verifica_percorso_esiste(labirinto, start=(0, 0), end=None):
    """
    Verifica se esiste un percorso usando BFS
    """
    if end is None:
        end = (len(labirinto) - 1, len(labirinto) - 1)
    
    if (labirinto[start[1]][start[0]] == 1 or 
        labirinto[end[1]][end[0]] == 1):
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

def analizza_labirinto_avanzato(labirinto):
    """
    Analizza la complessità del labirinto in dettaglio
    """
    dimensione = len(labirinto)
    celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
    
    # Conta vicoli ciechi
    vicoli_ciechi = 0
    celle_isolate = 0
    
    for y in range(1, dimensione - 1):
        for x in range(1, dimensione - 1):
            if labirinto[y][x] == 0:
                vicini_liberi = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if labirinto[y + dy][x + dx] == 0:
                        vicini_liberi += 1
                
                if vicini_liberi == 1:
                    vicoli_ciechi += 1
                elif vicini_liberi == 0:
                    celle_isolate += 1
    
    return {
        'celle_libere': celle_libere,
        'ostacoli': ostacoli,
        'vicoli_ciechi': vicoli_ciechi,
        'celle_isolate': celle_isolate,
        'percentuale_ostacoli': round(ostacoli/(celle_libere+ostacoli)*100, 1),
        'densita_vicoli': round(vicoli_ciechi/celle_libere*100, 1) if celle_libere > 0 else 0
    }

# Test del nuovo algoritmo
if __name__ == "__main__":
    print("=== GENERATORE LABIRINTI BILANCIATO ===")
    
    for densita in [0.25, 0.35, 0.45]:
        print(f"\n--- Densità: {densita} ---")
        labirinto = genera_labirinto_bilanciato(dimensione=30, densita_ostacoli=densita)
        
        stats = analizza_labirinto_avanzato(labirinto)
        print(f"Dimensioni: 30x30")
        print(f"Celle libere: {stats['celle_libere']}")
        print(f"Ostacoli: {stats['ostacoli']} ({stats['percentuale_ostacoli']}%)")
        print(f"Vicoli ciechi: {stats['vicoli_ciechi']}")
        print(f"Densità vicoli: {stats['densita_vicoli']}%")
        print(f"Celle isolate: {stats['celle_isolate']}")
        print(f"Percorso garantito: {'Sì' if verifica_percorso_esiste(labirinto) else 'No'}")
        
        # Visualizza una piccola porzione del labirinto
        print("Preview (5x5 in alto a sinistra):")
        for y in range(5):
            riga = ""
            for x in range(5):
                riga += "█" if labirinto[y][x] == 1 else "·"
            print(f"  {riga}")
        print()