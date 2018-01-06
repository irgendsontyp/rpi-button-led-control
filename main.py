import signal
import threading
import time
import RPi.GPIO as GPIO

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# define GPIO numbers for LED and button
GPIO_PIN_NR_LED = 40
GPIO_PIN_NR_BUTTON = 38

# LED needs output mode
GPIO.setup(GPIO_PIN_NR_LED, GPIO.OUT)

# Button needs input mode
GPIO.setup(GPIO_PIN_NR_SWITCH, GPIO.IN)

# Event object for handling SIGINT
ev = threading.Event()


# Cleanup function for application exit
def exitApplication():
	GPIO.output(GPIO_PIN_NR_LED, GPIO.LOW)
	GPIO.cleanup()


# Handler for SIGINT signal (for example when pressing CTRL + C in console)
def sigIntHandler(number, stackFrame):
	ev.set()


# Turn on LED for one second and turn it off again
def toggleLed(pin):
	GPIO.output(GPIO_PIN_NR_LED, GPIO.HIGH)		
	time.sleep(1)
	GPIO.output(GPIO_PIN_NR_LED, GPIO.LOW)	


# Register signal handler for SIGINT
signal.signal(signal.SIGINT, sigIntHandler)


# Register callback for falling voltage on the pin (= button released)
GPIO.add_event_detect(GPIO_PIN_NR_SWITCH, GPIO.FALLING, callback = toggleLed, bouncetime = 200) 


# Wait for SIGINT. Button handling is done via a separate thread created by GPIO.add_event_detect
ev.wait()


# Finally, exit the application
exitApplication()
