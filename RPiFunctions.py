import os
import shlex
import subprocess
from Config import AUDIO_CONFIG
from drive_quickstart import upload
import glob

proc = None
sessionFile = None
NB_MAX_FLAC = 5

def findFileName():
    files = glob.glob("*.flac")
    files.sort(key=os.path.getmtime, reverse=True)
    print("\n".join(files))
    if len(files)>NB_MAX_FLAC:
        for x in range(len(files)):
            if x>=NB_MAX_FLAC:
                os.remove(files[x])

    if len(files)>0:
        newfile = files[0]
        newfile = newfile[8:]
        newfile = newfile[:-5]
        inc = int(newfile)+1
        return "session-"+str(inc)
    else:
        return "session-1"

def start( debug ):
    print ("Start gb")
    global sessionFile
    audiofile = findFileName()
    sessionFile = audiofile
    print ("Recording to "+ sessionFile)
    start_rec( debug )
    return audiofile

def upload_file():
    print("Upload "+sessionFile)
    upload(sessionFile)

def start_rec( debug ):
    print("Start!")
    if debug is False :
        command_line = "arecord --device=hw:" + str(AUDIO_CONFIG['record_device']) + ",0 --format S16_LE --rate " + str(AUDIO_CONFIG['rate']) + " -c" + str(AUDIO_CONFIG['channel']) + " "+sessionFile+".wav &"
        args = shlex.split(command_line)
        global proc
        proc = subprocess.Popen(args)
        print("PID:" + str(proc.pid))
    else:
        print("Mock Recording")
        os.system("touch "+sessionFile+".flac")

def stop_rec(debug):
    print("Stop!")
    if debug is False:
        global proc
        command_line = "kill " + str(proc.pid)
        os.system(command_line)
        if AUDIO_CONFIG['channel'] == 2:
            command_line = "sox "+sessionFile+".wav -c 1 "+sessionFile+".wav"
            os.system(command_line)
        else:
            command_line = "cp "+sessionFile+".wav "+sessionFile+"_mono.wav"
            os.system(command_line)
        os.system("flac "+sessionFile+"_mono.wav -f "+sessionFile+".flac")
        os.system("rm session*.wav")

