"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

import numpy
import thinkbayes2
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from itertools import product


class Lidar(thinkbayes2.Suite, thinkbayes2.Joint):
    """Represents hypotheses about the location of objects sensor is at 0,0."""
    def __init__(self, hypos):
        self.mean = 0
        self.std = 0
        """Initialize self.

        """
        thinkbayes2.Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: r,theta coordinates where there might be an object
        (r is in cm)
        data: angle, measured distance pairs.
        """
        actualr, actualtheta = hypo


        for pair in data:
            if  pair[1]== actualtheta:
                #assume that there is no error for theta
                #calculate the error in measured r for a given hypothetical r
                measureddist = pair[0]
                errorr = measureddist - actualr

                #Mean and STD calculated based on distance 
                mean = 0.0054*measureddist**2 - 0.4089*measureddist + 6.8076
                std = 0.1211*measureddist - 3.2346,

                liker = thinkbayes2.EvalNormalPdf(errorr, mean, std)
            else:
                #This shouldn't happen, the way that we're planning to pass in data
                #We'll want to make sure we have a plan for if this does happen.
                liker = 0
        #print (actualr,actualtheta,liker)
        return liker


def plotPolar(joint):

    likeDict = joint.GetDict()
 

    rsarray = np.linspace(20,150,50)
    thetasarray = np.arange(0,85)
    thetasradarray = np.radians(thetasarray)

    rs,thetasrads = np.meshgrid(thetasradarray, rsarray)
    likes = np.zeros((rsarray.size,thetasarray.size))

    for indexr,r in enumerate(rsarray):
        for indextheta,theta in enumerate(thetasarray):

            likes[indexr][indextheta] = likeDict[r,theta]
            print (r,theta,likes[indexr][indextheta])


    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.contourf(rs,thetasrads, likes)

    plt.show()

def getSweepData(angleRange):
    #For Linux (I think)
    #ser=serial.Serial('/dev/ttyACM0', 9600) #Defines the serial port to use 
    #For Mac
    ser=serial.Serial('/dev/tty.usbmodem1411', 9600) #Defines the serial port to use 
    time.sleep(1)

    ser.write('4') #Sets the servo over to its home position on the right
    time.sleep(0.5) #Waits half a second to ensure the arduino is ready for next command
    readings = []

    horzAngle=range(0, angleRange-5) #(so we don't fight the servo) creates the horizontal range of angles that the servo should sweep through

    for eachHorizontalAngle in horzAngle:
        #print ('getting reading')
        ser.write('5') #Tells the arduino to send back a distance reading
        time.sleep(0.5)
        try:
            distance_response=ser.readline() #Receives the distance reading from the arduino
            cleanReading=distance_response[2:-2] #Removes the last 2 characters ("\r\n") from the arduino output
            #distance=float(cleanReading) #Type-casts it as an float so that it can be plotted
            #print ('clean' + str(cleanReading))
            distance = arduinoOutputToDistance(int(cleanReading))
            print (eachHorizontalAngle)
            readings.append((distance, eachHorizontalAngle))
        except Exception, e:
            print ('did not work' +  str(eachHorizontalAngle))
        else:
            pass
        finally:
            pass
        
        
        
        #print('Moving left')
        ser.write('2') #Moves the servo one degree to the left after taking a reading
    time.sleep(0.5)
    ser.write('4') #reset servo
    return readings
   
 
def arduinoOutputToDistance(output):
    outputVoltage = output*5.0/1023
    distance = 32.336*outputVoltage**(-0.845)
    return distance

def main():
    rs = np.linspace(20,150,50)
    thetas = np.arange(0,85)
    joint = Lidar(product(rs, thetas))

    data = getSweepData(90)
    print (data)

    joint.Update(data)
    
    # thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    # thinkplot.Show(xlabel='X', ylabel='Y')

    joint.Update(data)

    for hypo, prob in joint.Items():
        print(hypo, prob)

    plotPolar(joint)

    # thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    # thinkplot.Show(xlabel='X', ylabel='Y')

    # TODO: plot the marginals and print the posterior means


if __name__ == '__main__':
    main()
