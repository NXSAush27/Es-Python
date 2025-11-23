
import copy
from labirinto_variabile import labirinto

def es38(labirinto):
    ''' 
    Un labirinto e' rappresentato tramite una griglia.
    Le posizioni delle celle del labirinto sono determinate dalle coppie  (x,y) 
    dove y e' la riga ed x la colonna in cui si trova la cella.
    La cella in alto a sinistra ha coordinate (0,0).
    Le celle della griglia contengono l'intero 0 (libera) o l'intero 1 (ostacolo).
    E possibile spostarsi tra due celle adiacenti con soli due tipi di mosse:
    - dall'altro verso il basso  (vale a dire da una generica cella  (x,y) alla cella  (x,y+1) )
    - da sinistra verso destra   (vale a dire da una generica cella  (x,y) alla cella  (x+1,y) )
    Ci si puo' spostare in una cella solo se questa contiene l'intero 0 (e' vuota)
    Una cella (x,y) e' raggiungibile se esiste una sequenza di mosse che partendo 
    dalla cella (0,0) permette di raggiungerla.
    Si implementi la funzione es38(labirinto) che, dato un labirinto rappresentato come 
    lista di liste, restituisca le coordinate (x, y) della cella raggiungibile 
    situata piu' in basso e a parita' quella piu' a destra.
    Ad esempio per il labirinto di dimensioni 7x7:
    0001000
    1000010
    0001010
    1010010
    0011010
    1001011
    0110100
    la funzione deve restituire la tupla (4, 5).
    Nota bene: La lista di liste non deve essere modificata dalla funzione.  
    '''
    if not labirinto or not labirinto[0] or labirinto[0][0] == 1:
        return None
    rows = len(labirinto)
    cols = len(labirinto[0])
    reachable = [[False] * cols for _ in range(rows)]
    reachable[0][0] = True
    for y in range(rows):
        for x in range(cols):
            if labirinto[y][x] == 0:
                if x > 0 and reachable[y][x - 1]:
                    reachable[y][x] = True
                if y > 0 and reachable[y - 1][x]:
                    reachable[y][x] = True
    for y in range(rows - 1, -1, -1):
        for x in range(cols - 1, -1, -1):
            if reachable[y][x]:
                return (x, y)
    return None

def print_labirinto(labirinto):
    for row in labirinto:
        print(''.join(str(cell) for cell in row))

def trasforma_labirinto_in_immagine(labirinto):
    from PIL import Image
    height = len(labirinto)
    width = len(labirinto[0]) if height > 0 else 0
    img = Image.new('RGB', (width, height), "white")
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if labirinto[y][x] == 1:
                pixels[x, y] = (0, 0, 0)  # nero per ostacoli
            else:
                pixels[x, y] = (255, 255, 255)  # bianco per celle libere
    img.show()

labirinto_piccolo = [[0, 0, 0, 1, 0, 0, 0],
             [1, 0, 0, 0, 0, 1, 0], 
             [0, 0, 0, 1, 0, 1, 0], 
             [1, 0, 1, 0, 0, 1, 0], 
             [0, 0, 1, 1, 0, 1, 0], 
             [1, 0, 0, 1, 0, 1, 1], 
             [0, 1, 1, 0, 1, 0, 0]]

labirinto_grande = labirinto
trasforma_labirinto_in_immagine(labirinto=labirinto_grande)









