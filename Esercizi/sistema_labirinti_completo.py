"""
Sistema completo di labirinti 100x100 con algoritmo di generazione casuale
Integra tutti i componenti per un sistema di labirinti con percorso garantito
"""

# Importa la funzione es38 dal program.py originale
import sys
import os

# Aggiungi la directory corrente al path per gli import
sys.path.append(os.path.dirname(__file__))

from generatore_labirinto_casuale import genera_labirinto_con_percorso_garantito

def es38(labirinto):
    """Funzione es38 dal program.py originale per trovare la cella raggiungibile più in basso e a destra"""
    if not labirinto or not labirinto[0] or labirinto[0][0] == 1:
        return None
    rows = len(labirinto)
    cols = len(labirinto[0])
    reachable = [[False] * cols for _ in range(rows)]
    reachable[0][0] = True
    for y in range(rows):
        for x in range(cols):
            if labirinto[y][x] == 0:
                if x > 0 and reachable[y][x - 1]:
                    reachable[y][x] = True
                if y > 0 and reachable[y - 1][x]:
                    reachable[y][x] = True
    for y in range(rows - 1, -1, -1):
        for x in range(cols - 1, -1, -1):
            if reachable[y][x]:
                return (x, y)
    return None

def crea_labirinto_casuale_100x100():
    """
    Crea un labirinto 100x100 casuale con percorso garantito
    Utilizza l'algoritmo di generazione ottimizzato
    """
    return genera_labirinto_con_percorso_garantito(dimensione=100, densita_ostacoli=0.70)

def crea_labirinto_personalizzato(dimensione=100, densita_ostacoli=0.25):
    """
    Crea un labirinto di dimensioni personalizzate con percorso garantito
    
    Args:
        dimensione: dimensione del labirinto (NxN)
        densita_ostacoli: percentuale di ostacoli (0.0 - 1.0)
    
    Returns:
        labirinto: matrice NxN con percorso garantito
    """
    return genera_labirinto_con_percorso_garantito(dimensione=dimensione, densita_ostacoli=densita_ostacoli)

def stampa_labirinto(labirinto, max_righe=10):
    """
    Stampa una rappresentazione testuale del labirinto
    Args:
        labirinto: matrice del labirinto
        max_righe: numero massimo di righe da mostrare
    """
    print("Visualizzazione labirinto (0=libero, 1=ostacolo):")
    for i, riga in enumerate(labirinto[:max_righe]):
        print(f"Riga {i:2d}: {''.join(str(cell) for cell in riga)}")
    if len(labirinto) > max_righe:
        print(f"... ({len(labirinto) - max_righe} righe nascoste)")

def trasforma_labirinto_in_immagine(labirinto):
    from PIL import Image
    height = len(labirinto)
    width = len(labirinto[0]) if height > 0 else 0
    img = Image.new('RGB', (width, height), "white")
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if labirinto[y][x] == 1:
                pixels[x, y] = (0, 0, 0)  # nero per ostacoli
            else:
                pixels[x, y] = (255, 255, 255)  # bianco per celle libere
    img.show()

def analizza_labirinto(labirinto):
    """
    Analizza un labirinto e restituisce statistiche dettagliate
    """
    dimensione = len(labirinto)
    celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
    
    # Trova la cella raggiungibile più in basso e a destra
    risultato_es38 = es38(labirinto)
    
    return {
        'dimensione': f"{dimensione}x{dimensione}",
        'celle_libere': celle_libere,
        'ostacoli': ostacoli,
        'percentuale_ostacoli': round(ostacoli/(celle_libere+ostacoli)*100, 1),
        'cella_raggiungibile_max': risultato_es38,
        'percorsi_disponibili': 'Sì' if risultato_es38 else 'No'
    }

# Esempio di utilizzo
if __name__ == "__main__":
    print("=== SISTEMA DI LABIRINTI CASUALI CON PERCORSO GARANTITO ===")
    print()
    
    # Crea un labirinto 100x100
    print("1. Generazione labirinto 100x100...")
    labirinto_100 = crea_labirinto_casuale_100x100()
    
    # Analizza il labirinto
    stats_100 = analizza_labirinto(labirinto_100)
    print(f"   Dimensioni: {stats_100['dimensione']}")
    print(f"   Celle libere: {stats_100['celle_libere']}")
    print(f"   Ostacoli: {stats_100['ostacoli']}")
    print(f"   % Ostacoli: {stats_100['percentuale_ostacoli']}%")
    print(f"   Percorso garantito: {stats_100['percorsi_disponibili']}")
    if stats_100['cella_raggiungibile_max']:
        print(f"   Cella max raggiungibile: {stats_100['cella_raggiungibile_max']}")
    print()
    
    trasforma_labirinto_in_immagine(labirinto_100)
    print()
    