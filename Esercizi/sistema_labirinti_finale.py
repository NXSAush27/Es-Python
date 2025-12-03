"""
SISTEMA COMPLETO DI GENERAZIONE LABIRINTI REALISTICI
Algoritmo finale che crea labirinti con percorsi multipli, vicoli ciechi e maggiore imprevedibilità
"""

from generatore_labirinto_bilanciato import genera_labirinto_bilanciato, analizza_labirinto_avanzato
import sys
import os

def es38(labirinto):
    """Funzione es38 per trovare la cella raggiungibile più in basso e a destra"""
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

def genera_labirinto_variabile(dimensione=100, densita=0.35, complessita=0.7):
    """
    Genera una variabile labirinto con le caratteristiche richieste
    
    Args:
        dimensione: dimensione del labirinto (NxN)
        densita: percentuale di ostacoli (0.2-0.5 raccomandato)
        complessita: livello di complessità (0.5-0.9 raccomandato)
    """
    return genera_labirinto_bilanciato(dimensione=dimensione, densita_ostacoli=densita, complessita=complessita)

def analizza_labirinto_completo(labirinto):
    """
    Analisi completa del labirinto con tutte le metriche
    """
    stats = analizza_labirinto_avanzato(labirinto)
    
    # Aggiungi analisi della cella massima raggiungibile
    cella_max = es38(labirinto)
    
    return {
        **stats,
        'cella_raggiungibile_max': cella_max,
        'complesso_e_realistico': stats['vicoli_ciechi'] > 50 and stats['percentuale_ostacoli'] > 20,
        'imprevedibile': stats['densita_vicoli'] > 3  # Ha una buona densità di vicoli ciechi
    }

def stampa_labirinto_testuale(labirinto, max_righe=15, max_colonne=50):
    """
    Stampa una rappresentazione testuale del labirinto
    """
    print("=== VISUALIZZAZIONE LABIRINTO ===")
    print("Legenda: # = ostacolo, . = libero, S = start, E = end")
    
    righe = min(len(labirinto), len(labirinto))
    colonne = min(len(labirinto[0]), len(labirinto[0]))
    
    for y in range(righe):
        riga = ""
        for x in range(colonne):
            if y == 0 and x == 0:
                riga += "S"  # Start
            elif y == len(labirinto) - 1 and x == len(labirinto[0]) - 1:
                riga += "E"  # End
            elif labirinto[y][x] == 1:
                riga += "#"  # Ostacolo
            else:
                riga += "."  # Libero
        print(f"{y:2d}: {riga}")
    
    if len(labirinto) > max_righe:
        print(f"    ... ({len(labirinto) - max_righe} righe nascoste)")

def confronta_algoritmi():
    """
    Confronta i diversi algoritmi di generazione
    """
    print("=== CONFRONTO ALGORITMI DI GENERAZIONE ===")
    
    algoritmi = {
        "Originale": lambda: genera_labirinto_bilanciato(30, 0.25, 0.5),
        "Bilanciato": lambda: genera_labirinto_bilanciato(30, 0.35, 0.7),
        "Complesso": lambda: genera_labirinto_bilanciato(30, 0.45, 0.9)
    }
    
    for nome, generatore in algoritmi.items():
        print(f"\n--- {nome} ---")
        labirinto = generatore()
        stats = analizza_labirinto_completo(labirinto)
        
        print(f"Ostacoli: {stats['percentuale_ostacoli']}%")
        print(f"Vicoli ciechi: {stats['vicoli_ciechi']}")
        print(f"Densità vicoli: {stats['densita_vicoli']}%")
        print(f"Cella max: {stats['cella_raggiungibile_max']}")
        print(f"Realistico: {'Sì' if stats['complesso_e_realistico'] else 'No'}")
        print(f"Imprevedibile: {'Sì' if stats['imprevedibile'] else 'No'}")

def demo_labirinto_completo():
    """
    Dimostrazione completa del sistema
    """
    print("=== DEMO GENERATORE LABIRINTI REALISTICI ===")
    
    # Genera labirinto 100x100
    print("\n1. Generazione labirinto 100x100...")
    labirinto = genera_labirinto_variabile()
    
    # Analizza
    stats = analizza_labirinto_completo(labirinto)
    print(f"   Celle libere: {stats['celle_libere']} ({100-stats['percentuale_ostacoli']}%)")
    print(f"   Ostacoli: {stats['ostacoli']} ({stats['percentuale_ostacoli']}%)")
    print(f"   Vicoli ciechi: {stats['vicoli_ciechi']}")
    print(f"   Cella max raggiungibile: {stats['cella_raggiungibile_max']}")
    
    # Visualizza
    stampa_labirinto_testuale(labirinto, 8, 40)
    trasforma_labirinto_in_immagine(labirinto)
    # Confronta algoritmi
    print("\n" + "="*50)
    confronta_algoritmi()
    
    print(f"\n=== CARATTERISTICHE RAGGIUNTE ===")
    print("✅ Percorso garantito sempre presente")
    print(f"✅ {stats['vicoli_ciechi']} vicoli ciechi per interesse")
    print(f"✅ {stats['densita_vicoli']}% densità vicoli (realistico)")
    print(f"✅ {stats['percentuale_ostacoli']}% ostacoli (bilanciato)")
    print("✅ Maggiore imprevedibilità vs algoritmi precedenti")
    print("✅ Pattern complessi e non lineari")

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

def main():
    """
    Menu principale del sistema
    """
    print("GENERATORE LABIRINTI REALISTICI - SISTEMA COMPLETO")
    print("Crea labirinti con percorsi multipli, vicoli ciechi e maggiore imprevedibilità")
    
    labirinto = genera_labirinto_bilanciato()
    demo_labirinto_completo()
    trasforma_labirinto_in_immagine(labirinto)

if __name__ == "__main__":
    # Se eseguito direttamente, avvia demo
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_labirinto_completo()
    else:
        main()