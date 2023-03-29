import time
import pyfirmata

comport = 'COM5'

board = pyfirmata.Arduino(comport)

# Set up the LED on pin 13
led_pin = board.get_pin('d:13:o')

# Blink the LED 5 times
for i in range(10):
    led_pin.write(1)  # Turn the LED on
    time.sleep(1)   # Wait for 0.5 seconds
    led_pin.write(0)  # Turn the LED off
    time.sleep(1)   # Wait for 0.5 seconds

# Clean up the board
board.exit()
