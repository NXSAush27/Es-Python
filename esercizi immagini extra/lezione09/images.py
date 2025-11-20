'''
Funzioni di utilita' per leggere e salvare una immagine nella nostra codifica.
Utilities to load/save a PNG file to our encoding.
'''
import png, io
import IPython.display as ipd 

def load(filename):
    """ Carica la immagine PNG dal file 'filename'.  Torna una lista di liste di pixel.
        Ogni pixel è una tupla (R, G, B) dei 3 colori con valori tra 0 e 255.
        Load a PNG image from file 'filename'. Return a list of lists of pixel.
        Each pixel is a tuple (R, G, B) of its 3 colors with values in 0..255.
    """
    with open(filename, mode='rb') as f:
        reader = png.Reader(file=f)
        w, h, png_img, _ = reader.asRGB8()
        # ottimizzata leggermente
        w *= 3
        return [ [ (line[i],line[i+1],line[i+2]) 
                   for i in range(0, w, 3) ]
                 for line in png_img ]


def save(img, filename):
    """ Salva l'immagine 'img' nel file PNG 'filename'. img è una lista di liste di pixel. 
        Ogni pixel è una tupla (R, G, B) dei 3 colori con valori tra 0 e 255.
        Save the 'img' image in a 'filename' PNG file. img is a list of lists of pixel.
        Each pixel is a tuple (R, G, B) of its 3 colors with values in 0..255.
    """
    pngimg = png.from_array(img,'RGB')
    pngimg.save(filename)

class Image:                                                                                                                    
    '''Oggetto che contiene una immagine come lista di liste di colori (R,G,B) e che viene                                         
    direttamente visualizzate in IPython console/qtconsole/notebook col metodo _repr_png_'''                                       
    def __init__(self, img):                                                                                                       
        self.pixels = img                                                                                                          
    def _repr_png_(self):                                                                                                          
        '''Produce la rappresentazione binaria della immagine in formato PNG'''                                                    
        img = png.from_array(self.pixels, 'RGB')                                                                                   
        b = io.BytesIO()                                                                                                           
        img.save(b)                                                                                                                
        return b.getvalue()                                                                                                        
                                                                                                   
def visd(img, didascalia=''):                                                                                                      
    '''Visualizza una immagine in una console IPython seguita da una didascalia opzionale'''                                       
    ipd.display(Image(img))                                                                                                     
    if didascalia:                                                                                                                 
        print(didascalia)  

def visd_matplotlib(img: Image, titolo: str = "Visualizzazione Immagine") -> None:
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

def load_immagine_https(img_url: str) -> Image:
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

def crea_immagine(larghezza : int, altezza: int, colore: tuple = (0, 0, 0)) -> Image:
    return [[colore] * larghezza for _ in range(altezza)]
