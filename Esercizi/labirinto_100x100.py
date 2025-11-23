"""
Labirinto 100x100 creato seguendo lo stesso formato di program.py
Ogni cella contiene 0 (libera) o 1 (ostacolo)
"""

# Creazione di un labirinto 100x100 con pattern interessante
import random

# Inizializza la matrice con tutte celle libere (0)
labirinto = [[0 for _ in range(100)] for _ in range(100)]

# Aggiungi alcuni ostacoli (1) per creare un pattern interessante
# Bordi del labirinto
for i in range(100):
    labirinto[0][i] = 1          # Prima riga
    labirinto[99][i] = 1         # Ultima riga
    labirinto[i][0] = 1          # Prima colonna
    labirinto[i][99] = 1         # Ultima colonna

# Aggiungi ostacoli in pattern diagonali
for i in range(10, 90):
    labirinto[i][i] = 1
    labirinto[i][99-i] = 1

# Aggiungi alcuni ostacoli casuali
for _ in range(500):
    x = random.randint(1, 98)
    y = random.randint(1, 98)
    labirinto[y][x] = 1

# Assicurati che l'inizio (0,0) sia libero per il pathfinding
labirinto[0][0] = 0

print(f"Labirinto 100x100 creato con {sum(sum(row) for row in labirinto)} ostacoli")
print("Formato: lista di liste con 0 (libera) e 1 (ostacolo)")