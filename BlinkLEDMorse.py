import time
import board
import digitalio

# Set the GPIO number your LED is connector to
# Circuit Python version. Needs to be on boot.py for autorun (MicroPython wants main.py)
# Once in autorun Thonny can't open it. Need to use UF2 nuke to clear file system.
LED_PIN = led = digitalio.DigitalInOut(board.GP14)
LED_PIN.direction = digitalio.Direction.OUTPUT

text2morse = 'SOS'

MORSE = {'A': '.-',    'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'
        }

def dot():
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)

def start():
    for i in range(10):
        dot()
    time.sleep(1.5)

def dash():
    led.value = 1
    time.sleep(0.8)
    led.value = False
    time.sleep(0.2)

while True:
    start()
    for letter in text2morse:
        time.sleep(1.0)
        for symbol in MORSE[letter.upper()]:
            if symbol == '-':
                dash()
            elif symbol == '.':
                dot()
            else:
                time.sleep(1.4)
    time.sleep(5.0)
