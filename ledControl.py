import RPi.GPIO as GPIO
import time
import core.flags

USER_LED = 17        # GPIO17 → pin 11
ASSISTANT_LED = 27   # GPIO27 → pin 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(USER_LED, GPIO.OUT)
GPIO.setup(ASSISTANT_LED, GPIO.OUT)


def ledUserSpeaking():
    GPIO.output(USER_LED, GPIO.HIGH)
    GPIO.output(ASSISTANT_LED, GPIO.LOW)

def ledAssistantSpeaking():
    GPIO.output(USER_LED, GPIO.LOW)
    GPIO.output(ASSISTANT_LED, GPIO.HIGH)

def ledOff():
    GPIO.output(USER_LED, GPIO.LOW)
    GPIO.output(ASSISTANT_LED, GPIO.LOW)

def cleanUp():
    GPIO.cleanup()

