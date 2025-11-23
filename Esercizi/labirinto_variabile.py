# Labirinto 100x100 - Variabile nel formato richiesto
# Ogni cella contiene 0 (libera) o 1 (ostacolo)

# Per utilizzare questo labirinto:
# from labirinto_variabile import labirinto
# risultato = es38(labirinto)

# Il labirinto è stato generato dal file labirinto_completo.py
# e contiene:
# - 8926 celle libere (0)
# - 1074 ostacoli (1)
# - Dimensioni: 100 x 100
# - Bordi chiusi (tutti ostacoli)
# - Pattern di ostacoli interni per creare percorsi complessi

# Per ottenere la variabile labirinto, esegui:
import os
labirinto_path = os.path.join(os.path.dirname(__file__), 'labirinto_completo.py')
exec(open(labirinto_path).read())