import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO

GPIO_A = GPIO.gpio_id('GPIO_B')
pins = (
 (GPIO_A, 'out'),
)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=10000
spi.mode = 0b00
spi.bits_per_word = 8

def readadc(gpio):
    gpio.digital_write(GPIO_A, GPIO.HIGH)
    time.sleep(0.0002)
    gpio.digital_write(GPIO_A, GPIO.LOW)
    r = spi.xfer2([0x01, 0x80, 0x00])
    gpio.digital_write(GPIO_A, GPIO.HIGH)
    adcout = (r[1] << 8) & 0b1100000000
    adcout = adcout | (r[2] & 0xff)
    return adcout

while True:
 with GPIO(pins) as gpio:
     value = readadc(gpio)
     print("value = %d" % value)
     print(" ---------------------- " )
     time.sleep(0.5)
