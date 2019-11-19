from utils import *

import pyaudio
import wave
import os
import time
from pynput.keyboard import Key, Listener
import pandas as pd
import logging
import argparse
import numpy as np



def keypress(Key):
	logging.info(str(Key))

def keylogger(num_seconds):
	log_directory = ""
	logging.basicConfig(filename=tmp_dir+"log_results.txt",level=logging.DEBUG, format='%(asctime)s : %(message)s')
	listener = Listener(
    on_press=keypress)
	return listener

def record(num_seconds, CHUNK=1024,CHANNELS=2,RATE=44100,FORMAT = pyaudio.paInt16):
	""" Records audio and characters typed for num_seconds, returns the start time of recording.
	"""
	FORMAT = pyaudio.paInt16
	RECORD_SECONDS = num_seconds
	WAVE_OUTPUT_FILENAME = get_nonexistant_path(data_dir+"/sounddata.wav")
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)
	print("* recording")
	frames = []
	listener = keylogger(num_seconds)
	listener.start()
	start = time.time()
	while time.time()-start < num_seconds:
		print(time.time()-start)
		for i in range(0, int(RATE / CHUNK * num_seconds)):
		    data = stream.read(CHUNK)
		    frames.append(data)
		print("* done recording")
		listener.stop()
		stream.stop_stream()
		stream.close()
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
	return start

def txt_to_csv(txt,start):
	"""
	Turn the logging txt file into a usable CSV format
	"""
	arr = np.delete(np.loadtxt(tmp_dir+txt,dtype=str).squeeze(),2,1)
	times = convert_times(arr) - start
	output = np.vstack((times,arr[:,-1])).T
	data = pd.DataFrame(output,columns=["time","keypress"])
	fname = get_nonexistant_path(data_dir+"keystrokedata.csv")
	data["keypress"] = data["keypress"].apply(map_letters)
	data.to_csv(fname)

def map_letters(letter):
	try:
		return dictionary_mapping[letter]
	except:
		return letter.strip("'").lower()



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Log keypresses and record sound')
	parser.add_argument('--seconds',help='How many seconds',type=int,default=1)
	args = parser.parse_args()
	num_seconds = args.seconds
	

	make_dirs()
	start_time = record(num_seconds)
	txt_to_csv("log_results.txt",start_time)
	open(tmp_dir+"log_results.txt","w").close()
		
