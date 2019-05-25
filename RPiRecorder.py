from gpiozero import Button
from signal import pause
import os
import shlex
import subprocess
from Config import AUDIO_CONFIG

proc = None

def upload():
    file_metadata = {'name': 'photo.jpg'}
    media = MediaFileUpload('files/photo.jpg',
                        mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print ("File ID: " + file.get('id'))

def start_rec():
    print("Start!")
    command_line = "arecord --device=hw:" + str(AUDIO_CONFIG['record_device']) + ",0 --format S16_LE --rate " + str(AUDIO_CONFIG['rate']) + " -c" + str(AUDIO_CONFIG['channel']) + " temp_audio.wav &"
    args = shlex.split(command_line)
    global proc
    proc = subprocess.Popen(args)
    print("PID:" + str(proc.pid))

def stop_rec():
    print("Stop!")
    global proc
    command_line = "kill " + str(proc.pid)
    os.system(command_line)
    if AUDIO_CONFIG['channel'] == 2:
        command_line = "sox temp_audio.wav -c 1 temp_audio_mono.wav"
        os.system(command_line)
    else:
        command_line = "cp temp_audio.wav temp_audio_mono.wav"
        os.system(command_line)
    upload

button = Button(12)
button_stop = Button(20)

button.when_pressed = start_rec
button_stop.when_pressed = stop_rec

pause()
