import evdev
import RPi.GPIO as GPIO
import time

# Code für den Raspberry Pi des GreenPi Projekts für die Tastensteuerung des Projekt GreenPi für den Infotag der Bertha-Benz-Schule-Sigmaringen
# Geschrieben von Esad Sahin der Klasse EKIT 2025

# Tastenbelegung: GPIO-Pin -> Zeichen
KEY_MAPPING = {
    17: evdev.ecodes.KEY_1,
    18: evdev.ecodes.KEY_2,
    27: evdev.ecodes.KEY_3,
    22: evdev.ecodes.KEY_4,
    23: evdev.ecodes.KEY_5,
    24: evdev.ecodes.KEY_6,
    25: evdev.ecodes.KEY_7,
    5: evdev.ecodes.KEY_8,
    6: evdev.ecodes.KEY_9,
    12: evdev.ecodes.KEY_0,
}

# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in KEY_MAPPING.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Virtuelles Eingabegerät erstellen
device = evdev.UInput()

def send_key(key_code):
    device.write(evdev.ecodes.EV_KEY, key_code, 1)  # Taste gedrückt
    device.write(evdev.ecodes.EV_KEY, key_code, 0)  # Taste losgelassen
    device.syn()

def main():
    try:
        while True:
            for pin, key_code in KEY_MAPPING.items():
                if GPIO.input(pin) == GPIO.LOW:
                    send_key(key_code)
                    time.sleep(0.2)  # Entprellung
    except KeyboardInterrupt:
        print("Beende Skript...")
        GPIO.cleanup()
        device.close()

if __name__ == "__main__":
    main()
