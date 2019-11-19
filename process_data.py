import os
import wave
import pylab
import pandas as pd
from scipy import signal
import numpy as np
import datetime
from pathlib import Path
def split_on_letters()

def graph_spectrogram(wav_file):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    spec, freqs, ts, _ = pylab.specgram(sound_info, Fs=frame_rate)
    pylab.show()
    pylab.savefig('spectrogram.png')

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.frombuffer(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def make_image_dirs(filename):
    data = pd.read_csv(filename)
    print(data)
    for var in pd.unique(data["keypress"]):
        if not os.path.exists(var):
            os.mkdir("./proc_data/"+var)


if __name__ == '__main__':
    data = Path("./raw_data")
    files = data.glob("*.csv")
    for file in files:
        make_image_dirs(file)