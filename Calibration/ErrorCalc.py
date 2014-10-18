from __future__ import print_function, division
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from itertools import product


def getSweepData(realDist,numReadings):
    #For Linux (I think)
    #ser=serial.Serial('/dev/ttyACM0', 9600) #Defines the serial port to use 
    #For Mac
    ser=serial.Serial('/dev/tty.usbmodem1411', 9600) #Defines the serial port to use 
    time.sleep(1)
    #Sets the servo over to its home position on the right
    ser.write('4') 
    #Waits half a second to ensure the arduino is ready for next command
    time.sleep(0.5) 
    #Set up a list for the readings
    errors = []
    #Get a reading as many times as we want to 
    for eachReading in range(numReadings):
        #Tells the arduino to send back a distance reading
        ser.write('5') 
        #Wait to make sure that the arduino is ready
        time.sleep(0.3)
        try:
            #Receives the distance reading from the arduino
            distance_response=ser.readline() 
            #Removes the last 2 characters ("\r\n") from the arduino output
            cleanReading=distance_response[1:-2] 
            #Calculate the distance based on the reading
            distance = arduinoOutputToDistance(int(cleanReading)) 
            #Calculate error of measured distance from the known distance
            err = distance - realDist 
            #Add the error to our list of errors
            errors.append(err)  
            #print (eachReading)          
        except Exception, e:
            print ('did not work' +  str(eachReading))
        else:
            pass
        finally:
            pass
    return errors  

 
def arduinoOutputToDistance(output):
    #Find the distance based on the output of the arudino (a number 0-1023)
    outputVoltage = output*5.0/1023
    distance = 61.173*outputVoltage**(-1.159)
    return distance

def main():
    #Get readings from the arduino
    err = getSweepData(120,90)
    #print (err)
    mean = np.mean(err)
    print (mean)
    std = np.std(err)
    print (std)
    
if __name__ == '__main__':
    main()
