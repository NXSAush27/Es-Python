import csv, random

class Libro:
    def __init__(self, titolo, autore, anno_pubblicazione, prezzo, genere) -> None:
        self.titolo = titolo
        self.autore = autore
        self.anno_pubblicazione = anno_pubblicazione
        self.prezzo = prezzo
        self.genere = genere
        
    def ritornaValori(self)-> dict:
        return {"Titolo": self.titolo, "Autore": self.autore, "Anno Pubblicazione": self.anno_pubblicazione, "Prezzo": self.prezzo, "Genere": self.prezzo}
    def __str__(self) -> str:
        return f"Titolo: {self.titolo}\nAutore: {self.autore}\nAnno Pubblicazione: {self.anno_pubblicazione}\nPrezzo: {self.prezzo}\nGenere: {self.genere}"

class Libreria:
    def __init__(self) -> None:
        self.Libri = []
    def aggiungiLibro(self, titolo, autore, anno_pubblicazione, prezzo, genere):
        newLibro = Libro(titolo, autore, anno_pubblicazione, prezzo, genere)
        if not newLibro in self.Libri:
            for libro in self.Libri:
                if newLibro.titolo == libro.titolo:
                    return False
            self.Libri.append(newLibro)
            return True
        else:
            return False
    def cancellaLibro(self, titolo):
        for libro in self.Libri:
            if libro.titolo == titolo:
                self.Libri.remove(libro)
                return True 
        return False
    def ricercaLibro(self, titolo, genere) -> list:
        ricerca = 0 #0 nessuna ricerca, 1 ricerca titolo, 2 ricerca genere, 3 ricerca titolo e genere
        if titolo & genere:
            ricerca = 3
        elif titolo:
            ricerca = 1
        elif genere:
            ricerca = 2
        match ricerca: 
            case 0:
                return []
            case 1:
                risultato = []
                for libro in self.Libri:
                    if libro.titolo == titolo:
                        risultato.append(libro)
                return risultato
            case 2:
                risultato = []
                for libro in self.Libri:
                    if libro.genere == genere:
                        risultato.append(libro)
                return risultato
            case 3:
                risultato = []
                for libro in self.Libri:
                    if libro.titolo == titolo & libro.genere == genere:
                        risultato.append(libro)
                return risultato
    def LeggiCSV(self):
        try:
            with open("Libreria.csv", 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.Libri = [Libro(r["Titolo"], r["Autore"], int(r["Anno"]), float(r["Prezzo"]), r["Genere"]) for r in reader]
        except FileNotFoundError:
            print("Errore, file non trovato, verrà creato un nuovo file")
    def ScriviCSV(self):
        with open("Libreria.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Titolo", "Autore", "Anno", "Prezzo", "Genere"])
            for libro in self.Libri:
                writer.writerow([libro.titolo, libro.autore, libro.anno_pubblicazione, libro.prezzo, libro.genere])