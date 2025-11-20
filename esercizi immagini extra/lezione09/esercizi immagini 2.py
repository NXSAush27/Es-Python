# Ignorare le righe fino alla 31
from typing import Any, Callable, List, Tuple, Dict, Union
import sys
from unittest import result
import images
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Esegue un test e controlla il risultato


def check_test(func: Callable, expected: Any, *args: List[Any]):
    func_str = func.__name__
    args_str = ', '.join(repr(arg) for arg in args)
    try:
        result = func(*args)
        result_str = repr(result)
        expected_str = repr(expected)
        test_outcome = "succeeded" if (result == expected) else "failed"
        color = bcolors.OKGREEN if (result == expected) else bcolors.FAIL
        print(f'{color}Test on {func_str} on input {args_str} {test_outcome}. Output: {result_str} Expected: {expected_str}')
    except BaseException as error:
        error_str = repr(error)
        print(f'{bcolors.FAIL}ERROR: {func_str}({args_str}) => {error_str}')


# Definire una funzione che dato il nome di un file (img_in) contenente un'immagine,
# calcola l'immagine corrispondente in scala di grigi.
# Per fare ciò, se R è il canale del rosso, G del verde, e B del blu, rimpiazzare ogni canale
# con il valore 0.2126*R + 0.7152*G + 0.0722*B.
# Attenzione: Il valore di ciascun canale deve essere un intero.
# L'immagine risultante viene salvata nel file con nome indicato come parametro (img_out)
# Per leggere/scrivere l'immagine usare i comandi load/save del modulo "images" visto a lezione.
# Controllare il file risultante per verificare la correttezza della funzione (non vengono effettuati test automatici)
def img_grayscale(img_in: str, img_out: str):
    img = images.load(img_in)
    gray_img = []
    for row in img:
        gray_row = []
        for (R, G, B) in row:
            gray_value = int(0.2126 * R + 0.7152 * G + 0.0722 * B)
            gray_row.append((gray_value, gray_value, gray_value))
        gray_img.append(gray_row)
    images.visd_matplotlib(gray_img)


# Definire una funzione che dato il nome di un file (img_in) contenente un'immagine,
# ruota l'immagine (tenendo fisso il centro) di un certo numero di gradi centigradi
# specificato come parametro (theta).
# Per fare ciò, utilizzare la seguente formula:
#   - Se ruotiamo l'immagine di un angolo theta, il pixel che si trova alle coordinate (x, y),
#     nell'immagine ruotata si troverà alle coordinate (x*cos(theta) + y*sin(theta), -x*sin(theta) + y*cos(theta))
# Attenzione: controllare la documentazione per vedere cosa richiedono in input le funzioni
# math.sin e math.cos
# L'immagine risultante viene salvata nel file con nome indicato come parametro (img_out)
# Per leggere/scrivere l'immagine usare i comandi load/save del modulo "images" visto a lezione.
# Controllare il file risultante per verificare la correttezza della funzione (non vengono effettuati test automatici)
def img_rotate(img_in: str, theta: float, img_out: str):
    theta_rad = math.radians(theta)
    cos_theta = math.cos(theta_rad)
    sin_theta = math.sin(theta_rad)
    img = images.load(img_in)
    height = len(img)
    width = len(img[0])
    cx, cy = width / 2, height / 2
    rotated_img = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            x_rel = x - cx
            y_rel = y - cy
            x_src = int(cx + (x_rel * cos_theta + y_rel * sin_theta))
            y_src = int(cy + (-x_rel * sin_theta + y_rel * cos_theta))
            if 0 <= x_src < width and 0 <= y_src < height:
                rotated_img[y][x] = img[y_src][x_src]
    images.visd_matplotlib(rotated_img)


# Definire una funzione che disegna un cerchio centrato in (x,y) e di raggio r,
# su una immagine presa in input e la ri-scrive in output.
# Per disegnare il cerchio, testiamo se un punto è all'interno del cerchio o no,
# guardando se la distanza dal center è <= raggio. Nel caso settiamo il colore c.
# Il centro di ogni pixel è translato di 0.5 rispetto agli indici dei pixels.
def img_circle(img_in: str, x: float, y: float, r: float, c: Tuple, img_out: str):
    img = images.load(img_in)
    height = len(img)
    width = len(img[0])
    for j in range(height):
        for i in range(width):
            pixel_center_x = i + 0.5
            pixel_center_y = j + 0.5
            distance = math.sqrt((pixel_center_x - x) ** 2 + (pixel_center_y - y) ** 2)
            if distance <= r:
                img[j][i] = c
    images.visd_matplotlib(img)


# Definire una funzione che applica aggiunstamenti di colore ad una immagine.
# In particolare, applichiamo nel'ordine: (a) tinta, (b) contrasto, (c) saturazione.
# Per farlo, priam riportiamo i colori in [0,1] float, poi applichiamo gli updates,
# e poi torniamo in [0,255] intero.
# (a) tinta: pixel *= t
# (b) contrasto: pixel = (pixel - 0.5) * c + 0.5
# (c) saturazione: pixel = (pixel - gray(pixel)) * s + gray(pixel)
def img_colorgrade(img_in: str, t: tuple, c: float, s: float, img_out: str):
    img = images.load(img_in)
    height = len(img)
    width = len(img[0])
    for j in range(height):
        for i in range(width):
            R, G, B = img[j][i]
            Rf, Gf, Bf = R/255.0, G/255.0, B/255.0
            # Apply tint
            Rf *= t[0]
            Gf *= t[1]
            Bf *= t[2]
            # Apply contrast
            Rf = (Rf - 0.5) * c + 0.5
            Gf = (Gf - 0.5) * c + 0.5
            Bf = (Bf - 0.5) * c + 0.5
            # Apply saturation
            gray = 0.2126 * Rf + 0.7152 * Gf + 0.0722 * Bf
            Rf = (Rf - gray) * s + gray
            Gf = (Gf - gray) * s + gray
            Bf = (Bf - gray) * s + gray
            # Convert back to [0,255]
            R_new = max(0, min(255, int(Rf * 255)))
            G_new = max(0, min(255, int(Gf * 255)))
            B_new = max(0, min(255, int(Bf * 255)))
            img[j][i] = (R_new, G_new, B_new)
    images.visd_matplotlib(img)


# Definire una funzione che crea un mosaico sui pixel di una immagine. Il mosaico
# ha celle di larghezza n. Per questo esercizio usiamo un colore del quadratino e
# non ci preoccupiamo di fare la media. Inoltre disegniamo anche delle linee nere
# intorno a ogni cella del mosaico.
def img_mosaic(img_in: str, n: int, img_out: str):
    img = images.load(img_in)
    height = len(img)
    width = len(img[0])
    for j in range(0, height, n):
        for i in range(0, width, n):
            for y in range(j, min(j + n, height)):
                for x in range(i, min(i + n, width)):
                    # Set cell color (media dei pixel)
                    img[y][x] = img[j][i]
            # Draw black borders
            for x in range(i, min(i + n, width)):
                if j < height:
                    img[j][x] = (0, 0, 0)
                if j + n - 1 < height:
                    img[min(j + n - 1, height - 1)][x] = (0, 0, 0)
            for y in range(j, min(j + n, height)):
                if i < width:
                    img[y][i] = (0, 0, 0)
                if i + n - 1 < width:
                    img[y][min(i + n - 1, width - 1)] = (0, 0, 0)
    images.visd_matplotlib(img)


# Test funzioni
img_grayscale("esercizi immagini/esercizi immagini/img1.png", "esercizi immagini/esercizi immagini/img1_grayscale.png")
for angle in [-30, 15, 30, 45, 480, -500]:
    img_rotate("esercizi immagini/esercizi immagini/img1.png", angle, "esercizi immagini/esercizi immagini/img1_rotated_" + str(angle) + ".png")
img_circle("esercizi immagini/esercizi immagini/img1.png", 100, 100, 25, (255, 255, 0), "esercizi immagini/esercizi immagini/img1_circle.png")
img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (0.9, 1.0, 0.9), 1, 1, "esercizi immagini/esercizi immagini/img_colorgrade1.png")
img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (1.0, 1.0, 1.0), 2, 1, "esercizi immagini/esercizi immagini/img_colorgrade2.png")
img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (1.0, 1.0, 1.0), 1, 2, "esercizi immagini/esercizi immagini/img_colorgrade3.png")
img_colorgrade("esercizi immagini/esercizi immagini/img1.png", (0.8, 1.0, 0.8), 2, 0.7, "esercizi immagini/esercizi immagini/img_colorgrade4.png")
img_mosaic("esercizi immagini/esercizi immagini/img1.png", 3, "esercizi immagini/esercizi immagini/img_mosaic.png")