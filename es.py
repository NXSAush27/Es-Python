import csv, random, json, sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QMenuBar, QMenu, QInputDialog, QFileDialog, QHeaderView,
    QDialog, QFormLayout, QDialogButtonBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Libro:
    def __init__(self, titolo, autore, anno_pubblicazione, prezzo, genere) -> None:
        self.titolo = titolo
        self.autore = autore
        self.anno_pubblicazione = anno_pubblicazione
        self.prezzo = prezzo
        self.genere = genere

    def ritornaValori(self)-> dict:
        return {"Titolo": self.titolo, "Autore": self.autore, "Anno Pubblicazione": self.anno_pubblicazione, "Prezzo": self.prezzo, "Genere": self.genere}
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
        if titolo and genere:
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
                    if libro.titolo == titolo and libro.genere == genere:
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

class BookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.libreria = Libreria()
        self.libreria.LeggiCSV()
        self.initUI()
        self.updateTable()

    def initUI(self):
        self.setWindowTitle("Book Inventory Manager")
        self.setGeometry(100, 100, 800, 600)

        # Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        exportMenu = menubar.addMenu('Export')

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.saveData)
        fileMenu.addAction(saveAction)

        loadAction = QAction('Load', self)
        loadAction.triggered.connect(self.loadData)
        fileMenu.addAction(loadAction)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        exportJSONAction = QAction('Export to JSON', self)
        exportJSONAction.triggered.connect(self.exportJSON)
        exportMenu.addAction(exportJSONAction)

        exportPDFAction = QAction('Export to PDF', self)
        exportPDFAction.triggered.connect(self.exportPDF)
        exportMenu.addAction(exportPDFAction)

        # Central widget
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # Search section
        searchLayout = QHBoxLayout()
        self.searchTitleEdit = QLineEdit()
        self.searchTitleEdit.setPlaceholderText("Search by title")
        self.searchGenreCombo = QComboBox()
        self.searchGenreCombo.addItem("All Genres")
        self.searchGenreCombo.addItems(["Fiction", "Non-Fiction", "Science", "History", "Biography", "Other"])
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.searchBooks)
        clearButton = QPushButton("Clear Search")
        clearButton.clicked.connect(self.clearSearch)

        searchLayout.addWidget(QLabel("Title:"))
        searchLayout.addWidget(self.searchTitleEdit)
        searchLayout.addWidget(QLabel("Genre:"))
        searchLayout.addWidget(self.searchGenreCombo)
        searchLayout.addWidget(searchButton)
        searchLayout.addWidget(clearButton)
        layout.addLayout(searchLayout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Title", "Author", "Year", "Price", "Genre"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Buttons
        buttonLayout = QHBoxLayout()
        addButton = QPushButton("Add Book")
        addButton.clicked.connect(self.addBook)
        editButton = QPushButton("Edit Book")
        editButton.clicked.connect(self.editBook)
        deleteButton = QPushButton("Delete Book")
        deleteButton.clicked.connect(self.deleteBook)

        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(editButton)
        buttonLayout.addWidget(deleteButton)
        layout.addLayout(buttonLayout)

    def updateTable(self, books=None):
        if books is None:
            books = self.libreria.Libri
        self.table.setRowCount(len(books))
        for row, libro in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(libro.titolo))
            self.table.setItem(row, 1, QTableWidgetItem(libro.autore))
            self.table.setItem(row, 2, QTableWidgetItem(str(libro.anno_pubblicazione)))
            self.table.setItem(row, 3, QTableWidgetItem(f"{libro.prezzo:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(libro.genere))

    def addBook(self):
        dialog = BookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            titolo, autore, anno, prezzo, genere = dialog.getData()
            if self.libreria.aggiungiLibro(titolo, autore, anno, prezzo, genere):
                self.updateTable()
            else:
                QMessageBox.warning(self, "Error", "Book with this title already exists.")

    def editBook(self):
        currentRow = self.table.currentRow()
        if currentRow < 0:
            QMessageBox.warning(self, "Error", "Please select a book to edit.")
            return
        libro = self.libreria.Libri[currentRow]
        dialog = BookDialog(self, libro)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            titolo, autore, anno, prezzo, genere = dialog.getData()
            if titolo != libro.titolo and any(l.titolo == titolo for l in self.libreria.Libri):
                QMessageBox.warning(self, "Error", "Book with this title already exists.")
                return
            libro.titolo = titolo
            libro.autore = autore
            libro.anno_pubblicazione = anno
            libro.prezzo = prezzo
            libro.genere = genere
            self.updateTable()

    def deleteBook(self):
        currentRow = self.table.currentRow()
        if currentRow < 0:
            QMessageBox.warning(self, "Error", "Please select a book to delete.")
            return
        libro = self.libreria.Libri[currentRow]
        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{libro.titolo}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.libreria.cancellaLibro(libro.titolo)
            self.updateTable()

    def searchBooks(self):
        title = self.searchTitleEdit.text().strip()
        genre = self.searchGenreCombo.currentText()
        if genre == "All Genres":
            genre = ""
        results = self.libreria.ricercaLibro(title, genre)
        self.updateTable(results)

    def clearSearch(self):
        self.searchTitleEdit.clear()
        self.searchGenreCombo.setCurrentIndex(0)
        self.updateTable()

    def saveData(self):
        self.libreria.ScriviCSV()
        QMessageBox.information(self, "Saved", "Data saved successfully.")

    def loadData(self):
        self.libreria.LeggiCSV()
        self.updateTable()
        QMessageBox.information(self, "Loaded", "Data loaded successfully.")

    def exportJSON(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export to JSON", "", "JSON Files (*.json)")
        if filename:
            data = [libro.ritornaValori() for libro in self.libreria.Libri]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Exported", "Data exported to JSON successfully.")

    def exportPDF(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf)")
        if filename:
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            y = height - 50
            c.drawString(50, y, "Book Inventory")
            y -= 30
            for libro in self.libreria.Libri:
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, f"Title: {libro.titolo}")
                c.drawString(50, y-15, f"Author: {libro.autore}")
                c.drawString(50, y-30, f"Year: {libro.anno_pubblicazione}")
                c.drawString(50, y-45, f"Price: {libro.prezzo:.2f}")
                c.drawString(50, y-60, f"Genre: {libro.genere}")
                y -= 80
            c.save()
            QMessageBox.information(self, "Exported", "Data exported to PDF successfully.")

    def closeEvent(self, event):
        self.saveData()
        event.accept()

class BookDialog(QDialog):
    def __init__(self, parent=None, libro=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Book")
        self.layout = QFormLayout(self)

        self.titleEdit = QLineEdit(libro.titolo if libro else "")
        self.authorEdit = QLineEdit(libro.autore if libro else "")
        self.yearEdit = QLineEdit(str(libro.anno_pubblicazione) if libro else "")
        self.priceEdit = QLineEdit(str(libro.prezzo) if libro else "")
        self.genreCombo = QComboBox()
        self.genreCombo.addItems(["Fiction", "Non-Fiction", "Science", "History", "Biography", "Other"])
        if libro:
            index = self.genreCombo.findText(libro.genere)
            if index >= 0:
                self.genreCombo.setCurrentIndex(index)

        self.layout.addRow("Title:", self.titleEdit)
        self.layout.addRow("Author:", self.authorEdit)
        self.layout.addRow("Year:", self.yearEdit)
        self.layout.addRow("Price:", self.priceEdit)
        self.layout.addRow("Genre:", self.genreCombo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def getData(self):
        try:
            anno = int(self.yearEdit.text())
            prezzo = float(self.priceEdit.text())
            return self.titleEdit.text(), self.authorEdit.text(), anno, prezzo, self.genreCombo.currentText()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid year or price.")
            return None, None, None, None, None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookApp()
    window.show()
    sys.exit(app.exec())