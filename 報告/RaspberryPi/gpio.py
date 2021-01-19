import RPi.GPIO as GPIO
RELAY_PIN = 14

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

def set_relay_on():
    # GPIO.output(RELAY_PIN, GPIO.LOW)
    init()

def set_relay_off():
    # GPIO.output(RELAY_PIN, GPIO.HIGH)
    cleanup()

def cleanup():
    GPIO.cleanup()