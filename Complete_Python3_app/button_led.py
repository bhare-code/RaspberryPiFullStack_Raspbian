from signal import signal, SIGINT
from sys import exit
import RPi.GPIO as GPIO       ## Import GPIO Library
import time


def int_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Cleaning up GPIOs.')
    GPIO.cleanup()
    exit(0)

if __name__ == '__main__':
    signal(SIGINT, int_handler)   # Catch CTRL-C
    inPin = 8                     ## Switch connected to pin 8
    ledPin = 7                    ## LED connected to pin 7
    GPIO.setwarnings(False)       ## Turn off warnings
    GPIO.setmode(GPIO.BOARD)      ## Use BOARD pin numbering
    GPIO.setup(inPin, GPIO.IN)    ## Set pin 8 to INPUT
    GPIO.setup(ledPin, GPIO.OUT)  ## Set pin 7 to OUTPUT

    while True:                   ## Do this forever
        value = GPIO.input(inPin) ## Read input from switch
        print(value)

        if value:                 ## If switch is released
            print("Pressed")
            GPIO.output(ledPin, GPIO.HIGH)  ## Turn LED on
        else:                     ## Else switch is pressed
            print("Not Pressed")
            GPIO.output(ledPin, GPIO.LOW)   ## Turn LED off
        time.sleep(0.1)
