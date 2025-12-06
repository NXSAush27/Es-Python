import os
import os.path


def es67(path):
    """
    ATTENZIONE: e' VIETATO usare la funzione os.walk o altre funzioni di libreria che 
    permettono di cercare tutti i file presenti in una directory. 
    (la directory la dovete esplorare voi)

    Si definisca la funzione ricorsiva (o che fa uso di vostre funzioni ricorsive) es67 che:
    - riceve come argomento un path del filesystem
    - esplora ricorsivamente la directory corrispondente e torna un dizionario.

    NOTA: tutti i file e directory che iniziano con '.' vanno ignorati.

    Il dizionario ha come chiave le estensioni dei file trovati nella directory 
    (ovvero gli ultimi 3 caratteri del nome dei file, es: 'txt', 'pdf', 'png').
    Il valore associato a ciascuna chiave K e' la distanza (differenza delle profondita')
    tra il piu' profondo file che ha quella estensione e il meno profondo.
    Assumete che i file contenuti nella directory path siano a profondita' 0.
    Esempio:
    se nella directory con path='A1' sono presenti i soli due file di tipo 'txt'
        A1/a/b/c/d/e/f/g/h/pippo.txt    a profondita' 8    (contando A1 = 0)
        A1/d/f/pappo.txt                a profondita' 2
        risultato contiene la coppia chiave: valore
        'txt' : 6
    """
    minimi = {}
    massimi = {}
    minmassimi("C:/Users/Utente/Desktop/Projects/Es-Python/67/"+path, minimi, massimi, 0)
    return {k: massimi[k]-minimi[k] for k in minimi}

def minmassimi(path, m, M, prof):
    for fn in os.listdir(path):
        if '.' == fn[0]: continue
        filename = path + '/' + fn
        if os.path.isdir(filename):
            minmassimi(filename, m, M, prof+1)
        else:
            ext = fn[-3:]
            m[ext] = min(m.get(ext, prof), prof)
            M[ext] = max(M.get(ext, prof), prof)
