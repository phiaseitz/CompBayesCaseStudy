"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

import numpy
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from itertools import product


def getSweepData(realDist,numdata):
    #For Linux (I think)
    #ser=serial.Serial('/dev/ttyACM0', 9600) #Defines the serial port to use 
    #For Mac
    ser=serial.Serial('/dev/tty.usbmodem1411', 9600) #Defines the serial port to use 
    time.sleep(1)

    ser.write('4') #Sets the servo over to its home position on the right
    time.sleep(0.5) #Waits half a second to ensure the arduino is ready for next command
    readings = []

    horzAngle=range(0, angleRange+1) #creates the horizontal range of angles that the servo should sweep through

    for eachHorizontalAngle in horzAngle:
        #print ('getting reading')
        ser.write('5') #Tells the arduino to send back a distance reading
        time.sleep(0.3)
        try:
            distance_response=ser.readline() #Receives the distance reading from the arduino
            cleanReading=distance_response[1:-2] #Removes the last 2 characters ("\r\n") from the arduino output
            #distance=float(cleanReading) #Type-casts it as an float so that it can be plotted
            print (cleanReading)
            distance = arduinoOutputToDistance(int(cleanReading))
            print (distance)
            err = distance - realDist
            readings.append(err)  
            print (eachHorizontalAngle)          
        except Exception, e:
            print ('did not work' +  str(eachHorizontalAngle))
        else:
            pass
        finally:
            pass
    return readings

 
def arduinoOutputToDistance(output):
    outputVoltage = output*5.0/1023
    distance = 61.173*outputVoltage**(-1.159)
    return distance

def main():
    err = getSweepData(120,90)
    print (err)
    mean = np.mean(err)
    print (mean)
    std = np.std(err)
    print (std)
    # rs = np.linspace(20,150,50)
    # thetas = np.arange(0,90)
    # joint = Lidar(product(rs, thetas))

    



    # data = ((15, 10),(16,10))

    # joint.Update(data)
    
    # # thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    # # thinkplot.Show(xlabel='X', ylabel='Y')

    # data = ((15,12),(16,12))

    # joint.Update(data)


    # plotPolar(joint)

    # # thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    # # thinkplot.Show(xlabel='X', ylabel='Y')

    # # TODO: plot the marginals and print the posterior means


if __name__ == '__main__':
    main()
