"""
Test del labirinto 100x100 con la funzione es38 di program.py
"""

# Importa la funzione es38 dal program.py
import sys
sys.path.append('.')

# Esegui il program.py per importare la funzione es38
exec(open('program.py').read())

# Importa la variabile labirinto dal nostro file
exec(open('labirinto_completo.py').read())

# Testa la funzione es38 con il nostro labirinto
print("Testing es38 function with 100x100 labyrinth...")
risultato = es38(labirinto)
print(f"Risultato: {risultato}")

# Stampa alcune statistiche del labirinto
celle_libere = sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)
ostacoli = sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)
print(f"Celle libere (0): {celle_libere}")
print(f"Ostacoli (1): {ostacoli}")
print(f"Dimensioni: {len(labirinto)} x {len(labirinto[0])}")