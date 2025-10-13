#Esercizio 1.1: Somma e prodotto di due numeri interi
input1 = int(input("Inserisci il primo numero intero: "))
input2 = int(input("Inserisci il secondo numero intero: "))

print(f"Somma: {input1 + input2} (tipo: {type(input1 + input2)})")
print(f"Prodotto: {input1 * input2} (tipo: {type(input1 * input2)})")

#Esercizio 2: Divisione normale, divisione intera e resto
input1 = int(input("Inserisci il primo numero intero: "))
input2 = int(input("Inserisci il secondo numero intero: "))

print(f"Divisione normale: {input1 / input2} (tipo: {type(input1 / input2)})")
print(f"Divisione intera: {input1 // input2} (tipo: {type(input1 // input2)})")
print(f"Resto: {input1 % input2} (tipo: {type(input1 % input2)})")

#Esercizio 3: Manipolazione di stringhe
input1 = input("Inserisci una parola: ")
input2 = int(input("Inserisci un numero intero: "))
print(f"Stringa ripetuta: {input1 * input2} (tipo: {type(input1 * input2)})")
print(f"Lunghezza: {len(input1)} (tipo: {type(len(input1))})")

#Esercizio 4: Conversione e espressioni miste
input1 = input("Inserisci un numero: ")

print(f"Risultato di {int(input1)} + {float(input1)} * 2: {int(input1) + float(input1) * 2} (tipo: {type(int(input1) + float(input1) * 2)})")

#Esercizion 5: Valore booleano di oggetti
input1 = input("Inserisci una stringa: ")
print(f"Valore booleano della stringa: {bool(input1)} (tipo: {type(bool(input1))})")