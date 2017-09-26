#!/usr/bin/env python
from dweet import Dweet

import time

from gpio_96boards import GPIO

GPIO_A = GPIO.gpio_id('GPIO_A')
GPIO_C = GPIO.gpio_id('GPIO_C')
GPIO_E = GPIO.gpio_id('GPIO_E')

pins = (
    (GPIO_A, 'out'),(GPIO_C, 'out'),(GPIO_E, 'in'),
)

dweet = Dweet()

def liga():

	gpio.digital_write(GPIO_A, GPIO.HIGH)
	gpio.digital_write(GPIO_C, GPIO.HIGH)

	dweet.dweet_by_name(name="iplug", data={"button":1})
	resposta = dweet.latest_dweet(name="iplug")
	#print resposta['with'][0]['content']['button']


def desliga():

	gpio.digital_write(GPIO_A, GPIO.LOW)
	gpio.digital_write(GPIO_C, GPIO.LOW)

	dweet.dweet_by_name(name="iplug", data={"button":0})
	resposta = dweet.latest_dweet(name="iplug")
	#print resposta['content']


def run(gpio):

    status = 0
    while True:
        button_value = gpio.digital_read(GPIO_E)
	print "Botao:%d" %button_value
	print "Status:%d" %status	
        time.sleep(0.25)
	if button_value == 1:
	   if status == 0:
		   status = 1 
 		   liga()
	   else:
		   status = 0	
		   desliga()
	else:
	   resposta = dweet.latest_dweet(name="iplug")
           button_value_cloud = resposta['with'][0]['content']['button']
	   print "Cloud button: %d" %button_value_cloud
	   if button_value_cloud == 1:
		status = 1
		liga()
	   else:
		status = 0
		desliga()	   	
	
	time.sleep(1)
    
 
if __name__ == "__main__":

    
    with GPIO(pins) as gpio:
         run(gpio)

        
    

