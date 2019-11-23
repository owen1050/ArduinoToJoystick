import pyaudio
import wave
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as sp
from scipy import signal

sos = signal.butter(5, [27,4200], btype = 'bandpass', fs=44100, output='sos')
chunk = 2205  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 1


filename = "output.wav"
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)


p = pyaudio.PyAudio()  # Create an interface to PortAudio

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True,
                input_device_index=0)
frames = [] 
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

	# Stop and close the stream 
npd = np.frombuffer(data, dtype=np.int16)
npd = signal.sosfilt(sos, npd)
dft = sp.rfft(npd)
hz = sp.fftfreq(len(npd)) * 44100
hz = hz[:int(len(dft)/2)]
line1 = ax.plot(hz,hz)

for i in range(1000):
	frames = []  # Initialize array to store frames

	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * seconds)):
	    data = stream.read(chunk)
	    frames.append(data)

	# Stop and close the stream 
	npd = np.frombuffer(data, dtype=np.int16)
	npd = signal.sosfilt(sos, npd)
	dft = sp.rfft(npd)
	
	print(int(hz[np.where(dft == np.amax(dft))]))
	line1 = ax.plot(np.abs(dft)[:int(len(dft)/2)])
	fig.canvas.draw()
	
	
	


stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

