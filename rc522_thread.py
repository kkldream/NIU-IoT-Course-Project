import threading
import time

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

card_id = None
trigger = False

def job():
    global card_id, trigger
    reader = SimpleMFRC522()
    while True:
        card_read_id, _ = reader.read()
        print(f'[Theard] card_read_id：{card_read_id}')
        if card_read_id != card_id or time() - start_time > 5:
            start_time = time()
            card_id = card_read_id
            trigger = True
            print(f'[Theard] card_id：{card_id}')

try:
    threading.Thread(target = job).start()
    while True:
        if trigger:
            trigger = False
            print(f'card_id：{card_id}')
finally:
    GPIO.cleanup()