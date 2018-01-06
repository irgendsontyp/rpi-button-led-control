import signal
import threading
import time
import RPi.GPIO as GPIO

# Pin-Nummern wie auf dem Raspberry Board verwenden
GPIO.setmode(GPIO.BOARD)

GPIO_PIN_NR_LED = 40
GPIO_PIN_NR_SWITCH = 38

GPIO.setup(GPIO_PIN_NR_LED, GPIO.OUT)
GPIO.setup(GPIO_PIN_NR_SWITCH, GPIO.IN)


ev = threading.Event()


def exitApplication():
	GPIO.output(GPIO_PIN_NR_LED, GPIO.LOW)
	GPIO.cleanup()

def sigIntHandler(number, stackFrame):
	ev.set()


def toggleLed(pin):
	GPIO.output(GPIO_PIN_NR_LED, GPIO.HIGH)		
	time.sleep(1)
	GPIO.output(GPIO_PIN_NR_LED, GPIO.LOW)	


signal.signal(signal.SIGINT, sigIntHandler)


GPIO.add_event_detect(GPIO_PIN_NR_SWITCH, GPIO.FALLING, callback = toggleLed, bouncetime = 200) 

ev.wait()

exitApplication()
