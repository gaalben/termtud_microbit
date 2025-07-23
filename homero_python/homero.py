import serial
import matplotlib.pyplot as plt
#külső könyvtárak importálása
#serial: soros port kommunikációhoz, matplotlib.pyplot: grafikonok rajzolás

# Soros port beállítása, meg kell nézni, hogy melyik porton van a microbit és a makecode felületet bezárni
SERIAL_PORT = 'COM3'
BAUDRATE = 115200 

# A soros port beállítása, a microbit által használt port és a baudrate megadásával
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

# Az ábra létrehozása két alábrával: oszlopdiagram és vonaldiagram
fig, (ax_bar, ax_line) = plt.subplots(2, 1, figsize=(8, 6))



mablak = [] # Ez a lista fogja tárolni az utolsó 50 értéket, amit a vonaldiagramon mutatunk
global_min = None # Globális minimum érték, ami a teljes futás alatt változik
global_max = None # Globális maximum érték, ami a teljes futás alatt változik


while True:# Végtelen ciklus, amíg a program fut
    try: 
        line = ser.readline().decode().strip()
        # Beolvassa a soros portból érkező adatokat, dekódolja és eltávolítja a felesleges szóközöket
        if line:
            value = round(float(line), 2)# A beolvasott érték kerekítése két tizedesjegyre
            mablak.append(value)    # Hozzáadja az értéket a mablak listához


            if len(mablak) > 50:  # Csak az utolsó 50 értéket tartjuk meg
                # Ha több mint 50 érték van, eltávolítjuk a legrégebbit
                # Ez segít a memóriahasználat csökkentésében és a diagramok frissítésében
                mablak.pop(0)

            # Frissítjük a globális minimumot és maximumot, klasszikus max-min kiválasztással
            if global_min is None or value < global_min:
                global_min = value
            if global_max is None or value > global_max:
                global_max = value

            
            # Oszlopdiagram frissítése
            ax_bar.cla() # Töröljük az előző adatokat az oszlopdiagramról, ezzel frissítjük
            ax_bar.bar(['Hőmérséklet'], [value], color='red')   # Oszlopdiagram frissítése, a hőmérséklet értékkel, piros színnel
            ax_bar.set_ylim(10, 40) # Az oszlopdiagram y-tengelyének beállítása 10 és 40 között, szobahőmérséklet körüli tartományban
            ax_bar.set_title('Valós idejű hőmérséklet') # Diagram címének beállítása
            ax_bar.set_ylabel('Érték') # Y-tengely címének beállítása
            ax_bar.text(0, 39, f"{value} °C", ha='center', va='top', fontsize=14, color='black')
            # A hőmérséklet értékének kiírása az oszlopdiagram tetejére a 39-es értékhez
        
            
            # Vonaldiagram frissítése
            ax_line.cla() # Töröljük az előző adatokat a vonaldiagramról, ezzel frissítjük
            ax_line.plot(mablak, color='orange', marker='o', label="Aktuális hőmérséklet")
            # Vonaldiagram frissítése, az utolsó 50 értékkel, narancssárga színnel és kör alakú jelölőkkel
            ax_line.set_ylim(10, 40) # A vonaldiagram y-tengelyének beállítása 10 és 40 között, szobahőmérséklet körüli tartományban
            ax_line.set_title('Hőmérséklet változása') # Diagram címének beállítása
            ax_line.set_xlabel('Idő(ms)') # X-tengely címének beállítása
            ax_line.set_ylabel('Érték') # Y-tengely címének beállítása

            # Teljes futás alatti minimum és maximum megjelenítése
            if global_min is not None and global_max is not None:
                ax_line.axhline(global_min, color='blue', linestyle='--', label=f"Futás min: {global_min} °C")
                # Kék színű vízszintes vonal a globális minimum értéknél
                ax_line.axhline(global_max, color='red', linestyle='--', label=f"Futás max: {global_max} °C") 
                # Piros színű vízszintes vonal a globális maximum értéknél
                ax_line.legend(loc='upper right') # Jelmagyarázat hozzáadása a vonaldiagramhoz

            plt.pause(0.1)
    
    
    except KeyboardInterrupt: # A program leállítása Ctrl+C-vel
        print("Kilépés...")
        break

ser.close()