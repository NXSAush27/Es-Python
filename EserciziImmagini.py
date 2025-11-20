import immagini
def crea_bandiera_italiana(altezza: int) -> immagini.Immagine:
    #larghezza 1.5 volte l'altezza
    larghezza = round(altezza * 1.5)
    img = immagini.crea_immagine(larghezza, altezza)
    parte1 = (0, round(larghezza / 3))
    parte2 = (round(larghezza / 3) + 1 , 2*parte1[1])
    parte3 = (parte2[1] + 1, larghezza)

    #parte verde
    immagini.draw_rectangle_full(img, parte1[0], 0, parte1[1], altezza, immagini.green)
    # parte bianca
    immagini.draw_rectangle_full(img, parte2[0], 0, parte2[1], altezza, immagini.white)
    #parte rossa
    immagini.draw_rectangle_full(img, parte3[0], 0, parte3[1], altezza, immagini.red)
    return img

immagine_italiana = crea_bandiera_italiana(300)
#immagini.visd_matplotlib(immagine_italiana)

def disegna_griglia(img: immagini.Immagine, N: int, colore: immagini.Colore) -> None:
    #N-1 righe e colonne
    W, H = len(img[0]), len(img)

    spacingW = round(W / N)
    spacingH = round(H / N)
    x = 0
    for _ in range(N-1):
        x+= spacingW
        immagini.draw_line(img, x, 0, x, H, colore)
    y = 0
    for _ in range(N-1):
        y+= spacingH
        immagini.draw_line(img, 0, y, W, y, colore)


immagine_griglia = immagini.crea_immagine(300, 300, immagini.black)
disegna_griglia(immagine_griglia, 10, immagini.white)
#immagini.visd_matplotlib(immagine_griglia)

def collage_filtri(img: immagini.Immagine) -> immagini.Immagine:
    H = len(img)
    W = len(img[0])
    copia = immagini.deepcopy(img)
    #quadrante superiore sinistro: originale
    #quadrante superiore destro: scala di grigi
    #quadrante inferiore sinistro: negativo
    #quadrante inferiore destro: luminosità aumentata del 50%
    #utilizzo copy and paste per evitare di influenzare i calcoli
    for y in range(H):
        for x in range(W):
            colore = copia[y][x]
            if x >= W // 2 and y < H // 2:
                #scala di grigi
                media = sum(colore) / 3
                colore = (round(media), round(media), round(media))
            elif x < W // 2 and y >= H // 2:
                #negativo
                colore = (255 - colore[0], 255 - colore[1], 255 - colore[2])
            elif x >= W // 2 and y >= H // 2:
                #luminosità aumentata del 50%
                colore = (immagini.bound(colore[0] * 1.5),
                          immagini.bound(colore[1] * 1.5),
                          immagini.bound(colore[2] * 1.5))
            img[y][x] = colore
    return img

immagini.visd_matplotlib(collage_filtri(immagini.load_immagine_file("8vuLtqi.png")))