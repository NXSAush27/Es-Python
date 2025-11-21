# Esercizi avanzati di programmazione con matrici e elaborazione avanzata di immagini
# Ignorare le righe fino alla 31
from typing import Any, Callable, List, Tuple, Dict, Union
import sys
from unittest import result
import images
import math  # Per funzioni trigonometriche e matematiche

# Classe per gestire i colori del terminale per output formattato
class bcolors:
    HEADER = '\033[95m'      # Colore magenta per intestazioni
    OKBLUE = '\033[94m'      # Colore blu per informazioni
    OKCYAN = '\033[96m'      # Colore ciano
    OKGREEN = '\033[92m'     # Colore verde per successi
    WARNING = '\033[93m'     # Colore giallo per avvertimenti
    FAIL = '\033[91m'        # Colore rosso per errori
    ENDC = '\033[0m'         # Reset colore
    BOLD = '\033[1m'         # Testo in grassetto
    UNDERLINE = '\033[4m'    # Testo sottolineato

# Funzione per eseguire test automatizzati e controllare i risultati
def check_test(func: Callable, expected: Any, *args: List[Any]):
    """
    Esegue un test su una funzione e confronta il risultato con il valore atteso.
    
    Args:
        func: Funzione da testare
        expected: Valore atteso dal test
        *args: Argomenti da passare alla funzione
    """
    func_str = func.__name__  # Nome della funzione da testare
    args_str = ', '.join(repr(arg) for arg in args)  # Rappresentazione stringa degli argomenti
    try:
        result = func(*args)  # Esegue la funzione con gli argomenti forniti
        result_str = repr(result)  # Rappresentazione stringa del risultato
        expected_str = repr(expected)  # Rappresentazione stringa del valore atteso
        test_outcome = "succeeded" if (result == expected) else "failed"  # Determina l'esito del test
        color = bcolors.OKGREEN if (result == expected) else bcolors.FAIL  # Colore per il risultato
        # Stampa il risultato del test con colori formattati
        print(f'{color}Test on {func_str} on input {args_str} {test_outcome}. Output: {result_str} Expected: {expected_str}')
    except BaseException as error:
        error_str = repr(error)  # Rappresentazione stringa dell'errore
        print(f'{bcolors.FAIL}ERROR: {func_str}({args_str}) => {error_str}')  # Stampa l'errore


# FUNZIONI AVANZATE PER ELABORAZIONE DI IMMAGINI

def img_grayscale(img_in: str, img_out: str):
    """
    Converte un'immagine a colori in scala di grigi usando la formula di luminosità standard.
    
    Args:
        img_in: Nome del file di input contenente l'immagine a colori
        img_out: Nome del file di output dove salvare l'immagine in scala di grigi
        
    Note:
        Usa i coefficienti di luminosità per convertire RGB in grigio:
        L = 0.2126*R + 0.7152*G + 0.0722*B
        Il risultato viene visualizzato usando images.visd_matplotlib()
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    gray_img = []  # Lista per memorizzare l'immagine convertita
    # Converte ogni pixel da RGB a scala di grigi
    for row in img:  # Per ogni riga dell'immagine
        gray_row = []  # Lista per una riga in scala di grigi
        for (R, G, B) in row:  # Per ogni pixel RGB nella riga
            # Calcola il valore di luminosità usando la formula standard
            gray_value = int(0.2126 * R + 0.7152 * G + 0.0722 * B)
            # Assegna lo stesso valore a tutti e tre i canali per il grigio
            gray_row.append((gray_value, gray_value, gray_value))
        gray_img.append(gray_row)  # Aggiunge la riga convertita all'immagine finale
    images.visd_matplotlib(gray_img)  # Visualizza l'immagine convertita

def img_rotate(img_in: str, theta: float, img_out: str):
    """
    Ruota un'immagine di un angolo specificato attorno al centro.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        theta: Angolo di rotazione in gradi (positivo = orario, negativo = antiorario)
        img_out: Nome del file di output dove salvare l'immagine ruotata
        
    Note:
        Usa trasformazioni trigonometriche per calcolare le nuove posizioni dei pixel.
        Pixel non coperti dalla rotazione rimangono neri.
    """
    # Converte l'angolo da gradi a radianti per le funzioni trigonometriche
    theta_rad = math.radians(theta)
    cos_theta = math.cos(theta_rad)  # Calcola il coseno una sola volta per efficienza
    sin_theta = math.sin(theta_rad)  # Calcola il seno una sola volta per efficienza
    
    img = images.load(img_in)  # Carica l'immagine dal file di input
    height = len(img)  # Altezza dell'immagine (numero di righe)
    width = len(img[0])  # Larghezza dell'immagine (numero di colonne)
    
    # Calcola il centro dell'immagine come punto di rotazione
    cx, cy = width / 2, height / 2
    
    # Crea una nuova immagine nera delle stesse dimensioni
    rotated_img = images.crea_immagine(width, height, (0, 0, 0))
    
    # Applica la trasformazione di rotazione a ogni pixel
    for y in range(height):  # Per ogni riga
        for x in range(width):  # Per ogni colonna
            # Calcola le coordinate relative al centro
            x_rel = x - cx
            y_rel = y - cy
            # Applica la formula di rotazione trigonometrica
            x_src = int(cx + (x_rel * cos_theta + y_rel * sin_theta))
            y_src = int(cy + (-x_rel * sin_theta + y_rel * cos_theta))
            
            # Verifica se le coordinate calcolate sono valide e dentro i confini
            if 0 <= x_src < width and 0 <= y_src < height:
                rotated_img[y][x] = img[y_src][x_src]  # Copia il pixel dalla posizione originale
    images.visd_matplotlib(rotated_img)  # Visualizza l'immagine ruotata

def img_circle(img_in: str, x: float, y: float, r: float, c: Tuple[int, int, int], img_out: str):
    """
    Disegna un cerchio vuoto su un'immagine esistente.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        x: Coordinata x del centro del cerchio
        y: Coordinata y del centro del cerchio
        r: Raggio del cerchio
        c: Colore del cerchio come tupla (R, G, B)
        img_out: Nome del file di output dove salvare l'immagine con il cerchio
        
    Note:
        Il cerchio viene disegnato testando se il centro del pixel è all'interno del cerchio
        usando la distanza euclidea dal centro. I pixel vengono considerati al centro
        con un offset di 0.5 rispetto agli indici degli array.
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    height = len(img)  # Altezza dell'immagine
    width = len(img[0])  # Larghezza dell'immagine
    
    # Disegna il cerchio controllando ogni pixel
    for j in range(height):  # Per ogni riga
        for i in range(width):  # Per ogni colonna
            # Calcola il centro del pixel (offset di 0.5 per il centro effettivo)
            pixel_center_x = i + 0.5
            pixel_center_y = j + 0.5
            # Calcola la distanza euclidea dal centro del cerchio
            distance = math.sqrt((pixel_center_x - x) ** 2 + (pixel_center_y - y) ** 2)
            # Se il pixel è sul bordo del cerchio, lo colora creando un cerchio vuoto
            if abs(distance - r) <= 0.5:
                img[j][i] = c  # Assegna il colore specificato
    images.visd_matplotlib(img)  # Visualizza l'immagine con il cerchio

def img_colorgrade(img_in: str, t: Tuple[float, float, float], c: float, s: float, img_out: str):
    """
    Applica regolazioni di colore avanzate: tinta, contrasto e saturazione.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        t: Tuple con i fattori di tinta per (R, G, B) - moltiplicatori per canale
        c: Fattore di contrasto (>1 = maggiore contrasto, <1 = minore contrasto)
        s: Fattore di saturazione (>1 = maggiore saturazione, <1 = minore saturazione)
        img_out: Nome del file di output dove salvare l'immagine elaborata
        
    Note:
        Lavora in spazio colore float [0,1] per evitare perdita di precisione,
        poi riconverte in intero [0,255]. Le trasformazioni vengono applicate in ordine:
        1. Tinta (tint): pixel *= t
        2. Contrasto: pixel = (pixel - 0.5) * c + 0.5
        3. Saturazione: pixel = (pixel - gray) * s + gray
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    height = len(img)  # Altezza dell'immagine
    width = len(img[0])  # Larghezza dell'immagine
    
    # Elabora ogni pixel dell'immagine
    for j in range(height):  # Per ogni riga
        for i in range(width):  # Per ogni colonna
            # Estrae i valori RGB del pixel corrente
            R, G, B = img[j][i]
            # Converte in float normalizzato [0,1]
            Rf, Gf, Bf = R/255.0, G/255.0, B/255.0
            
            # 1. Applica la tinta (tint) - moltiplica ogni canale per il fattore corrispondente
            Rf *= t[0]  # Tinta per il rosso
            Gf *= t[1]  # Tinta per il verde
            Bf *= t[2]  # Tinta per il blu
            
            # 2. Applica il contrasto - normalizza attorno a 0.5, applica il fattore, poi riporta in [0,1]
            Rf = (Rf - 0.5) * c + 0.5  # Contrasto per il rosso
            Gf = (Gf - 0.5) * c + 0.5  # Contrasto per il verde
            Bf = (Bf - 0.5) * c + 0.5  # Contrasto per il blu
            
            # 3. Applica la saturazione - separa il colore dalla luminosità, applica il fattore
            gray = 0.2126 * Rf + 0.7152 * Gf + 0.0722 * Bf  # Calcola la luminosità
            Rf = (Rf - gray) * s + gray  # Saturazione per il rosso
            Gf = (Gf - gray) * s + gray  # Saturazione per il verde
            Bf = (Bf - gray) * s + gray  # Saturazione per il blu
            
            # Converte di nuovo in intero [0,255] con controllo dei limiti
            R_new = max(0, min(255, int(Rf * 255)))  # Rosso normalizzato
            G_new = max(0, min(255, int(Gf * 255)))  # Verde normalizzato
            B_new = max(0, min(255, int(Bf * 255)))  # Blu normalizzato
            
            # Assegna i valori finali al pixel
            img[j][i] = (R_new, G_new, B_new)
    images.visd_matplotlib(img)  # Visualizza l'immagine con le regolazioni applicate

def img_mosaic(img_in: str, n: int, img_out: str):
    """
    Crea un effetto mosaico dividendo l'immagine in celle di dimensione n x n.
    
    Args:
        img_in: Nome del file di input contenente l'immagine
        n: Dimensione del lato di ogni cella del mosaico
        img_out: Nome del file di output dove salvare l'immagine con effetto mosaico
        
    Note:
        Ogni cella prende il colore del pixel in alto a sinistra della cella.
        Aggiunge bordi neri intorno a ogni cella per evidenziare l'effetto mosaico.
        Se l'immagine non è divisibile per n, le ultime righe/colonne possono essere più piccole.
    """
    img = images.load(img_in)  # Carica l'immagine dal file di input
    height = len(img)  # Altezza dell'immagine
    width = len(img[0])  # Larghezza dell'immagine
    
    # Crea il mosaico processando l'immagine in blocchi
    for j in range(0, height, n):  # Per ogni blocco di righe
        for i in range(0, width, n):  # Per ogni blocco di colonne
            
            # Riempie ogni cella con il colore del pixel in alto a sinistra
            for y in range(j, min(j + n, height)):  # Per le righe della cella corrente
                for x in range(i, min(i + n, width)):  # Per le colonne della cella corrente
                    # Set cell color (usa il colore del pixel in alto a sinistra della cella)
                    img[y][x] = img[j][i]
            
            # Disegna i bordi neri intorno alla cella (quattro lati del quadrato)
            
            # Bordo superiore e inferiore
            for x in range(i, min(i + n, width)):  # Per ogni colonna della cella
                if j < height:  # Se c'è una riga superiore da colorare
                    img[j][x] = (0, 0, 0)  # Colora di nero il bordo superiore
                if j + n - 1 < height:  # Se c'è una riga inferiore da colorare
                    img[min(j + n - 1, height - 1)][x] = (0, 0, 0)  # Colora di nero il bordo inferiore
            
            # Bordo sinistro e destro
            for y in range(j, min(j + n, height)):  # Per ogni riga della cella
                if i < width:  # Se c'è una colonna sinistra da colorare
                    img[y][i] = (0, 0, 0)  # Colora di nero il bordo sinistro
                if i + n - 1 < width:  # Se c'è una colonna destra da colorare
                    img[y][min(i + n - 1, width - 1)] = (0, 0, 0)  # Colora di nero il bordo destro
    images.visd_matplotlib(img)  # Visualizza l'immagine con effetto mosaico


# SEZIONE DI TEST PER LE FUNZIONI AVANZATE DI ELABORAZIONE IMMAGINI

# Test della conversione in scala di grigi
#img_grayscale("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_grayscale.png")

# Test della rotazione con diversi angoli (inclusi angoli negativi e multipli di 360°)
#for angle in [-30, 15, 30, 45, 480, -500]:
    # -30: rotazione antioraria di 30°, 15: rotazione oraria di 15°
    # 30: rotazione oraria di 30°, 45: rotazione oraria di 45°
    # 480: equivalente a 120° (480-360), -500: equivalente a -140° (-500+360)
    #img_rotate("esercizi immagini/esercizi immagini/img1.png", angle,
    #           "esercizi immagini/esercizi immagini/img1_rotated_" + str(angle) + ".png")

# Test del disegno di un cerchio (giallo) al centro dell'immagine
#img_circle("esercizi immagini/esercizi immagini/img1.png", 100, 100, 25, (255, 255, 0),
#           "esercizi immagini/esercizi immagini/img1_circle.png")  # Centro (100,100), raggio 25, colore giallo

# Test delle regolazioni di colore con parametri diversi per osservare gli effetti
# Test 1: Tinta leggermente verdastra con contrasto e saturazione normali
#img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (0.9, 1.0, 0.9), 1, 1,
#               "esercizi immagini/esercizi immagini/img_colorgrade1.png")  # Tinta: 0.9,1.0,0.9 - Contrasto: 1 - Saturazione: 1

# Test 2: Colori naturali con contrasto raddoppiato (effetto drammatico)
#img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (1.0, 1.0, 1.0), 2, 1,
#               "esercizi immagini/esercizi immagini/img_colorgrade2.png")  # Tinta: 1,1,1 - Contrasto: 2 - Saturazione: 1

# Test 3: Colori naturali con saturazione raddoppiata (colori più vivaci)
#img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (1.0, 1.0, 1.0), 1, 2,
#               "esercizi immagini/esercizi immagini/img_colorgrade3.png")  # Tinta: 1,1,1 - Contrasto: 1 - Saturazione: 2

# Test 4: Combinazione di tinta verdastra, alto contrasto e bassa saturazione
#img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (0.8, 1.0, 0.8), 2, 0.7,
#               "esercizi immagini/esercizi immagini/img_colorgrade4.png")  # Tinta: 0.8,1.0,0.8 - Contrasto: 2 - Saturazione: 0.7

# Test dell'effetto mosaico con celle di 3x3 pixel
img_mosaic("esercizi immagini/esercizi immagini/img1.png", 8,
           "esercizi immagini/esercizi immagini/img_mosaic.png")  # Dimensione cella: 3x3 pixel