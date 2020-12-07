import RPi.GPIO as GPIO
import time

RELAY_PIN = 14

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

def set_relay_on():
    GPIO.output(RELAY_PIN, GPIO.LOW)

def set_relay_off():
    GPIO.output(RELAY_PIN, GPIO.HIGH)

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        init()
        set_relay_on()
        time.sleep(1)
        set_relay_off()
    finally:
        cleanup()