# Project-Greenpi
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
VRX |  A0
VRY |  A1

Stick 2 (an Arduino):
5v  |  5v
GND |  GND
VRX |  A2
VRY |  A3

Das finale Produkt sollte in etwa so aussehen:

![image](https://github.com/user-attachments/assets/ee029c1c-9a85-4759-b842-12aa72158c4f)

Zurück am Pi angekommen, erstellen wir jetzt den eigentlichen Code, welcher Tastatureingabe simuliert:

```
cd ~
mkdir controls
cd controls
sudo nano 
