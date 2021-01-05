import threading
from time import time, sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

card_id = None
trigger = False

def job():
    # global card_id, trigger
    reader = SimpleMFRC522()
    while True:
        card_read_id, _ = reader.read()
        print(f'[Theard] card_read_id：{card_read_id}')
        # if card_read_id != card_id or time() - start_time > 5:
        #     start_time = time()
        #     card_id = card_read_id
        #     trigger = True
        #     print(f'[Theard] card_id：{card_id}')

t = threading.Thread(target = job)
t.start()
try:
    while True:
        print(f'{time()}')
        # sleep(1)
    t.join()
finally:
    pass
    GPIO.cleanup()