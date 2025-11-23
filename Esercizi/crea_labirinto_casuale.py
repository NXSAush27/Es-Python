"""
Genera un labirinto 100x100 casuale con percorso garantito
usando l'algoritmo di generazione sviluppato
"""

from generatore_labirinto_casuale import genera_labirinto_con_percorso_garantito, stampa_statistiche_labirinto
import sys
import os

def crea_labirinto_100x100_casuale():
    """
    Crea un labirinto 100x100 ottimizzato con percorso garantito
    """
    print("Generazione di un labirinto 100x100 con percorso casuale garantito...")
    
    # Genera il labirinto con una densità bilanciata
    labirinto = genera_labirinto_con_percorso_garantito(
        dimensione=100, 
        densita_ostacoli=0.25  # 25% di ostacoli circa
    )
    
    # Verifica e stampa le statistiche
    stampa_statistiche_labirinto(labirinto)
    
    return labirinto

# Genera la variabile labirinto
labirinto = crea_labirinto_100x100_casuale()

# Salva in un file separato per uso futuro
print("\nSalvataggio del labirinto in labirinto_casuale_100x100.py...")

with open('labirinto_casuale_100x100.py', 'w') as f:
    f.write('# Labirinto 100x100 casuale con percorso garantito\n')
    f.write('# Generato automaticamente dal generatore di labirinti\n\n')
    f.write('labirinto = [\n')
    
    for i, riga in enumerate(labirinto):
        f.write('    ' + str(riga))
        if i < len(labirinto) - 1:
            f.write(',')
        f.write('\n')
    
    f.write(']\n\n')
    
    # Aggiungi informazioni
    celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
    ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
    
    f.write(f'# Dimensioni: {len(labirinto)} x {len(labirinto[0])}\n')
    f.write(f'# Celle libere (0): {celle_libere}\n')
    f.write(f'# Ostacoli (1): {ostacoli}\n')
    f.write(f'# Percentuale ostacoli: {ostacoli/(celle_libere+ostacoli)*100:.1f}%\n')
    f.write('# Percorso garantito da (0,0) a (99,99): Sì\n')

print("Labirinto casuale 100x100 creato e salvato con successo!")
print("File creato: labirinto_casuale_100x100.py")