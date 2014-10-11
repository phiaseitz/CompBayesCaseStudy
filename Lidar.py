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
        measuredr, measuredtheta = data

        for pair in data:
            if  pair[1]== actualtheta:
                #assume that there is no error for theta
                #calculate the error in measured r for a given hypothetical r
                errorr = pair[0] - actualr

                #come up with a better way of doing this.
                mean = 0
                std = 1,

                liker = thinkbayes2.EvalNormalPdf(errorr, mean, std)
            else:
                #This shouldn't happen, the way that we're planning to pass in data
                liker = 0.000001

        return liker


def plotPolar(joint):

    likeDict = joint.GetDict()
 

    rsarray = np.linspace(1,100,50)
    thetasarray = np.arange(0,361)
    thetasradarray = np.radians(thetasarray)

    rs,thetasrads = np.meshgrid(thetasradarray, rsarray)
    likes = np.zeros((rsarray.size,thetasarray.size))

    for indexr,r in enumerate(rsarray):
        for indextheta,theta in enumerate(thetasarray):

            likes[indexr][indextheta] = likeDict[r,theta]


    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.contourf(rs,thetasrads, likes)

    plt.show()


def main():
    rs = np.linspace(1,100,50)
    thetas = np.arange(0,361)
    joint = Lidar(product(rs, thetas))

    data = ((15, 10),(16,10))

    joint.Update(data)
    
    # thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    # thinkplot.Show(xlabel='X', ylabel='Y')

    data = ((15,12),(16,12))

    joint.Update(data)


    plotPolar(joint)

    # thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    # thinkplot.Show(xlabel='X', ylabel='Y')

    # TODO: plot the marginals and print the posterior means


if __name__ == '__main__':
    main()
