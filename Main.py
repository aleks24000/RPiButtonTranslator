
#PiButtonTranslator
#A simple translator for raspberry pi (with push button)
#Test git

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os
import shlex
import subprocess
#from Recorder import start_AVrecording, stop_AVrecording
from transcribe import transcribe_file
#from Player import play
from Config import AUDIO_CONFIG

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

passed = False
proc = None
while True: # Run forever
    if GPIO.input(3) == GPIO.HIGH and not passed:
        print("Button was pushed!")
        time.sleep(0.5)
        passed = True
        command_line = "arecord --device=hw:" + str(AUDIO_CONFIG['record_device']) + ",0 --format S16_LE --rate " + str(
            AUDIO_CONFIG['rate']) + " -c" + str(AUDIO_CONFIG['channel']) + " temp_audio.wav &"
        args = shlex.split(command_line)
        proc = subprocess.Popen(args)
        print("PID:" + str(proc.pid))

    if GPIO.input(3) != GPIO.HIGH and passed:
        print("Button released")
        time.sleep(0.5)
        passed = False
        command_line = "kill " + str(proc.pid)
        os.system(command_line)
        if AUDIO_CONFIG['channel'] == 2:
            command_line = "sox temp_audio.wav -c 1 temp_audio_mono.wav"
            os.system(command_line)
        else:
            command_line = "cp temp_audio.wav temp_audio_mono.wav"
            os.system(command_line)
        command_line = "flac -f temp_audio_mono.wav"
        os.system(command_line)

        transcribe_file("temp_audio_mono.flac")
        # cmd = "aplay -D hw:" + str(AUDIO_CONFIG['play_device']) + ",0 output.wav"
        cmd = "aplay output.wav"
        print("Launching cmd : " + cmd)
        os.system(cmd)

