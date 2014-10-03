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
        time = data[0]
        characterTuples = data [1:]
        print (characterTuples)
         
        for charTup in characterTuples:
            if hypo == charTup[0]:
            	like = charTup[1] * time/10
                return like
            else:
                like=0.5*time/10
        return like
   


def main():
    hypos = numpy.linspace(0, 6, 7)
    suite = Crime(hypos)

    #thinkplot.Hist(suite, label='prior')

    data = 1, (6,0.8)
    suite.Update(data)

    data = 2, (6,0.8)
    suite.Update(data)

    data = 3, (1,0.8)
    suite.Update(data)

    data = 4, (2,0.8)
    suite.Update(data)

    data = 5, (2,0.8)
    suite.Update(data)

    data = 6, (2,0.9)
    suite.Update(data)

    data = 7, (0,0.8), (1,0.8)
    suite.Update(data)

    data = 8, (0,0.4)
    suite.Update(data)

    data = 9, (1,0.8), (2, 0.8)
    suite.Update(data)
    """
    data = 10, (2,0.8)
    suite.Update(data)

    data = 11, (2,0.8)
    suite.Update(data)

    data = 12, (2,0.1)
    suite.Update(data)    

    data = 13, (0,0.8), (1,0.8), (2,0.1)
    suite.Update(data)

    data = 14, (1,0.8)
    suite.Update(data)

    data = 15, (0,0.9)
    suite.Update(data)

    data = 16, (0,0.8)
    suite.Update(data)"""



    thinkplot.Hist(suite, label='posterior')
    thinkplot.Show()

    for hypo, prob in suite.Items():
    	print (hypo,prob)

if __name__ == '__main__':
    main()
