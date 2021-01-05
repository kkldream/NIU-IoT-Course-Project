import RPi.GPIO as GPIO
import time
# from flask import Flask, request, Response, jsonify, render_template
# import threading
RELAY_PIN = 14

# app = Flask(__name__)
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

def set_relay_on():
    # GPIO.output(RELAY_PIN, GPIO.LOW)
    init()
    # cleanup()

def set_relay_off():
    # GPIO.output(RELAY_PIN, GPIO.HIGH)
    cleanup()
    # init()

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        init()
        while True:
            set_relay_on()
            print('on')
            time.sleep(1)
            set_relay_off()
            print('off')
            time.sleep(1)
    finally:
        cleanup()
        print('end')