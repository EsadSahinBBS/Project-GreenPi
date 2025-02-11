# Project-GreenPi
Greenfoot games powered by Raspberry pi. 




Projekt für Infotag 2025 der Bertha-Benz TG/IT.
Ein retro style Cabinet wird mithilfe von einem Raspberry Pi 4 aufgebaut und optimiert um Java spiele der Klasses zu spielen. 
Natürlich ist das ganze nicht nur darauf beschränkt und könnte mit RetroPie combiniert werden also ist jeder Willkommen sich auf ein Peojekt zu wagen. 

Für unsere Version haben wir folgende Bauteile verwendet (was zumindest die Technick angeht):
- Raspberry Pi 4 B+ (2GB Modell)
- Raspberry Pi Kühlgehäuse (Optional aber empfohlen)
- Arduino UNO R3 (Jeder UNO mit I2C sollte passen)
- 2x 5V Analog Joystick-Module
- 8x 2 Pin Arcade-Tasten
- einen alten 17 Zoll 4:3 Monitor 
- Holzgehäuse

Wir begannen indem wir das Panel des Monitors aus dem ursprünglichen Gehäuse mamen und in unser Holzgehäuse für den Bau einsetzten.
Die Technick kam erst dannach. Für die Installation habe ich mich für den Raspberry Pi OS entschieden (Recalbox, Lakka oder RetroPie möglich). 
Für die Folgende Betriebssysteminstallation kann man das Gewünschte Betriebssystem auf einer SD Karte für den Zugehörigen Pi installieren. 
Hier geht es zum Download:

https://www.raspberrypi.com/software/

Im Betriebssystem angekommen muss gegebenfalls Python und die benötigte Bibliothek installiert werden:

```
sudo apt update
sudo apt install python3
sudo apt install python3-evdev
```

Anschließend muss das I2C-Protokoll der GPIO Pins aktiviert werden. Dazu verwendet ihr:
```
sudo raspi-config
```

Und geht über "Interface Options" auf die I2C Option.


Das war's vorerst mit dem Pi. 

Arduino UNO

Arduino UNO ist ein passender Mikrocontroller aufgrund der I2C compatibilität, welche direkte Kommunikation mit dem Pi ermöglicht, aber auch des simplicismus der Analog-Eingänge, als auch 5V und 3.3V unterstützung. In unserem Fall verwenden wir einen Arduino UNO R3. (jeder Arduino mit I2C und 4 Analog-Eingängen ist verwendbar mit ein paar Einstellungen in der Software). Um diesen zu Programmieren verwenden wir hierbei die Arduino IDE. Zum Download geht es hier:

https://www.arduino.cc/en/software

Angekommen in der Software verbindet ihr euren Arduino mit einem USB Kabel mit dem Computer und wählt diesen aus. 
Wir programmieren den Arduino die Werte der Analog-Eingänge A1-A4 über I2C weiterzuhgeben:

```
#include <Wire.h>

/*
* Code für den Arduino des Project GreenPi für den Infotag der Bertha-Benz-Schule Sigmaringen
* geschrieben von Esad Sahin der Klasse EKIT 2025
*/

void setup() {
  Wire.begin(0x08); // Arduino als I2C-Slave mit der Adresse 0x08 setzen
  Wire.onRequest(requestEvent); // Definiert was auf Datenanfrage passiert
}

void loop() {
  // Nichts hier. Daten werden nur auf Anfrage des Pis gesendet
}

void requestEvent() {
  int val1 = analogRead(A1) / 4; // X-Achse des ersten Joysticks
  int val2 = analogRead(A2) / 4; // Y-Achse des ersten Joysticks

  int val3 = analogRead(A3) / 4; // X-Achse des zweiten Joysticks
  int val4 = analogRead(A4) / 4; // Y-Achse des zweiten Joysticks

  // Die Werte weitergeben
  Wire.write(val1); 
  Wire.write(val2); 
  Wire.write(val3); 
  Wire.write(val4);  
}

```

Da wir den code haben können wir uns die Verbindungen der Geräte anschauen:

Arduino UNO | Raspberry Pi
3.3v |  3.3v
Vin  |  5v
GND  |  GND
SDA  |  SDA (GPIO 2)
SDC  |  SDC (GPIO 3)

Die Analog-Sticks werden so Verbunden:

Stick 1 (an Arduino):
5v  |  5v
GND |  GND
VRX |  A1
VRY |  A2

Stick 2 (an Arduino):
5v  |  5v
GND |  GND
VRX |  A3
VRY |  A4

Das finale Produkt sollte in etwa so aussehen:

![image](https://github.com/user-attachments/assets/ee029c1c-9a85-4759-b842-12aa72158c4f)

Zurück am Pi angekommen, erstellen wir jetzt den eigentlichen Code, welcher Tastatureingabe simuliert:

```
cd ~
mkdir controls
cd controls
sudo nano maini2c.py
```

Im folgendem Fenster fügt ihr nun den Python-Code für den Raspberry Pi ein:

```
import smbus
import time
from evdev import UInput, ecodes as e

# Code für den Raspberry Pi zum erhalten der I2C Werte des Arduinos für das GreenPi-Projekts für den Infotag der Bertha-Benz-Schule Sigmaringen
# Code von Esad Sahin der Klasse EKIT 2025


# I2C Protokoll initialisieren
bus = smbus.SMBus(1)  
arduino_addr = 0x08  

# Tastaturausgabe initialisieren
ui = UInput()

# Tastenbelegung definieren
KEYS = {
    "W": e.KEY_W,
    "A": e.KEY_A,
    "S": e.KEY_S,
    "D": e.KEY_D,
    "UP": e.KEY_UP,
    "DOWN": e.KEY_DOWN,
    "LEFT": e.KEY_LEFT,
    "RIGHT": e.KEY_RIGHT
}

# Threshold für Joystickbewegung
DEADZONE = 20  # Anpassen falls nötig
CENTER = 127   # Da A1, A2, A3, und A4 Werte von 0 bis 255 wiedergeben

# Track pressed keys
pressed_keys = set()

# Debug-Ausgabendrosselung
last_debug_time = 0
DEBUG_INTERVAL = 0.1  # 100ms

def press_key(key):
    if key not in pressed_keys:
        ui.write(e.EV_KEY, KEYS[key], 1)  # Press key
        ui.syn()
        pressed_keys.add(key)
        print(f"[KEY PRESS] {key}")  # Debug

def release_key(key):
    if key in pressed_keys:
        ui.write(e.EV_KEY, KEYS[key], 0)  # Release key
        ui.syn()
        pressed_keys.remove(key)
        print(f"[KEY RELEASE] {key}")  # Debug

try:
    while True:
        try:
            data = bus.read_i2c_block_data(arduino_addr, 0, 4)  # Read 4 bytes (2 for each joystick)
            x1, y1, x2, y2 = data[0], data[1], data[2], data[3]

            # Debug print rate limit
            current_time = time.time()
            if current_time - last_debug_time > DEBUG_INTERVAL:
                print(f"[DEBUG] Joystick 1 X: {x1}, Y: {y1} | Joystick 2 X: {x2}, Y: {y2}")
                last_debug_time = current_time

            # Joystick 1 (WASD)
            if x1 < CENTER - DEADZONE:
                press_key("A")
                release_key("D")
            elif x1 > CENTER + DEADZONE:
                press_key("D")
                release_key("A")
            else:
                release_key("A")
                release_key("D")

            if y1 < CENTER - DEADZONE:
                press_key("W")
                release_key("S")
            elif y1 > CENTER + DEADZONE:
                press_key("S")
                release_key("W")
            else:
                release_key("W")
                release_key("S")

            # Joystick 2 (Pfeiltasten)
            if x2 < CENTER - DEADZONE:
                press_key("LEFT")
                release_key("RIGHT")
            elif x2 > CENTER + DEADZONE:
                press_key("RIGHT")
                release_key("LEFT")
            else:
                release_key("LEFT")
                release_key("RIGHT")

            if y2 < CENTER - DEADZONE:
                press_key("UP")
                release_key("DOWN")
            elif y2 > CENTER + DEADZONE:
                press_key("DOWN")
                release_key("UP")
            else:
                release_key("UP")
                release_key("DOWN")

        except Exception as e:
            print("[ERROR] I2C Read Failed:", e)

        time.sleep(0.05)  # Verzögerung um pam zu vermeiden 

except KeyboardInterrupt:
    print("[EXIT] Programm wird gestoppt...")
    ui.close()

```

Nach dem Einfgen des codes, seichern mit Strg + X und anschließend die Anfrage auf Speichern mit Y (yes) und Enter beantworten. 
Beim Ausführen des codes mit 
```
sudo python3 maini2c.py
```
sollten die einzelnen Analog-Sticks WASD und Pfeiltasten simulieren und den Zustand im Terminal anzeigen. 
