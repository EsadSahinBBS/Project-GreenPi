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
