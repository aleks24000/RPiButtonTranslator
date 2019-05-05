
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# VideoRecorder.py

from __future__ import print_function, division
#import numpy as np
#import cv2
import pyaudio
import wave
import threading
import time
#import subprocess
import os
from Config import AUDIO_CONFIG

class AudioRecorder():
    "Audio class based on pyAudio and Wave"
    def __init__(self, filename="temp_audio.wav", input_device_index=AUDIO_CONFIG['record_device'], rate=AUDIO_CONFIG['rate'], fpb=AUDIO_CONFIG['chunk'], channels=1):
        self.open = True
        self.rate = rate
        self.input_device_index = input_device_index
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      input_device_index=self.input_device_index,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        print("Recording")
        "Audio starts being recorded"
        self.stream.start_stream()
        while self.open:
            #data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)a
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self):
        print("Stop record")
        "Finishes the audio recording therefore the thread too"
        if self.open:
            print("stream opened")
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            print(os.getcwd())
            print(self.audio_filename)
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()
        pass

    def start(self):
        print("Start thread")
        "Launches the audio recording function using a thread"
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

def start_AVrecording(filename="test"):
#    global video_thread
    global audio_thread
#    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()
    audio_thread.start()
#    video_thread.start()
    return filename


#def start_audio_recording(filename="test"):
#    global audio_thread
#    audio_thread = AudioRecorder()
#    audio_thread.start()
#    return filename

def stop_AVrecording(filename="test"):
    audio_thread.stop()
#    frame_counts = video_thread.frame_counts
#    elapsed_time = time.time() - video_thread.start_time
#    recorded_fps = frame_counts / elapsed_time
#    print("total frames " + str(frame_counts))
#    print("elapsed time " + str(elapsed_time))
#    print("recorded fps " + str(recorded_fps))
#    video_thread.stop()

    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)

    print("After sleep")
    # Merging audio and video signal
#    if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected
#        print("Re-encoding")
#        cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.avi -pix_fmt yuv420p -r 6 temp_video2.avi"
#        subprocess.call(cmd, shell=True)
#        print("Muxing")
#        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.avi -pix_fmt yuv420p " + filename + ".avi"
#        subprocess.call(cmd, shell=True)
#    else:
#        print("Normal recording\nMuxing")
#        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + filename + ".avi"
#        subprocess.call(cmd, shell=True)
#        print("..")

#def file_manager(filename="test"):
  #  "Required and wanted processing of final files"
 #   local_path = os.getcwd()
   # print(local_path)
    #if os.path.exists(str(local_path) + "/temp_audio.wav"):
     #   os.remove(str(local_path) + "/temp_audio.wav")
    #if os.path.exists(str(local_path) + "/temp_video.avi"):
     #   os.remove(str(local_path) + "/temp_video.avi")
    #if os.path.exists(str(local_path) + "/temp_video2.avi"):
     #   os.remove(str(local_path) + "/temp_video2.avi")
    # if os.path.exists(str(local_path) + "/" + filename + ".avi"):
    #     os.remove(str(local_path) + "/" + filename + ".avi")

if __name__ == '__main__':
    start_AVrecording()
    time.sleep(5)
    stop_AVrecording()
    #file_manager()
