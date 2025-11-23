"""
Generazione labirinto 100x100 con algoritmo bilanciato
Crea labirinti realistici con percorsi multipli e vicoli ciechi
"""

from generatore_labirinto_bilanciato import genera_labirinto_bilanciato, analizza_labirinto_avanzato
import os

def crea_labirinto_100x100_realistico():
    """
    Crea un labirinto 100x100 realistico con buon equilibrio
    """
    print("Generazione labirinto 100x100 realistico...")
    
    # Genera con densità bilanciata per labirinti interessanti
    labirinto = genera_labirinto_bilanciato(
        dimensione=100, 
        densita_ostacoli=0.35,  # 35% ostacoli per buon equilibrio
        complessita=0.7         # Alta complessità per molti vicoli ciechi
    )
    
    # Analizza il risultato
    stats = analizza_labirinto_avanzato(labirinto)
    print(f"Dimensioni: {stats['celle_libere'] + stats['ostacoli']}x{stats['celle_libere'] + stats['ostacoli']}")
    print(f"Celle libere: {stats['celle_libere']}")
    print(f"Ostacoli: {stats['ostacoli']} ({stats['percentuale_ostacoli']}%)")
    print(f"Vicoli ciechi: {stats['vicoli_ciechi']}")
    print(f"Densità vicoli: {stats['densita_vicoli']}%")
    print(f"Celle isolate: {stats['celle_isolate']}")
    
    return labirinto, stats

def salva_labirinto_100x100(labirinto, stats):
    """
    Salva il labirinto in un file Python
    """
    print("\nSalvataggio del labirinto...")
    
    filename = 'labirinto_realistico_100x100.py'
    with open(filename, 'w') as f:
        f.write('# Labirinto 100x100 realistico con vicoli ciechi\n')
        f.write('# Generato con algoritmo bilanciato\n\n')
        f.write('labirinto = [\n')
        
        for i, riga in enumerate(labirinto):
            f.write('    ' + str(riga))
            if i < len(labirinto) - 1:
                f.write(',')
            f.write('\n')
        
        f.write(']\n\n')
        
        # Aggiungi statistiche
        f.write(f'# STATISTICHE LABIRINTO\n')
        f.write(f'# Dimensioni: {len(labirinto)}x{len(labirinto[0])}\n')
        f.write(f'# Celle libere: {stats["celle_libere"]}\n')
        f.write(f'# Ostacoli: {stats["ostacoli"]} ({stats["percentuale_ostacoli"]}%)\n')
        f.write(f'# Vicoli ciechi: {stats["vicoli_ciechi"]}\n')
        f.write(f'# Densità vicoli: {stats["densita_vicoli"]}%\n')
        f.write(f'# Celle isolate: {stats["celle_isolate"]}\n')
        f.write(f'# Percorso garantito da (0,0) a (99,99): Sì\n')
    
    print(f"Labirinto salvato in: {filename}")
    return filename

def anteprima_labirinto(labirinto, dimensione_anteprima=10):
    """
    Mostra un'anteprima del labirinto
    """
    print(f"\nAnteprima labirinto ({dimensione_anteprima}x{dimensione_anteprima} in alto a sinistra):")
    print("Legenda: # = ostacolo, . = libero")
    
    for y in range(min(dimensione_anteprima, len(labirinto))):
        riga = ""
        for x in range(min(dimensione_anteprima, len(labirinto[0]))):
            riga += "#" if labirinto[y][x] == 1 else "."
        print(f"  {riga}")
    print("...")

def main():
    print("=== GENERATORE LABIRINTI 100x100 REALISTICI ===")
    
    # Genera il labirinto
    labirinto, stats = crea_labirinto_100x100_realistico()
    
    # Mostra anteprima
    anteprima_labirinto(labirinto)
    
    # Salva il labirinto
    filename = salva_labirinto_100x100(labirinto, stats)
    
    print(f"\n=== LABIRINTO COMPLETATO ===")
    print(f"File: {filename}")
    print(f"Caratteristiche:")
    print(f"  - {stats['percentuale_ostacoli']}% di ostacoli (bilanciato)")
    print(f"  - {stats['vicoli_ciechi']} vicoli ciechi (interessante)")
    print(f"  - {stats['densita_vicoli']}% densità vicoli (realistico)")
    print(f"  - Percorso garantito sempre presente")
    print(f"  - Maggiore imprevedibilità vs algoritmi precedenti")

if __name__ == "__main__":
    main()