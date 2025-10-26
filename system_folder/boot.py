# Fichier boot.py - Version CORRIGÉE
# N'active que le Gamepad HID.

import usb_hid

# --- Descripteur de Rapport Gamepad STANDARD (8 octets) ---
GAMEPAD_REPORT_DESCRIPTOR = (
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x05,        # Usage (Gamepad)
    0xA1, 0x01,        # Collection (Application)
    
    # --- MODIFICATION 1 : AJOUT DU REPORT ID ---
    0x85, 0x01,        # Report ID (1)
    
    0xA1, 0x00,        # Collection (Physical)

    # 16 Boutons (2 octets)
    0x05, 0x09,        # Usage Page (Button)
    0x19, 0x01,        # Usage Minimum (Button 1)
    0x29, 0x10,        # Usage Maximum (Button 16)
    0x15, 0x00,        # Logical Minimum (0)
    0x25, 0x01,        # Logical Maximum (1)
    0x75, 0x01,        # Report Size (1)
    0x95, 0x10,        # Report Count (16)
    0x81, 0x02,        # Input (Data, Var, Abs)

    # 4 Axes: X, Y, Z, Rz (4 octets)
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x30,        # Usage (X)
    0x09, 0x31,        # Usage (Y)
    0x09, 0x32,        # Usage (Z)
    0x09, 0x35,        # Usage (Rz)
    0x16, 0x81, 0x7F,  # Logical Minimum (-127)
    0x26, 0x7F, 0x00,  # Logical Maximum (127)
    0x75, 0x08,        # Report Size (8)
    0x95, 0x04,        # Report Count (4)
    0x81, 0x02,        # Input (Data, Var, Abs)

    # Padding final (2 octets) pour un rapport de 8 octets total
    0x75, 0x08,        # Report Size (8)
    0x95, 0x02,        # Report Count (2)
    0x81, 0x03,        # Input (Cnst, Var, Abs)

    0xC0,              # End Collection
    0xC0               # End Collection
)

# Definit le Gamepad
custom_gamepad_device = usb_hid.Device(
    report_descriptor=bytes(GAMEPAD_REPORT_DESCRIPTOR),
    usage_page=0x01,
    usage=0x05,
    report_ids=(1,),   # On déclare utiliser le Report ID 1 (notez la virgule)
    in_report_lengths=bytearray([8]),
    out_report_lengths=bytearray([0]),
)

# Active le Gamepad USB en tant que SEUL peripherique USB HID
try:
     usb_hid.enable(
        (custom_gamepad_device,),
        boot_device=0,
    )
except Exception:
    raise