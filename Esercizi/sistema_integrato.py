"""
SISTEMA INTEGRATO: GENERAZIONE E VISUALIZZAZIONE LABIRINTI
Combina generazione avanzata di labirinti con visualizzazione grafica
"""

from generatore_labirinto_bilanciato import genera_labirinto_bilanciato, analizza_labirinto_avanzato
from visualizzatore_labirinti import visualizza_labirinto, salva_labirinto_immagine, crea_percorso_visuale
import sys

def es38(labirinto):
    """Funzione es38 per trovare la cella raggiungibile più in basso e a destra"""
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

def genera_labirinto_con_visualizzazione(dimensione=100, densita=0.35, complessita=0.7):
    """
    Genera un labirinto e lo visualizza automaticamente
    """
    print(f"Generazione labirinto {dimensione}x{dimensione}...")
    labirinto = genera_labirinto_bilanciato(dimensione, densita, complessita)
    
    # Analizza il labirinto
    stats = analizza_labirinto_avanzato(labirinto)
    percorso = crea_percorso_visuale(labirinto)
    
    print(f"Completato:")
    print(f"   - Celle libere: {stats['celle_libere']} ({100-stats['percentuale_ostacoli']}%)")
    print(f"   - Ostacoli: {stats['ostacoli']} ({stats['percentuale_ostacoli']}%)")
    print(f"   - Vicoli ciechi: {stats['vicoli_ciechi']}")
    print(f"   - Lunghezza percorso: {len(percorso)} celle")
    print(f"   - Cella max raggiungibile: {es38(labirinto)}")
    
    # Visualizza l'immagine
    visualizza_labirinto(labirinto,
                        dimensione_cella=6,
                        mostra_percorso=True,
                        percorso_path=percorso,
                        titolo=f"Labirinto {dimensione}x{dimensione}")
    
    return labirinto, stats

def menu_visualizzazione():
    """
    Menu dedicato alla visualizzazione di labirinti
    """
    print("\n" + "="*50)
    print("VISUALIZZAZIONE LABIRINTI")
    print("="*50)
    
    while True:
        print("\nOPZIONI:")
        print("1. Genera e visualizza labirinto (default)")
        print("2. Labirinto piccolo (20x20) - per test veloci")
        print("3. Labirinto medio (50x50) - bilanciato")
        print("4. Labirinto grande (100x100) - completo")
        print("5. Labirinto personalizzato")
        print("6. Salva labirinti come immagini")
        print("7. Torna al menu principale")
        
        try:
            scelta = input("\nScegli un'opzione (1-7): ").strip()
            
            if scelta == "1":
                labirinto, stats = genera_labirinto_con_visualizzazione()
                
            elif scelta == "2":
                labirinto, stats = genera_labirinto_con_visualizzazione(20, 0.3, 0.6)
                
            elif scelta == "3":
                labirinto, stats = genera_labirinto_con_visualizzazione(50, 0.35, 0.7)
                
            elif scelta == "4":
                labirinto, stats = genera_labirinto_con_visualizzazione(100, 0.35, 0.8)
                
            elif scelta == "5":
                try:
                    dim = int(input("Dimensione (es. 30): ") or "30")
                    dens = float(input("Densità ostacoli 0.1-0.6 (es. 0.35): ") or "0.35")
                    comp = float(input("Complessità 0.1-1.0 (es. 0.7): ") or "0.7")
                    labirinto, stats = genera_labirinto_con_visualizzazione(dim, dens, comp)
                except ValueError:
                    print("Valori non validi, uso valori di default.")
                    labirinto, stats = genera_labirinto_con_visualizzazione()
                
            elif scelta == "6":
                print("\nGenerazione di labirinti multipli per il salvataggio...")
                labirinti_multipli = {
                    "Labirinto_Semplice_20x20": genera_labirinto_bilanciato(20, 0.25, 0.5),
                    "Labirinto_Bilanciato_30x30": genera_labirinto_bilanciato(30, 0.35, 0.7),
                    "Labirinto_Complesso_40x40": genera_labirinto_bilanciato(40, 0.4, 0.8),
                    "Labirinto_Grande_50x50": genera_labirinto_bilanciato(50, 0.35, 0.9)
                }
                
                for nome, labirinto in labirinti_multipli.items():
                    print(f"Salvataggio: {nome}")
                    percorso = crea_percorso_visuale(labirinto)
                    
                    # Colori personalizzati per ogni tipo
                    if "Semplice" in nome:
                        colori = {
                            'libero': (255, 255, 255),
                            'ostacolo': (50, 50, 150),
                            'percorso': (255, 100, 100),
                            'sfondo': (240, 240, 240),
                            'start': (0, 200, 0),
                            'end': (200, 0, 200)
                        }
                    elif "Complesso" in nome:
                        colori = {
                            'libero': (245, 245, 245),
                            'ostacolo': (30, 30, 30),
                            'percorso': (255, 50, 50),
                            'sfondo': (250, 250, 250),
                            'start': (0, 150, 0),
                            'end': (150, 0, 150)
                        }
                    else:
                        colori = None  # Colori default
                    
                    visualizza_labirinto(labirinto,
                                       dimensione_cella=4,
                                       colori=colori,
                                       mostra_percorso=True,
                                       percorso_path=percorso,
                                       salva_file=f"{nome}.png",
                                       titolo=nome)
                
                print("Tutti i labirinti sono stati salvati!")
                
            elif scelta == "7":
                break
            else:
                print("Opzione non valida!")
                
        except KeyboardInterrupt:
            print("\nTorno al menu principale...")
            break
        except Exception as e:
            print(f"Errore: {e}")
            print("Riproviamo...")

def menu_principale():
    """
    Menu principale del sistema integrato
    """
    print("="*70)
    print("GENERATORE E VISUALIZZATORE LABIRINTI REALISTICI")
    print("="*70)
    print("Sistema completo per creare e visualizzare labirinti con:")
    print("- Percorsi multipli e vicoli ciechi")
    print("- Visualizzazione grafica avanzata") 
    print("- Percorso garantito sempre presente")
    print("- Salvataggio immagini")
    
    while True:
        print("\n" + "="*70)
        print("MENU PRINCIPALE:")
        print("1. Demo rapida (genera + visualizza)")
        print("2. Visualizzazione avanzata (menu dedicato)")
        print("3. Analisi comparativa algoritmi")
        print("4. Test sistema (labirinti multipli)")
        print("5. Esci")
        
        try:
            scelta = input("\nScegli un'opzione (1-5): ").strip()
            
            if scelta == "1":
                print("\nDEMO RAPIDA")
                print("-" * 30)
                genera_labirinto_con_visualizzazione(50, 0.35, 0.7)
                
            elif scelta == "2":
                menu_visualizzazione()
                
            elif scelta == "3":
                print("\nANALISI COMPARATIVA")
                print("-" * 30)
                # Confronto tra diversi parametri
                parametri = [
                    ("Semplice", 20, 0.25, 0.5),
                    ("Bilanciato", 30, 0.35, 0.7),
                    ("Complesso", 30, 0.45, 0.9),
                    ("Denso", 25, 0.5, 0.8)
                ]
                
                for nome, dim, dens, comp in parametri:
                    print(f"\n{nome} ({dim}x{dim}, dens={dens}, comp={comp}):")
                    labirinto = genera_labirinto_bilanciato(dim, dens, comp)
                    stats = analizza_labirinto_avanzato(labirinto)
                    percorso = crea_percorso_visuale(labirinto)
                    
                    print(f"  Ostacoli: {stats['percentuale_ostacoli']}%")
                    print(f"  Vicoli ciechi: {stats['vicoli_ciechi']}")
                    print(f"  Densità vicoli: {stats['densita_vicoli']}%")
                    print(f"  Lunghezza percorso: {len(percorso)}")
                    
                    # Visualizza automaticamente ogni configurazione
                    visualizza_labirinto(labirinto,
                                       dimensione_cella=8,
                                       mostra_percorso=True,
                                       percorso_path=percorso,
                                       titolo=f"Confronto: {nome}")
                
            elif scelta == "4":
                print("\nTEST SISTEMA")
                print("-" * 30)
                print("Generazione di diversi labirinti per test completo...")
                
                test_sizes = [10, 15, 20, 30]
                for size in test_sizes:
                    print(f"\nTest {size}x{size}:")
                    labirinto = genera_labirinto_bilanciato(size, 0.35, 0.7)
                    stats = analizza_labirinto_avanzato(labirinto)
                    
                    # Verifica che il percorso esista
                    percorso = crea_percorso_visuale(labirinto)
                    percorso_ok = len(percorso) > 0
                    
                    print(f"  Generazione: OK")
                    print(f"  Statistiche: {stats['celle_libere']} libere, {stats['ostacoli']} ostacoli")
                    print(f"  Percorso: {'OK' if percorso_ok else 'ERRORE'} ({len(percorso)} celle)")
                    print(f"  Vicoli ciechi: {stats['vicoli_ciechi']}")
                
                print("\nTest completato! Tutti i labirinti sono stati generati con successo.")
                
            elif scelta == "5":
                print("\nGrazie per aver usato il Generatore Labirinti!")
                print("Arrivederci!")
                break
                
            else:
                print("Opzione non valida! Scegli un numero da 1 a 5.")
                
        except KeyboardInterrupt:
            print("\n\nArrivederci!")
            break
        except Exception as e:
            print(f"\nErrore imprevisto: {e}")
            print("Il sistema continuerà a funzionare...")

def main():
    """
    Entry point del sistema integrato
    """
    # Verifica dipendenze
    try:
        from PIL import Image
        print("PIL/Pillow disponibile - Visualizzazione abilitata")
    except ImportError:
        print("PIL/Pillow non disponibile - Installare con: pip install Pillow")
        print("   La visualizzazione sarà limitata.")
    
    # Avvia il menu principale
    menu_principale()

if __name__ == "__main__":
    # Modalità auto-demo se richiesto
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            print("MODALITA DEMO AUTOMATICA")
            print("=" * 50)
            genera_labirinto_con_visualizzazione(30, 0.35, 0.7)
        elif sys.argv[1] == "test":
            print("MODALITA TEST AUTOMATICA")
            print("=" * 50)
            menu_principale()
        else:
            print("Uso: python sistema_integrato.py [demo|test]")
    else:
        main()