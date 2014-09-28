from __future__ import print_function, division

import numpy
import thinkbayes2
import thinkplot


class Crime(thinkbayes2.Suite):
    """Represents hypotheses about the state of the electorate."""

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: that a certain character commited the crime
        data: time, characters implicated, how strongly
        """
        #Assuming that for this case, the hypothesis is correct
        time, character, howstrong = data
        
        if hypo == character:
        	like = 1
        else:
        	like = 0.1
        return like
   


def main():
    hypos = numpy.linspace(0, 10, 11)
    suite = Crime(hypos)

    #thinkplot.Hist(suite, label='prior')

    data = 1, 3, 5
    suite.Update(data)
    data = 1, 10, 4
    suite.Update(data)

    thinkplot.Hist(suite, label='posterior')
    thinkplot.Show()

    for hypo, prob in suite.Items():
    	print (hypo,prob)

if __name__ == '__main__':
    main()
