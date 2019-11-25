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
                    #print(a)
                    i0 = a.find("A0:")+3
                    i1 = a.find("!",i0)
                    roll = int(a[i0:i1])
                    rog = roll

                    i0 = a.find("A1:")+3
                    i1 = a.find("!",i0)
                    pitch = int(a[i0:i1])
                    pog = pitch

                    i0 = a.find("A2:")+3
                    i1 = a.find("!",i0)
                    yaw = int(a[i0:i1])
                    yog = yaw
                    #print("data:\t"+str(pitch) + ":\t"+str(yaw)+":\t"+str(roll))
                    
                    y0 = -545201
                    y1 = 1113* math.pow(yaw,1)
                    y2 = -0.511 * math.pow(yaw,2)
                    
                    yaw = y0+y1+y2
                    yaws[yc] = yaw
                    yaw = round(np.average(yaws))
                    if(yc < len(yaws)-1):
                         yc = yc +1;
                    else:
                         yc = 0;

                    p0 = 1598
                    p1 = -161 * math.pow(pitch,1)
                    p2 = 2.36 * math.pow(pitch,2)
                    p3 = -0.0137  * math.pow(pitch,3)
                    p4 = 4.03 * math.pow(10,-5) * math.pow(pitch,4)
                    p5 = -5.56 * math.pow(10,-8) * math.pow(pitch,5)
                    p6 = 2.86 * math.pow(10,-11) * math.pow(pitch,6)

                    pitch = round(p0+p1+p2+p3+p4+p5+p6)
                    
                    pitchs[rc] = pitch
                    pitch = round(np.average(pitchs))
                    if(pc < len(pitchs)-1):
                         pc = pc +1;
                    else:
                         pc = 0;
                    
                    r0 = -28643
                    r1 = 39.6 * math.pow(roll,1)
                    r2 = 0.214 * math.pow(roll,2)
                    
                    roll = 32000-(r0+r1+r2)
                    rolls[rc] = roll
                    roll = round(np.average(rolls))
                    if(rc < len(rolls)-1):
                         rc = rc +1;
                    else:
                         rc = 0;
                    
                    j.data.wAxisZ = int(yaw)
                    j.data.wAxisX = int(roll)
                    j.data.wAxisY = int(pitch)
                    
                    print("data:\t"+str(round(pitch))+ ":\t"+str(pog) + ":\t"+str(yaw)+ ":\t"+str(yog)+":\t"+str(roll)+ ":\t"+str(rog))
                    j.update()
        except: 
                print(sys.exc_info()[0])
                if "board" in str(sys.exc_info()[0]):
                    break