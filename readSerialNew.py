import time
import serial
import pyvjoy
import math
import sys
import numpy as np
yaws = np.zeros(15)
yc = 0;
rolls = np.zeros(10)
rc = 0;
pitchs = np.zeros(10)
pc = 0;

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
                    #print("data:\t"+str(pitch) + ":\t"+str(yaw)+":\t"+str(roll))
                    y0 = 1797 
                    y1 = 281* math.pow(yaw,1)
                    y2 = -2.51* math.pow(yaw,2)
                    y3 = 9.93 * math.pow(10,-3) * math.pow(yaw,3)
                    y4 = -1.91 * math.pow(10,-5)* math.pow(yaw,4)
                    y5 = 1.76 * math.pow(10,-8)* math.pow(yaw,5)
                    y6 = -6.22 * math.pow(10,-12)* math.pow(yaw,6)

                    #yaw =  (32000 - 43 * math.exp(yaw * 7.32 * 10**-3 ))/3+11000
                    yaw = yaw * 267 - 198667

                    yaws[yc] = yaw
                    yaw = round(np.average(yaws))
                    if(yc < len(yaws)-1):
                         yc = yc +1;
                    else:
                         yc = 0;

                    p0 = 11797
                    p1 = -337 * math.pow(pitch,1)
                    p2 = 3.48 * math.pow(pitch,2)
                    p3 = -1.68 * math.pow(10,-2) * math.pow(pitch,3)
                    p4 = 4.37 * math.pow(10,-5) * math.pow(pitch,4)
                    p5 = -5.54 * math.pow(10,-8) * math.pow(pitch,5)
                    p6 = 2.68 * math.pow(10,-11) * math.pow(pitch,6)

                    pitch = p0+p1+p2+p3+p4+p5+p6
                    pitch = round(pitch * 0.7)
                    pitchs[rc] = pitch
                    pitch = round(np.average(pitchs))
                    if(pc < len(pitchs)-1):
                         pc = pc +1;
                    else:
                         pc = 0;
                    r0 = -840
                    r1 = 236 *math.pow(roll, 1)
                    r2 = 2.38 * math.pow(roll, 2)
                    r3 = -4.93 * math.pow(10,-2) * math.pow(roll, 3)
                    r4 = 2.97 * math.pow(10,-4) * math.pow(roll, 4)
                    r5 = -7.64 * math.pow(10,-7) *math.pow(roll, 5)
                    r6 = 7.28 * math.pow(10,-10) * math.pow(roll, 6)
 
                    roll = round(r0+r1+r2+r3+r4+r5+r6)
                    rolls[rc] = roll
                    roll = round(np.average(rolls))
                    if(rc < len(rolls)-1):
                         rc = rc +1;
                    else:
                         rc = 0;
                    
                    #j.data.wAxisXRot = int(v)
                    
                    #j.data.wAxisYRot = int(roll)
                    #j.data.wAxisZRot = int(pitch)
                    #print(str(roll) + " " + str(pitch))
                    j.data.wAxisZ = int(yaw)
                    j.data.wAxisX = int(roll)
                    j.data.wAxisY = int(pitch)
                    #j.data.wSlider = int(pitch)
                    #j.data.wDial = int(roll)
                    #print("data:\t"+str(pitch) + ":\t"+str(yaw)+":\t"+str(roll))
                    j.update()
        except: 
                print(sys.exc_info()[0])
                if "board" in str(sys.exc_info()[0]):
                    break