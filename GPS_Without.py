"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

import numpy
import thinkbayes2
import thinkplot

from itertools import product


class Gps(thinkbayes2.Suite, thinkbayes2.Joint):
    """Represents hypotheses about your location in the field."""
    def __init__(self, hypos):
        self.mean = 0
        self.std = 0
        """Initialize self.

        hypos: sequence of string bowl IDs
        """
        thinkbayes2.Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: x,y coordinates
        data: gps coordinates
        """
        actualx, actualy = hypo
        measuredx, measuredy = data
        errorx = measuredx - actualx
        errory = measuredy - actualy
        mean = 0
        std = 30

        likex = thinkbayes2.EvalNormalPdf(errorx, mean, std)
        likey = thinkbayes2.EvalNormalPdf(errory, mean, std)
        # TODO: fill this in
        return likex * likey


def main():
    coords = numpy.linspace(-100, 100, 101)
    joint = Gps(product(coords, coords))

    joint.Update((51, -15))

    thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    thinkplot.Show(xlabel='X', ylabel='Y')

    joint.Update((48, 90))
    pairs = [(11.903060613102866, 19.79168669735705),
             (77.10743601503178, 39.87062906535289),
             (80.16596823095534, -12.797927542984425),
             (67.38157493119053, 83.52841028148538),
             (89.43965206875271, 20.52141889230797),
             (58.794021026248245, 30.23054016065644),
             (2.5844401241265302, 51.012041625783766),
             (45.58108994142448, 3.5718287379754585)]

    joint.UpdateSet(pairs)

    thinkplot.Contour(joint.GetDict(), contour=False, pcolor=True)
    thinkplot.Show(xlabel='X', ylabel='Y')

    # TODO: plot the marginals and print the posterior means


if __name__ == '__main__':
    main()
