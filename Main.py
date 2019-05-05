
#PiButtonTranslator

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os
from Recorder import start_AVrecording, stop_AVrecording
from transcribe import transcribe_file
from Player import play
from Config import AUDIO_CONFIG

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

passed = False
while True: # Run forever
    if GPIO.input(3) == GPIO.HIGH and not passed:
        print("Button was pushed!")
        time.sleep(0.5)
        start_AVrecording()
        passed = True
        #break

    if GPIO.input(3) != GPIO.HIGH and passed:
        print("Button released")
        time.sleep(0.5)
        stop_AVrecording()
        transcribe_file("temp_audio.wav")
        # play()
        cmd = "aplay -D hw:" + str(AUDIO_CONFIG['play_device']) + ",0 output.wav"
        print("Launching cmd : " + cmd)
        os.system(cmd)

