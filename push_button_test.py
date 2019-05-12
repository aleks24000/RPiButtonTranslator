import time
import subprocess
#from Recorder import start_AVrecording, stop_AVrecording
from transcribe import transcribe_file
from Player import play
from Config import AUDIO_CONFIG
import os
import shlex


passed = False
pushButton = True
releaseButton = True
proc = None
#while True: # Run forever
if pushButton:
   print("Button was pushed!")
   #start_AVrecording("temp_audio.wav")
   command_line="arecord --device=hw:"+str(AUDIO_CONFIG['record_device'])+",0 --format S16_LE --rate "+str(AUDIO_CONFIG['rate'])+" -c"+str(AUDIO_CONFIG['channel'])+" temp_audio.wav &"
   args = shlex.split(command_line)
   proc = subprocess.Popen(args)
   print ("PID:"+str(proc.pid))
   passed = True

time.sleep(5)

if releaseButton:
#    stop_AVrecording("temp_audio.wav")
    command_line = "kill "+str(proc.pid)
    os.system(command_line)
    #print("PID:" + str(proc.pid))
    if AUDIO_CONFIG['channel']==2:
        command_line = "sox temp_audio.wav -c 1 temp_audio_mono.wav"
        os.system(command_line)
    else:
        command_line = "cp temp_audio.wav temp_audio_mono.wav"
        os.system(command_line)
    command_line = "flac -f temp_audio_mono.wav"
    os.system(command_line)

    transcribe_file("temp_audio_mono.flac")
    #play()
    #cmd = "aplay -D hw:" + str(AUDIO_CONFIG['play_device']) + ",0 output.wav"
    cmd = "aplay output.wav"
    print("Launching cmd : "+cmd)
    os.system(cmd)

