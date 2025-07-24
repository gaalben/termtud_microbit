import serial # A serial modul importálása a soros kommunikációhoz
import matplotlib.pyplot as plt # A matplotlib.pyplot importálása a radar diagramhoz
import math  # A math modul importálása a szög konvertálásához



# Soros port beállítása, meg kell nézni, hogy melyik porton van a microbit és a makecode felületet bezárni
SERIAL_PORT = 'COM7' # A soros port neve, amely a microbit-hez csatlakozik
BAUDRATE = 115200  # A soros port sebessége, amely megegyezik a microbit beállításával
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) # Soros port megnyitása a megadott sebességgel


# A radar diagram beállítása
plt.figure() # Új ábra létrehozása, amelyen a diagram megjelenik
ax = plt.subplot(polar=True)  # Poláris diagram létrehozása
ax.set_ylim(0, 400)  # A maximális távolság beállítása 400 cm-re, a vonalak közötti távolság automatikusan igazodik
ax.set_theta_zero_location("N")  # Az északi irány (felső) beállítása 0 fokra
ax.set_theta_direction(-1)  # Az irány beállítása óramutató járásával megegyezőre

# Változó az első szög tárolására
kezdo_szog = None

# Változó a radar pontok tárolására
radar = None 

# Adatok olvasásának indítása
while True: # Végtelen ciklus, amíg a program fut
    try:
        # Olvasson be egy sort a soros portból
        line = ser.readline().decode().strip().split(',')
        if line:
            #print("Nyers adatok:", line)  # Nyers adatok megjelenítése hibakereséshez

            # Az adatok számokká konvertálása
            tav = float(line[0])
            szog = float(line[1])

            # Az első szög beállítása elülső szögként
            if kezdo_szog is None:
                kezdo_szog = szog

            # A szög beállítása az első szöghöz képest
            igazitott_szog = szog - kezdo_szog

            # A scatter plot frissítése az egész diagram törlése nélkül
            


            radar = ax.scatter(math.radians(igazitott_szog), tav, color='red') # A pont hozzáadása a diagramhoz, a szöget radiánba konvertálva

            plt.pause(0.1)  # Szünet a diagram frissítéséhez, enélkül a diagram nem frissül
            radar.remove()
    
    except KeyboardInterrupt: # A program leállítása, amikor a felhasználó megnyomja a Ctrl+C-t
        print("Kilépés...")
        break
# A soros kapcsolat bezárása
ser.close()