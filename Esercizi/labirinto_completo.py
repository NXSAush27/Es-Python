# Labirinto 100x100 completo nel formato di program.py

def crea_labirinto_100x100():
    """
    Crea una matrice 100x100 dove ogni cella contiene 0 (libera) o 1 (ostacolo)
    Seguendo il formato del labirinto in program.py
    """
    labirinto = []
    
    # Crea 100 righe
    for riga in range(100):
        nuova_riga = []
        
        for colonna in range(100):
            # Bordi del labirinto sono ostacoli
            if riga == 0 or riga == 99 or colonna == 0 or colonna == 99:
                nuova_riga.append(1)
            # Cella di partenza (0,0) deve essere libera
            elif riga == 0 and colonna == 0:
                nuova_riga.append(0)
            # Alcuni ostacoli interni per creare percorsi interessanti
            elif riga == colonna and 10 < riga < 90:  # Diagonale principale
                nuova_riga.append(1)
            elif riga + colonna == 99 and 10 < riga < 90:  # Diagonale secondaria
                nuova_riga.append(1)
            elif riga == 50 and 20 < colonna < 80:  # Linea orizzontale centrale
                nuova_riga.append(1)
            elif colonna == 50 and 20 < riga < 80:  # Linea verticale centrale
                nuova_riga.append(1)
            else:
                # Celle libere con alcuni ostacoli casuali distribuiti
                if (riga * 3 + colonna * 7) % 23 == 0:  # Pattern matematico per distribuzione
                    nuova_riga.append(1)
                else:
                    nuova_riga.append(0)
        
        labirinto.append(nuova_riga)
    
    return labirinto

# Creazione della variabile labirinto
labirinto = crea_labirinto_100x100()

# Test: stampa le dimensioni e alcuni dettagli
print(f"Labirinto 100x100 creato con successo!")
print(f"Dimensioni: {len(labirinto)} righe x {len(labirinto[0])} colonne")
print(f"Celle libere (0): {sum(sum(1 for cella in riga if cella == 0) for riga in labirinto)}")
print(f"Ostacoli (1): {sum(sum(1 for cella in riga if cella == 1) for riga in labirinto)}")

# Mostra un esempio delle prime righe
print("\nPrime 5 righe del labirinto:")
for i in range(min(5, len(labirinto))):
    print(f"Riga {i}: {labirinto[i][:20]}... (mostrati solo primi 20 elementi)")