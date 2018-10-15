#!/usr/bin/env python3
from gpiozero import Button, LED
from signal import pause
import os
import sys
import time
from mpd import MPDClient

#GPIO pins that we use for this
#18, 19, 21 are in use by the Speaker Bonnet, do not use them!!
offGPIO = 3
ledGPIO = 17

#turn on the LED to get some feedback when the system is ready
led = LED(ledGPIO)
led.blink(on_time=0.5, off_time=0.5)

mpdClient = MPDClient() 
mpdClient.connect("localhost", 6600)
mpdClient.play(0)
mpdClient.stop()
mpdClient.clear()
mpdClient.add("Hallo Mattis.m4a")
mpdClient.play(0)

#this waits for the off switch to be pushed
btn = Button(offGPIO)
btn.wait_for_press()
led.off() #remember to turn off the LEDs

mpdClient = MPDClient() 
mpdClient.connect("localhost", 6600)
mpdClient.stop()
mpdClient.clear()
mpdClient.add("Tschüß.m4a")
mpdClient.play(0)
time.sleep(3.0)

#shutdown the system
os.system("sudo shutdown -h now")