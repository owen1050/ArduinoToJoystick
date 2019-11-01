import serial
import time
import pyvjoy
import math
import sys
ser = serial.Serial('COM16', 250000, timeout=0)
j = pyvjoy.VJoyDevice(1)
while 1:
	

	try:
		if ser.inWaiting()>60:
			a = str(ser.readline())			
			
			i0 = a.find("A0:")+3
			i1 = a.find("!",i0)
			roll = int(a[i0:i1])

			i0 = a.find("A1:")+3
			i1 = a.find("!",i0)
			pitch = int(a[i0:i1])

			i0 = a.find("A2:")+3
			i1 = a.find("!",i0)
			yaw = int(a[i0:i1])
			
			
			pitch = (pitch) * (32000/720.0)
			if roll < 69:
				roll = roll + (1.18*roll-6)
			else:
				roll = roll + (-.32*roll+100)

			roll = (roll) * (32000/310)
			yaw = (yaw - 380) * (32000/650)

			#j.data.wAxisXRot = int(v)
			print(yaw)
			#j.data.wAxisYRot = int(roll)
			#j.data.wAxisZRot = int(pitch)
			#print(str(roll) + " " + str(pitch))
			j.data.wAxisZ = int(yaw)
			j.data.wAxisX = int(roll)
			j.data.wAxisY = int(pitch)
			#j.data.wSlider = int(pitch)
			#j.data.wDial = int(roll)
			
			j.update()
	except: 
		print(sys.exc_info()[0])