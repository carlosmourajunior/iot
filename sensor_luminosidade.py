import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
LED = GPIO.gpio_id('GPIO_A')

pins = ((GPIO_CS, 'out'), (LED, 'out'),)

sensibilidade = 500

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

def readadc(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)	

	led_status = "Desligado"

	if adcout > sensibilidade:
				
		gpio.digital_write(LED, GPIO.HIGH)
		led_status = "Ligado"

	else: 
		gpio.digital_write(LED, GPIO.LOW)		
		led_status = "Apagado"
	
	print (adcout)
	print ("Status do LED:%s" %led_status)

	return r

while True:
	with GPIO(pins) as gpio:
		value = readadc(gpio)
		time.sleep(0.5)




	
