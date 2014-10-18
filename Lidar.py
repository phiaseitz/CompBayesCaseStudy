from __future__ import print_function, division
import numpy
import thinkbayes2
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from itertools import product

#Defining variables up here so that we make our lives easier
maxAngle = 80
minRange = 20
maxRange = 150
numPoints = 50

class Lidar(thinkbayes2.Suite):
    """Represents hypotheses about the location of objects (sensor is at 0,0)."""
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
        #Calculate the likelihood that if we were at distance =hypo that we would get a reading = data
        error = data - hypo
        #Mean and STD calculated based on distance 
        mean = 0.0054*hypo**2 - 0.4089*hypo + 6.8076
        std = 0.1211*hypo - 3.2346

        #The error is normally distributed
        like = thinkbayes2.EvalNormalPdf(error, mean, std)
        if math.isnan(like):
            like = 5e-50

        #print (hypo, data,like)
        return like

def UpdateSuites(suites, data):
    #We take in an array of all the angle,reading pairs and our suites
    #for each of the measurements we look at the angle and update the appropriate suite
    for measurement in data:
        r = measurement[0]
        theta = measurement[1]
        suite = suites[theta]
        suite.Update(r)


def plotPolar(suites):
    #Create arrays of r, theta, and theta converted to radians
    rsarray = np.linspace(minRange,maxRange,numPoints)
    thetasarray = np.arange(0,maxAngle)
    thetasradarray = np.radians(thetasarray)

    #Meshgrid for thinkplot
    rs,thetasrads = np.meshgrid(thetasradarray, rsarray)
    likes = np.zeros((rsarray.size,thetasarray.size))
    
    #Find the likelihood of a given r,theta pair so that we can color the contour plot appropriately
    for theta in thetasarray:
        currentSuite = suites[theta]
        for indexr,r in enumerate(rsarray):
            
            likes[indexr][theta] = currentSuite.Prob(r)
   

    #Plotting things
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.contourf(rs,thetasrads, likes)

    plt.show()

def getSweepData(angleRange):
    #For Linux (I think)
    #ser=serial.Serial('/dev/ttyACM0', 9600) #Defines the serial port to use 
    #For Mac
    ser=serial.Serial('/dev/tty.usbmodem1411', 9600) #Defines the serial port to use 
    time.sleep(1)

    #Sets the servo over to its home position on the right
    ser.write('4') 
    #Waits half a second to ensure the arduino is ready for next command
    time.sleep(0.5) 
    #Create a lits of readings
    readings = []
    #Our range of angles to run through
    Angle=range(0, angleRange) 

    for eachHorizontalAngle in Angle:
        #print ('getting reading')
        #Tells the arduino to send back a distance reading
        ser.write('5') 
        time.sleep(0.3)
        try:
            #Receives the distance reading from the arduino
            distance_response=ser.readline() 
            #Removes the last 2 characters ("\r\n") from the arduino output
            cleanReading=distance_response[2:-2] 
            #Calculate distance from arduino reading
            distance = arduinoOutputToDistance(int(cleanReading))
            #print (eachHorizontalAngle)
            #If we're given NaN - set the distance to the maximum distance we can meausre at
            #This is not the world's best fix
            if math.isnan(distance):
                distance = maxRange
            #Add each reading to our list of readings
            readings.append((distance, eachHorizontalAngle))
        except Exception, e:
            print ('did not work' +  str(eachHorizontalAngle))
            readings.append((maxRange, eachHorizontalAngle))
        else:
            pass
        finally:
            pass
        
        
        
        #print('Moving left')
        #Moves the servo one degree to the left after taking a reading
        ser.write('2') 
        time.sleep(0.3)
    #reset servo
    ser.write('4') 
    return readings
   
 
def arduinoOutputToDistance(output):
    #calculate distance based on arduino output
    outputVoltage = output*5.0/1023
    distance = 32.336*outputVoltage**(-0.845)
    return distance

def main():
    #All the rs
    rs = np.linspace(minRange,maxRange,numPoints)
    #all the thetas
    thetas = np.arange(0,maxAngle)
    #A list of what will be all our suites
    suites = []

    #Create one squite per theta and add it to our list of suites
    for theta in thetas:
        suites.append(Lidar(rs))

    #How many times do we want to collect data and update
    numRuns = 5
    #Collect data and update that many times
    for run in range(numRuns):
        data = getSweepData(maxAngle)
        UpdateSuites(suites, data)
        #Plot the state of our hypotheses after each update
        plotPolar(suites)

    


if __name__ == '__main__':
    main()
