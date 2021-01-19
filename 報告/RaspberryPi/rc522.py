from time import time
import mysql
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
    card_id = None
    mysql.connect()
    while True:
        card_read_id, _ = reader.read()
        if card_read_id != card_id or time() - start_time > 1:
            start_time = time()
            card_id = card_read_id
            student_id = mysql.find_id_user(card_id)
            my_data = {### HIDE ###}
            status_result = requests.post('http://192.168.1.20:5000/api', data = my_data)
            status_temp = None
            if eval(status_result.text)['status'] == 'shutdown':
                # print(student_id)
                if student_id != False:
                    status_temp = 'boot'
                    my_data = { 'action': 'debug',
                                'key': 'insert_status',
                                'student_id': str(student_id),
                                'status': status_temp}
                    r = requests.post('http://192.168.1.20:5000/api', data = my_data)
                    print(f'status={status_temp}')
                    print(r.text)
                else:
                    mysql.insert_unregistered_status(card_id, '')
                    print(f'card_id={card_id}')
            elif eval(status_result.text)['status'] == 'boot':
                if student_id == eval(status_result.text)['studio_id']:
                    status_temp = 'shutdown'
                    my_data = {### HIDE ###}
                    r = requests.post('http://192.168.1.20:5000/api', data = my_data)
                    print(f'status={status_temp}')
                    print(r.text)
                else:
                    mysql.insert_unregistered_status(card_id, '')
                    print(f'card_id={card_id}')    
finally:
    pass
    mysql.release()
    GPIO.cleanup()