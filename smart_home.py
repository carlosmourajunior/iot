import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO
from dweet import Dweet

GPIO_CS = GPIO.gpio_id('GPIO_CS')
BUTTON = GPIO.gpio_id('GPIO_A')
RELE = GPIO.gpio_id('GPIO_C')
LED = GPIO.gpio_id('GPIO_E')

pins = ((GPIO_CS, 'out'), (BUTTON, 'in'), (RELE, 'out'), (LED, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

system_status = 1

dweet = Dweet()


def readDigital(gpio):
	digital = [0,0]
	digital[0] = gpio.digital_read(LED)
	digital[1] = gpio.digital_read(RELE)

	return digital

def writeDigital(gpio, digital):
	write = digital
	gpio.digital_write(LED, write[0])
	gpio.digital_write(RELE, write[1])

	return digital


def detectaButton(gpio):
	global system_status
	status = gpio.digital_read(BUTTON)
	if status == 1:
		if system_status == 0:
			system_status = 1
			print "Sistema Ligado! \n"
		else:
			system_status = 0
			print "Sistema Desligado \n"

	return system_status


def readTemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100

	#print("Temperatura:%2.1f " %adc_temp)
	return adc_temp

def readLumi(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0x80, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)

	#print("Luminosidade: %d" %adcout)
	return  adcout

#def readDweet():


if __name__=='__main__':
	with GPIO(pins) as gpio:
		while True:
			digital = [0,0]
			if detectaButton(gpio) == 1:
				resposta = dweet.latest_dweet(name="inatel_ead")
			        digital[0] =  resposta['with'][0]['content']['led']
			        digital[1] =  resposta['with'][0]['content']['rele']
				writeDigital(gpio, digital)
				temp = readTemp(gpio)
				lumi = readLumi(gpio)
				digital = readDigital(gpio)
				print "Temp: %2.1f\nlumi: %d\nled: %d\nrele: %d" %(temp, lumi,
digital[0], digital[1])
				dweet.dweet_by_name(name="inatel_ead", data={"led":digital[0],
"rele": digital[1], "Temperatura":temp, "Luminosidade": lumi})

			time.sleep(10)
