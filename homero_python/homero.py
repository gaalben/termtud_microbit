import serial
import matplotlib.pyplot as plt
#pip install matplotlib és pip install pyserial kell consolban alul, hogy menjen

# Soros port beállítása, meg kell nézni, hogy melyik porton van a microbit és a makecode felületet bezárni
SERIAL_PORT = 'COM3'
BAUDRATE = 115200 

# A soros port beállítása, a microbit által használt port és a baudrate
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

# Az ábra létrehozása két alábrával: oszlopdiagram és vonaldiagram
fig, (ax_bar, ax_line) = plt.subplots(2, 1, figsize=(8, 6))


mablak = []
global_min = None
global_max = None

while True:
    try:
        line = ser.readline().decode().strip()
        # Beolvassa a soros portból érkező adatokat
        if line:
            value = round(float(line), 2)
            # A beolvasott érték kerekítése két tizedesjegyre

            mablak.append(value)
            if len(mablak) > 50:  # Csak az utolsó 50 értéket mutatjuk, ez az also diagramnál fog kelleni
                # Ha több mint 50 érték van, eltávolítjuk a legrégebbit
                # Ez segít a memóriahasználat csökkentésében és a diagramok frissítésében
                mablak.pop(0)

            # Frissítjük a globális minimumot és maximumot, classic maxkiválasztás
            if global_min is None or value < global_min:
                global_min = value
            if global_max is None or value > global_max:
                global_max = value

            print("Beolvasott érték:", value) # Debugging output
            
            # Oszlopdiagram frissítése
            ax_bar.cla()
            ax_bar.bar(['Hőmérséklet'], [value], color='red')
            #a szenzor 0-tól 100-ig terjedő értékeket ad vissza, de a hőmérséklet 10 és 30 között van, így látványosabb
            ax_bar.set_ylim(10, 40)
            ax_bar.set_title('Valós idejű hőmérséklet')
            ax_bar.set_ylabel('Érték')
            # Fix position for the value text under the title
            ax_bar.text(0, 39, f"{value} °C", ha='center', va='top', fontsize=14, color='black')
        
            
            # Vonaldiagram frissítése
            ax_line.cla()
            ax_line.plot(mablak, color='orange', marker='o', label="Aktuális hőmérséklet")
            ax_line.set_ylim(10, 40)
            ax_line.set_title('Hőmérséklet változása')
            ax_line.set_xlabel('Idő(ms)')
            ax_line.set_ylabel('Érték')

            # Teljes futás alatti minimum és maximum megjelenítése
            # axhline függvények: vízszintes vonalakat rajzolnak a diagramra
            if global_min is not None and global_max is not None:
                ax_line.axhline(global_min, color='blue', linestyle='--', label=f"Futás min: {global_min} °C")
                ax_line.axhline(global_max, color='red', linestyle='--', label=f"Futás max: {global_max} °C")
                ax_line.legend(loc='upper right')

            plt.pause(0.1)
    except KeyboardInterrupt:
        print("Kilépés...")
        break

ser.close()
print("Serial connection closed.")