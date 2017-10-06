import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

TILT = GPIO.gpio_id('GPIO_A')

pins = ((TILT, 'in'),)

count = 0
sleep_count = 0

with GPIO(pins) as gpio:
	while True:

		value = gpio.wait_for_interrupt(1)								
		print("Contador:" , count)
