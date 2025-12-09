import albero

def es6(percorsi):
   '''
   Si definisca la funzione es6(testo) ricorsiva (o che fa uso di funzioni o 
   metodi ricorsive/i) che:
   - riceve come argomento:
      - un insieme di stringhe che hanno la proprietà che ciascuna è stata 
      ottenuta a partire dallo stesso albero binario
         (in cui ciascun nodo contiene un solo carattere), risalendo da ciascuna 
         foglia fino alla radice e concatenando
         i valori dei nodi
         NOTA l'albero è localmente ordinato da sinistra a destra, ovvero:
         - ciascun figlio sinistro contiene un carattere minore di quello del padre
         - ciascun figlio destro contiene un carattere maggiore di quello del padre
   - ricostruisce l'albero originale e lo torna come risultato

   Esempio: se l'albero da ricostruire è
                     i     
                     |
             |-----------------|               
             h                 m 
             |                 |   
         |--------|        |------|   
         c        j        k      p
         |        |               |
      |-----|  |-----|         |-----|
      a     f  g     k         m     q    

   L'insieme di stringhe è
      { 'achi', 'qpmi', 'gjhi', 'fchi', 'mpmi', 'kmi', 'kjhi' }

   ATTENZIONE: è VIETATO usare i metodi della classe AlberoBinario

   '''
   # inserisci qui il tuo codice
   

   radice = None
   for percorso in percorsi:
      radice = inserisci_nodo(radice, percorso)
   return radice


def inserisci_nodo(radice, percorso):
   if radice is None:
      radice = albero.AlberoBinario(percorso[-1])
   
   if len(percorso) > 1:
      char_corrente = percorso[-2]
      if char_corrente < radice.valore:
         radice.sx = inserisci_nodo(radice.sx, percorso[:-1])
      elif char_corrente > radice.valore:
         radice.dx = inserisci_nodo(radice.dx, percorso[:-1])
   
   return radice

