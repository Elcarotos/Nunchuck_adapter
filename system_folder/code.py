# Fichier: code.py
# Convertisseur Nunchuk Simple vers Gamepad USB
# Materiel: Trinkey QT2040, Adaptateur Nunchuk
# Bibliotheques requises dans /lib: adafruit_nunchuk

import time
import board
import busio
import usb_hid
from adafruit_nunchuk import Nunchuk
from digitalio import DigitalInOut, Pull # ESSENTIEL pour les pull-ups I2C

# --- Classe Gamepad simplifiee (integree) ---
class Gamepad:
    """Emule un Gamepad generique avec 16 boutons et 4 axes (-127 a 127)."""

    # CORRECTION CRUCIALE APPORTEE ICI:
    # Le paramètre 'devices' est le tuple usb_hid.devices
    def __init__(self, devices):
        # Nous extrayons le Gamepad (qui est le seul et donc le premier element [0])
        # du tuple usb_hid.devices.
        self._gamepad_device = devices[0]

        # Rapport de 8 octets, standard pour la definition HID dans boot.py
        self._report = bytearray(8)
        self._last_report = bytearray(8)

        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0

        self.reset_all()

    def press_buttons(self, *buttons):
        for button in buttons:
            self._buttons_state |= 1 << (button - 1)
        self._send()

    def release_buttons(self, *buttons):
        for button in buttons:
            self._buttons_state &= ~(1 << (button - 1))
        self._send()

    def move_joysticks(self, x=None, y=None, z=None, r_z=None):
        if x is not None:
            self._joy_x = x
        if y is not None:
            self._joy_y = y
        if z is not None:
            self._joy_z = z
        if r_z is not None:
            self._joy_r_z = r_z
        self._send()

    def reset_all(self):
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._send()

    def _send(self):
        # Les 2 premiers octets gerent les 16 boutons
        self._report[0] = self._buttons_state & 0xFF
        self._report[1] = (self._buttons_state >> 8) & 0xFF

        # Les octets 2 a 5 gerent les 4 axes (X, Y, Z, Rz)
        self._report[2] = self._joy_x & 0xFF
        self._report[3] = self._joy_y & 0xFF
        self._report[4] = self._joy_z & 0xFF
        self._report[5] = self._joy_r_z & 0xFF
        # Les octets restants sont du padding ou reserves

        if self._report != self._last_report:
            # Cette ligne fonctionne maintenant car _gamepad_device est l'objet Gamepad
            self._gamepad_device.send_report(self._report)
            self._last_report[:] = self._report

# --- Fonctions utilitaires ---
def map_nunchuk_axis_to_hid(value):
    """Mappe une valeur d'axe Nunchuk (typ. 30-220) a la plage HID (-127 a 127)."""
    # Decalage du centre (127.5) et limitation
    mapped_val = value - 128

    if mapped_val > 127:
        mapped_val = 127
    elif mapped_val < -127:
        mapped_val = -127

    return mapped_val

# --- INITIALISATION DU MATERIEL ---

# 1. Configuration des pull-ups I2C
# CECI A CORRIGE L'ERREUR "Aucun pull up trouve"
print("Configuration I2C (Pull-ups)...")
try:
    sda_pin = DigitalInOut(board.SDA)
    scl_pin = DigitalInOut(board.SCL)
    sda_pin.pull = Pull.UP
    scl_pin.pull = Pull.UP
    sda_pin.deinit() # On les relache pour que busio les prenne
    scl_pin.deinit() # On les relache pour que busio les prenne
except Exception as e:
    print(f"Erreur de configuration Pull-up: {e}")

# 2. Initialisation du bus I2C et du Nunchuk
print("Initialisation du Nunchuk...")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    time.sleep(1) # Petit delai pour stabiliser l'I2C
    # CORRECTION : Suppression de with_accel=True
    nunchuk = Nunchuk(i2c)
    print("Nunchuk initialise avec succes. Demarrage de la manette...")
except Exception as e:
    print(f"ECHEC Nunchuk: {e}")
    print("Verifiez le cablage I2C (SDA, SCL, VCC, GND).")
    while True:
        time.sleep(1)

# 3. Initialisation du Gamepad USB
# usb_hid.devices est un tuple, nous le passons a la classe Gamepad
joystick_usb = Gamepad(usb_hid.devices)
print("Demarrage du Gamepad USB...")


# --- BOUCLE PRINCIPALE ---
while True:
    buttons_to_press = []

    try:
        # 1. Lecture des donnees
        x_joy, y_joy = nunchuk.joystick
        # Assurez-vous que nunchuk.acceleration est toujours disponible
        x_accel, y_accel, z_accel = nunchuk.acceleration

        # 2. Mappe les 4 axes HID
        joystick_usb.move_joysticks(
            x=map_nunchuk_axis_to_hid(x_joy),  # Joystick X -> Axe X
            y=map_nunchuk_axis_to_hid(y_joy),  # Joystick Y -> Axe Y
            z=map_nunchuk_axis_to_hid(x_accel),  # Accel X -> Axe Z
            r_z=map_nunchuk_axis_to_hid(y_accel) # Accel Y -> Axe RZ
        )

        # 3. Mappe boutons C (Bouton 1) et Z (Bouton 2)
        if nunchuk.buttons[0]:
            buttons_to_press.append(1) # Bouton 1 (C)
            print("C: APPUYE")
        if nunchuk.buttons[1]:
            buttons_to_press.append(2) # Bouton 2 (Z)
            print("Z: APPUYE")

        # 4. Envoie le rapport HID (Pression)
        joystick_usb.press_buttons(*buttons_to_press)

        # 5. Envoie le rapport HID (Relachement)
        if not nunchuk.buttons[0]:
            joystick_usb.release_buttons(1)
        if not nunchuk.buttons[1]:
            joystick_usb.release_buttons(2)

    except OSError as e:
        print(f"Erreur de lecture Nunchuk (OSError): {e}")
        joystick_usb.reset_all()

    time.sleep(0.01)
