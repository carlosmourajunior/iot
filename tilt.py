import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

TILT = GPIO.gpio_id('GPIO_A')

pins = ((TILT, 'in'),)

count = 0
sleep_count = 0


def detectTilt(gpio):
	status = gpio.digital_read(TILT)
	count = 0
	tilt_detected = 0
	while count < 100:
		if gpio.digital_read(TILT) != status:
			tilt_detected += 1
			print("Tilt Detected")
			if tilt_detected > 5:
				print("Problem Detected")
		time.sleep(0.02)

with GPIO(pins) as gpio:
	while True:
		detectTilt(gpio)
		time.sleep(0.5)
