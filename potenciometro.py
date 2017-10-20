import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_A')

pins = ((GPIO_CS, 'out'),(RELE, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

def readtemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)		
	print ("Valor do Pot.:%d" %adcout)
	return adcout
	
while True:
	with GPIO(pins) as gpio:
		value = readtemp(gpio)
		if value > 500:
			gpio.digital_write(RELE, GPIO.HIGH)
		else:
			gpio.digital_write(RELE, GPIO.LOW)		

		time.sleep(0.5)




	
