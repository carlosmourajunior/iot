import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
TILT = GPIO.gpio_id('GPIO_A')

pins = ((GPIO_CS, 'out'), (TILT, 'in'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

def detectaTilt(gpio):
	status = gpio.digital_read(TILT)
	tilt_detected = 0
	sleep_count = 0
	while sleep_count < 1000:
		if gpio.digital_read(TILT) != status:
			tilt_detected += 1
			status = gpio.digital_read(TILT)
			if tilt_detected > 5:
				print("Problem Detected")
				tilt_detected = 0
				break
		sleep_count += 1
		time.sleep(0.002)


def readTemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0x80, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100

	print("Temperatura:%2.1f " %adc_temp)


def readLumi(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)

	print("Luminosidade: %d" %adcout)

if __name__=='__main__':

	with GPIO(pins) as gpio:
		while True:
			readTemp(gpio)
			readLumi(gpio)
			detectaTilt(gpio)
			time.sleep(0.5)
