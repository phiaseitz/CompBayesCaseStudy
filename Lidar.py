from __future__ import print_function, division
import numpy
import thinkbayes2
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from itertools import product

maxAngle = 80
minRange = 20
maxRange = 150
numPoints = 50

class Lidar(thinkbayes2.Suite):
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

        hypo: hypothetical distance
        data: measured distance.
        """

        error = data - hypo
        #Mean and STD calculated based on distance 
        mean = 0.0054*hypo**2 - 0.4089*hypo + 6.8076
        std = 0.1211*hypo - 3.2346

        like = thinkbayes2.EvalNormalPdf(error, mean, std)
        if math.isnan(like):
            like = 5e-50

        #print (hypo, data,like)
        return like

def UpdateSuites(suites, data):
    for measurement in data:
        r = measurement[0]
        theta = measurement[1]
        suite = suites[theta]
        suite.Update(r)


def plotPolar(suites):
    rsarray = np.linspace(minRange,maxRange,numPoints)
    thetasarray = np.arange(0,maxAngle)
    thetasradarray = np.radians(thetasarray)

    rs,thetasrads = np.meshgrid(thetasradarray, rsarray)
    likes = np.zeros((rsarray.size,thetasarray.size))
    # print (rsarray)
    # for theta,suite in enumerate(suites):
    #     for hypo, prob in suite.Items():
    #         likes[np.where(rsarray == hypo)][theta] = prob
    # print (likeDicts)

    for theta in thetasarray:
        currentSuite = suites[theta]
        for indexr,r in enumerate(rsarray):
            #print(currentSuite.Prob(r))
            likes[indexr][theta] = currentSuite.Prob(r)
    
    # for indextheta,theta in enumerate(thetasarray):
    #     likeDict = likeDicts[theta]
    #     print (likeDict)
    #     for indexr,r in enumerate(rsarray):
    #         print (likeDict[r])
    #         #likes[indexr][indextheta] = likeDict[r]



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

    horzAngle=range(0, angleRange) #(so we don't fight the servo) creates the horizontal range of angles that the servo should sweep through

    for eachHorizontalAngle in horzAngle:
        #print ('getting reading')
        ser.write('5') #Tells the arduino to send back a distance reading
        time.sleep(0.3)
        try:
            distance_response=ser.readline() #Receives the distance reading from the arduino
            cleanReading=distance_response[2:-2] #Removes the last 2 characters ("\r\n") from the arduino output
            #distance=float(cleanReading) #Type-casts it as an float so that it can be plotted
            #print ('clean' + str(cleanReading))
            distance = arduinoOutputToDistance(int(cleanReading))
            print (eachHorizontalAngle)
            if math.isnan(distance):
                distance = maxRange
            readings.append((distance, eachHorizontalAngle))
        except Exception, e:
            print ('did not work' +  str(eachHorizontalAngle))
            readings.append((maxRange, eachHorizontalAngle))
        else:
            pass
        finally:
            pass
        
        
        
        #print('Moving left')
        ser.write('2') #Moves the servo one degree to the left after taking a reading
        time.sleep(0.3)
    time.sleep(0.5)
    ser.write('4') #reset servo
    return readings
   
 
def arduinoOutputToDistance(output):
    outputVoltage = output*5.0/1023
    distance = 32.336*outputVoltage**(-0.845)
    return distance

def main():
    rs = np.linspace(minRange,maxRange,numPoints)
    thetas = np.arange(0,maxAngle)
    suites = []

    for theta in thetas:
        suites.append(Lidar(rs))

    numRuns = 5
    for run in range(numRuns):
        data = getSweepData(maxAngle)
    #print (data)
        UpdateSuites(suites, data)
        plotPolar(suites)

    


if __name__ == '__main__':
    main()
