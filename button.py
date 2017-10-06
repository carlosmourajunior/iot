import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

BUTTON = GPIO.gpio_id('GPIO_A')
RELAY = GPIO.gpio_id('GPIO_C')

pins = ((TILT, 'in'), (RELAY, 'out'),)

count = 0
sleep_count = 0

with GPIO(pins) as gpio:
	while True:

		button_value = gpio.digital_read(TILT)

		if button_value == 1:
			gpio.digital_write(BUTTON, 1)
		else:
			gpio.digital_write(BUTTON, 0)

		time.sleep(1)
