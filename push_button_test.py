import time
from Recorder import start_AVrecording, stop_AVrecording
from transcribe import transcribe_file
from Player import play
from Config import AUDIO_CONFIG
import os


passed = False
pushButton = True
releaseButton = True
#while True: # Run forever
if pushButton:
   print("Button was pushed!")
   start_AVrecording("temp_audio.wav")
   passed = True

time.sleep(5)

if releaseButton:
    stop_AVrecording("temp_audio.wav")
    transcribe_file("temp_audio.wav")
    #play()
    cmd = "aplay -D hw:" + str(AUDIO_CONFIG['play_device']) + ",0 output.wav"
    print("Launching cmd : "+cmd)
    os.system(cmd)

