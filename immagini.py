import math 
from copy import deepcopy
from typing import Callable
#tipi
Colore = tuple[int, int, int]
Immagine = list[list[Colore]]
Filtro = Callable[[Colore], Colore]
FiltroXY = Callable[[int, int, Immagine, int, int], Colore]

#Colori
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#funzioni di base
def crea_immagine(larghezza : int, altezza: int, colore: Colore = black) -> Immagine:
    return [[colore] * larghezza for _ in range(altezza)]

def draw_pixel(img : Immagine, x: int, y: int, colore : Colore) -> None:
    altezza = len(img)
    larghezza = len(img[0])
    if 0 <= x < larghezza and 0 <= y < altezza:
        img[y][x] = colore

def draw_rectangle_full(img: Immagine, x1: int, y1: int, x2: int, y2: int, colore: Colore) -> None:
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            draw_pixel(img, x, y, colore)

def draw_line(img: Immagine, x1: int, y1: int, x2: int, y2: int, colore: Colore) -> None:
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1
            dx *= -1
            dy *= -1
        m = dy / dx if dx != 0 else 0

        for x in range(x1, x2 + 1):
            y = m * (x - x1) + y1
            draw_pixel(img, round(y), x, colore)
    else:
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y2
            dx *= -1
            dy *= -1
        m = dx / dy if dy != 0 else 0
        for y in range(y1, y2 + 1):
            x = m * (y - y1) + x1
            draw_pixel(img, y, round(x), colore)

def bound(canale: float | int, m: int = 0, M: int = 255) -> int:
    canale = round(canale)
    return min(max(canale, m), M)

def crop_image(img : Immagine, alto: int, basso: int, sx: int, dx: int) -> Immagine:
    L, A = len(img[0]), len(img)

    assert 0 <= alto < A and 0 <= basso < A and 0 <= sx < L and 0 <= dx < L and alto + basso < A and sx + dx < L, "Parametri di crop non validi"
    
    if basso :
        fetta = img[alto: - basso]
    else: 
        fetta = img[alto:]
    if dx:
        return [riga[sx:-dx] for riga in fetta]
    else:
        return [riga[sx:] for riga in fetta]

def cut_paste_img(imgS : Immagine, imgD : Immagine, xs1 : int, xs2 : int, ys1 : int, ys2 : int, xD : int, yD : int) -> None:
    HS = len(imgS)
    WS = len(imgS[0])

    frammento = crop_image(imgS, ys1, HS - ys2 -1, xs1, WS - xs2 -1)
    larghezza = len(frammento[0])
    for yF, riga in enumerate(frammento):
        y_dest = yF + yD
        if 0 <= y_dest < len(imgD):
            x_start_dest = max(0, xD)
            x_end_dest = min(len(imgD[0]), xD + larghezza)

            x_start_src = max(0, -xD)
            x_end_src = min(larghezza, len(imgD[0]) -xD)
            if x_start_dest < x_end_dest:
                imgD[y_dest][x_start_dest:x_end_dest] = riga[x_start_src:x_end_src]

def applica_filtro(img: Immagine, filtro: Filtro) -> Immagine:
    copia = deepcopy(img)
    for y, riga in enumerate(img):
        for x, colore in enumerate(riga):
            copia[y][x] = filtro(colore)
    return copia

def applica_filtro_XY(img: Immagine, filtro : FiltroXY) -> Immagine:
    W, H = len(img[0]), len(img)
    copia = deepcopy(img)
    for y in range(H):
        for x in range(W):
            copia[y][x] = filtro(x, y, img, W, H)
    return copia

def visd_terminale(img: Immagine, larghezza_desiderata: int = 80):
    """
    Mostra un'anteprima dell'immagine nel terminale usando colori ANSI.
    Questa funzione è un'alternativa di debug alla 'visd' usata nelle lezioni.
    
    NOTA: Richiede un terminale moderno che supporti "true color" (la maggior parte lo fa).
    
    Args:
        img: L'immagine da visualizzare.
        larghezza_desiderata: Il numero di caratteri in larghezza da usare (default: 80).
    """
    
    # --- 1. Ottieni dimensioni e gestisci immagine vuota ---
    H_orig = len(img)
    if H_orig == 0:
        print("[Immagine vuota]")
        return
        
    W_orig = len(img[0])
    if W_orig == 0:
        print("[Immagine vuota]")
        return

    # --- 2. Calcola la nuova altezza con correzione dell'aspect ratio ---
    # I caratteri del terminale non sono quadrati (sono circa 2:1 alti/larghi).
    # Correggiamo per questo (valore 2.0) per evitare immagini "stirate".
    ASPECT_RATIO_CORRECTION = 2.0
    altezza_desiderata = int((H_orig * larghezza_desiderata) / (W_orig * ASPECT_RATIO_CORRECTION))
    
    # Evitiamo altezza 0
    if altezza_desiderata == 0:
        altezza_desiderata = 1
        
    # --- 3. Itera sulle nuove coordinate (più piccole) e campiona l'originale ---
    for y_new in range(altezza_desiderata):
        riga_da_stampare = []
        
        # Calcola la y originale da cui campionare (Nearest Neighbor)
        y_orig = int(y_new * H_orig / altezza_desiderata)
        
        for x_new in range(larghezza_desiderata):
            # Calcola la x originale da cui campionare
            x_orig = int(x_new * W_orig / larghezza_desiderata)
            
            # Ottieni il colore del pixel originale
            R, G, B = img[y_orig][x_orig]
            
            # --- 4. Crea la stringa ANSI ---
            # \033[48;2;R;G;Bm  -> Imposta il colore di SFONDO (48) in RGB (2)
            # " "                -> Il carattere "pixel"
            ansi_pixel = f"\033[48;2;{R};{G};{B}m "
            riga_da_stampare.append(ansi_pixel)
        
        # --- 5. Stampa la riga e il codice di reset ---
        # \033[0m -> Resetta tutti gli stili (colore, sfondo, ecc.)
        print("".join(riga_da_stampare) + "\033[0m")

def visd_matplotlib(img: Immagine, titolo: str = "Visualizzazione Immagine") -> None:
    """
    Apre una finestra esterna per visualizzare l'immagine usando Matplotlib.
    Richiede l'installazione di matplotlib (`pip install matplotlib`).
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("ERRORE: La libreria 'matplotlib' non è installata.")
        print("Installala con il comando: pip install matplotlib")
        return

    # Gestione immagine vuota
    if not img or not img[0]:
        print("L'immagine è vuota, nulla da visualizzare.")
        return

    # Crea la figura
    plt.figure(figsize=(6, 6))  # Dimensione della finestra (in pollici)
    
    # Mostra l'immagine
    # Matplotlib accetta nativamente liste di liste di tuple (R,G,B)
    plt.imshow(img)
    
    # Aggiungi titolo e rimuovi gli assi (numeri sui bordi)
    plt.title(titolo)
    plt.axis('off')
    
    # Mostra la finestra (questo comando blocca l'esecuzione finché non chiudi la finestra)
    plt.show()

def load_immagine_https(img_url: str) -> Immagine:
    """
    Carica un'immagine da un URL HTTPS e la converte nel formato Immagine.
    Richiede l'installazione di Pillow e requests (`pip install Pillow requests`).
    """
    try:
        from PIL import Image
        import requests
        from io import BytesIO
    except ImportError:
        print("ERRORE: Le librerie 'Pillow' e 'requests' non sono installate.")
        print("Installale con il comando: pip install Pillow requests")
        return []

    # Scarica l'immagine
    response = requests.get(img_url)
    if response.status_code != 200:
        print(f"ERRORE: Impossibile scaricare l'immagine. Status code: {response.status_code}")
        return []

    # Apri l'immagine con Pillow
    img_pil = Image.open(BytesIO(response.content)).convert('RGB')
    
    # Converti in formato Immagine
    larghezza, altezza = img_pil.size
    img = crea_immagine(larghezza, altezza)
    
    for y in range(altezza):
        for x in range(larghezza):
            img[y][x] = img_pil.getpixel((x, y))
    
    return img

def load_immagine_file(percorso_file: str) -> Immagine:
    """
    Carica un'immagine da un file locale e la converte nel formato Immagine.
    Richiede l'installazione di Pillow (`pip install Pillow`).
    """
    try:
        from PIL import Image
    except ImportError:
        print("ERRORE: La libreria 'Pillow' non è installata.")
        print("Installala con il comando: pip install Pillow")
        return []

    # Apri l'immagine con Pillow
    img_pil = Image.open(percorso_file).convert('RGB')
    
    # Converti in formato Immagine
    larghezza, altezza = img_pil.size
    img = crea_immagine(larghezza, altezza)
    
    for y in range(altezza):
        for x in range(larghezza):
            img[y][x] = img_pil.getpixel((x, y))
    
    return img