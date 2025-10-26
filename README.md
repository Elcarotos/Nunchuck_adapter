# Nunchuck-adapter

## Description
A wii nunchuck usb adapter for pc use.                                                                                                                                        
Plug and play outcome.                                                                                                                                                        
Only on windows but can be simply modified for linux version (no more details)

## Needs
- Adafruit RP2040 QT Trinkey (controller card)
- Adafruit Wii Nunchuck Breakout Adapter STEMMA QT (adapter)
- Wire JST SH 4-pin 50/100 mm  (connectivity)

## Assembly
Connect the wire to both the Wii adapter and the micro controller.
It's done !

## Initalisation
- You have to plug the controller card into your usb pc port while pressing the "BOOT" button.
- A usb key should be detected by the system.
- You copy/paste the file.uf2 which is provided (it will init CircuitPython).
- After that your usb key should disapear and a new one appear ("CIRCUITPY").
- You will have to copy/paste all the content of the system_folder.

## How it's work
The boot.py code initializes a receiver which takes 12C (nunchuck communication protocol) and send it to micro-controller.                                                    
The code.py program loops while listenings for inputs, when one is detected, the code convert it in usb en send it to the machine/pc.

## Debug
If you adapter doesn't work (the flashing red LED is the sign), you have to open again your usb key so :
- Press and release the "RST" button, at the same time press the "BOOT" button.
- The interface should show up again as "CIRCUITPY" too
- You will have to put the whole system_folder back in and click on "replace"
- If it continues to not work.. please contact me

## Post-scriptum
Other libraries or software may be required to run this system on "legal" platforms like Steam, etc...                                                                        
This system remains perfect for use on Python/PyGame and other programming languages.
