import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

TOQUE = GPIO.gpio_id('GPIO_A')
RELAY = GPIO.gpio_id('GPIO_C')

pins = ((TOQUE, 'in'), (RELAY, 'out'),)

with GPIO(pins) as gpio:
	while True:

		button_value = gpio.digital_read(TOQUE)

		if button_value == 1:
			gpio.digital_write(RELAY, 1)
		else:
			gpio.digital_write(RELAY, 0)

		print("Status do Rele: %d" %button_value)

		time.sleep(1)
