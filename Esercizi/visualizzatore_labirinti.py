"""
Funzioni avanzate per visualizzare labirinti come immagini
Trasforma le matrici dei labirinti in immagini visualizzabili
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow non disponibile. Installare con: pip install Pillow")

def visualizza_labirinto(labirinto, 
                        dimensione_cella=8,
                        colori=None,
                        mostra_percorso=False,
                        percorso_path=None,
                        salva_file=None,
                        titolo="Labirinto"):
    """
    Visualizza un labirinto come immagine su schermo
    
    Args:
        labirinto: matrice del labirinto (0=libero, 1=ostacolo)
        dimensione_cella: dimensione in pixel di ogni cella
        colori: dict con chiavi 'libero', 'ostacolo', 'percorso', 'sfondo'
        mostra_percorso: se evidenziare il percorso ottimale
        percorso_path: lista di coordinate del percorso da evidenziare
        salva_file: nome file per salvare l'immagine (opzionale)
        titolo: titolo della finestra
    """
    
    if not PIL_AVAILABLE:
        print("Errore: PIL/Pillow non è installato!")
        return
    
    if colori is None:
        colori = {
            'libero': (255, 255, 255),    # Bianco
            'ostacolo': (0, 0, 0),        # Nero
            'percorso': (255, 0, 0),      # Rosso
            'sfondo': (240, 240, 240),    # Grigio chiaro
            'start': (0, 255, 0),         # Verde
            'end': (255, 0, 255)          # Magenta
        }
    
    altezza = len(labirinto)
    larghezza = len(labirinto[0]) if altezza > 0 else 0
    
    # Crea l'immagine
    img_larg = larghezza * dimensione_cella
    img_alte = altezza * dimensione_cella
    img = Image.new('RGB', (img_larg, img_alte), colori['sfondo'])
    draw = ImageDraw.Draw(img)
    
    # Disegna le celle del labirinto
    for y in range(altezza):
        for x in range(larghezza):
            x_pixel = x * dimensione_cella
            y_pixel = y * dimensione_cella
            
            # Determina il colore della cella
            if x == 0 and y == 0:  # Start
                colore = colori['start']
            elif x == larghezza-1 and y == altezza-1:  # End
                colore = colori['end']
            elif labirinto[y][x] == 1:  # Ostacolo
                colore = colori['ostacolo']
            else:  # Libero
                colore = colori['libero']
            
            # Disegna la cella
            draw.rectangle([x_pixel, y_pixel, 
                          x_pixel + dimensione_cella, y_pixel + dimensione_cella], 
                          fill=colore)
    
    # Evidenzia il percorso se richiesto
    if mostra_percorso and percorso_path:
        for x, y in percorso_path:
            if 0 <= x < larghezza and 0 <= y < altezza:
                x_pixel = x * dimensione_cella + dimensione_cella//4
                y_pixel = y * dimensione_cella + dimensione_cella//4
                size = dimensione_cella//2
                
                draw.rectangle([x_pixel, y_pixel,
                              x_pixel + size, y_pixel + size],
                              fill=colori['percorso'])
    
    # Aggiungi griglia per cella grande
    if dimensione_cella >= 6:
        for x in range(larghezza + 1):
            x_pixel = x * dimensione_cella
            draw.line([(x_pixel, 0), (x_pixel, img_alte)], fill=(200, 200, 200))
        
        for y in range(altezza + 1):
            y_pixel = y * dimensione_cella
            draw.line([(0, y_pixel), (img_larg, y_pixel)], fill=(200, 200, 200))
    
    # Mostra l'immagine
    img.show()
    
    # Salva se richiesto
    if salva_file:
        img.save(salva_file)
        print(f"Immagine salvata in: {salva_file}")

def crea_percorso_visuale(labirinto):
    """
    Calcola il percorso ottimale dal punto (0,0) alla destinazione
    per evidenziarlo nell'immagine
    """
    from collections import deque
    
    altezza = len(labirinto)
    larghezza = len(labirinto[0]) if altezza > 0 else 0
    
    if altezza == 0 or larghezza == 0:
        return []
    
    start = (0, 0)
    end = (larghezza - 1, altezza - 1)
    
    # BFS per trovare il percorso
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == end:
            # Ricostruisci il percorso
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = visited.get(current)
            return list(reversed(path))
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < larghezza and 0 <= ny < altezza and
                labirinto[ny][nx] == 0 and (nx, ny) not in visited):
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))
    
    return []

def salva_labirinto_immagine(labirinto, 
                           nome_file="labirinto.png",
                           dimensione_cella=6,
                           colori=None,
                           mostra_percorso=True):
    """
    Salva il labirinto come immagine su disco
    """
    percorso_path = crea_percorso_visuale(labirinto) if mostra_percorso else None
    
    visualizza_labirinto(labirinto,
                        dimensione_cella=dimensione_cella,
                        colori=colori,
                        mostra_percorso=mostra_percorso,
                        percorso_path=percorso_path,
                        salva_file=nome_file,
                        titolo="Labirinto Salvato")

def confronto_labirinti_immagine(labirinti_dict, 
                                dimensione_cella=4,
                                righe=2, 
                                colonne=2):
    """
    Crea un confronto visivo di più labirinti in un'unica immagine
    
    Args:
        labirinti_dict: dict con nome->matrice labirinto
        dimensione_cella: dimensione delle celle
        righe: numero di righe nella griglia
        colonne: numero di colonne nella griglia
    """
    
    if not PIL_AVAILABLE:
        print("Errore: PIL/Pillow non è installato!")
        return
    
    # Trova la dimensione massima
    max_altezza = max(len(lab) for lab in labirinti_dict.values())
    max_larghezza = max(len(lab[0]) for lab in labirinti_dict.values() if lab)
    
    # Calcola dimensioni totali dell'immagine
    cella_size = dimensione_cella
    total_altezza = max_altezza * cella_size * righe + (righe + 1) * 10
    total_larghezza = max_larghezza * cella_size * colonne + (colonne + 1) * 10
    
    # Crea immagine combinata
    img_completa = Image.new('RGB', (total_larghezza, total_altezza), (255, 255, 255))
    
    labirinti_lista = list(labirinti_dict.items())
    
    for i, (nome, labirinto) in enumerate(labirinti_lista):
        if i >= righe * colonne:
            break
            
        riga = i // colonne
        col = i % colonne
        
        # Calcola posizione nella griglia
        x_offset = col * (max_larghezza * cella_size + 10) + 10
        y_offset = riga * (max_altezza * cella_size + 10) + 10
        
        # Crea sotto-immagine per questo labirinto
        img_labirinto = Image.new('RGB', 
                                 (len(labirinto[0]) * cella_size, len(labirinto) * cella_size),
                                 (255, 255, 255))
        draw = ImageDraw.Draw(img_labirinto)
        
        # Disegna il labirinto
        for y, riga_lab in enumerate(labirinto):
            for x, cella in enumerate(riga_lab):
                x_pixel = x * cella_size
                y_pixel = y * cella_size
                
                if cella == 1:
                    colore = (0, 0, 0)  # Nero per ostacoli
                else:
                    colore = (255, 255, 255)  # Bianco per libero
                
                draw.rectangle([x_pixel, y_pixel,
                              x_pixel + cella_size, y_pixel + cella_size],
                              fill=colore)
        
        # Incolla nella posizione corretta
        img_completa.paste(img_labirinto, (x_offset, y_offset))
    
    img_completa.show()
    return img_completa

def demo_visualizzazione():
    """
    Dimostrazione delle funzioni di visualizzazione
    """
    from generatore_labirinto_bilanciato import genera_labirinto_bilanciato
    
    print("=== DEMO VISUALIZZAZIONE LABIRINTI ===")
    
    # Genera diversi labirinti di prova
    labirinti = {
        "Semplice (20x20)": genera_labirinto_bilanciato(20, 0.3, 0.5),
        "Complesso (30x30)": genera_labirinto_bilanciato(30, 0.4, 0.8),
        "Denso (25x25)": genera_labirinto_bilanciato(25, 0.5, 0.9)
    }
    
    # Visualizza ogni labirinto singolarmente
    for nome, labirinto in labirinti.items():
        print(f"\nGenerazione: {nome}")
        
        # Calcola percorso
        percorso = crea_percorso_visuale(labirinto)
        print(f"  - Celle libere: {sum(sum(1 for c in r if c == 0) for r in labirinto)}")
        print(f"  - Ostacoli: {sum(sum(1 for c in r if c == 1) for r in labirinto)}")
        print(f"  - Lunghezza percorso: {len(percorso)} celle")
        
        # Mostra l'immagine
        colori_personalizzati = {
            'libero': (240, 248, 255),     # Alice Blue
            'ostacolo': (25, 25, 112),     # Midnight Blue
            'percorso': (255, 69, 0),      # Red Orange
            'sfondo': (230, 230, 250),     # Lavender
            'start': (50, 205, 50),        # Lime Green
            'end': (255, 20, 147)          # Deep Pink
        }
        
        visualizza_labirinto(labirinto,
                           dimensione_cella=8,
                           colori=colori_personalizzati,
                           mostra_percorso=True,
                           percorso_path=percorso,
                           titolo=f"Labirinto: {nome}")
        
        # Salva su disco
        nome_file = nome.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png"
        salva_labirinto_immagine(labirinto, nome_file, dimensione_cella=6)
    
    # Crea confronto visivo
    print(f"\nCreazione confronto visivo...")
    confronto_labirinti_immagine(labirinti, dimensione_cella=3, righe=2, colonne=2)

# Test se eseguito direttamente
if __name__ == "__main__":
    demo_visualizzazione()