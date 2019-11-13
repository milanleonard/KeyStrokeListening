import pyaudio
import wave
import os
import time
from pynput.keyboard import Key, Listener
import logging
import multiprocessing
import argparse

def keypress(Key):
	logging.info(str(Key))

def keylogger(num_seconds):
	log_directory = ""
	logging.basicConfig(filename ="./data/log_results.txt",level = logging.DEBUG, format = '%(asctime)s : %(message)s')
	listener = Listener(
    on_press=keypress)
	return listener

def begin_audio(num_seconds, CHUNK=1024,CHANNELS=2,RATE=44100,FORMAT = pyaudio.paInt16):
	FORMAT = pyaudio.paInt16
	RECORD_SECONDS = num_seconds
	WAVE_OUTPUT_FILENAME = "data.wav"
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
def make_dirs():
	if not os.path.exists("./data"):
		os.makedirs("./data")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Log keypresses and record sound')
	parser.add_argument('--seconds',help='How many seconds',type=int,default=1)
	args = parser.parse_args()
	num_seconds = args.seconds
	make_dirs()
	begin_audio(num_seconds)
	
