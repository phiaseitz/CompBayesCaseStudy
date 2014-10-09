import math
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


def calcRealDist(theta, length, width, up, right):
	radTheta = math.radians(theta)
	down = width - up
	left = length - right
	dist = 0
	if theta == 0:
		dist = up
	elif theta == 90:
		dist = left
	elif theta == 180:
		dist = down
	elif theta == 270:
		dist = right
	elif theta < 90:
		#check walls 1 and 2
		w1 = up/math.fabs(math.cos(radTheta))
		w2 = left/math.fabs(math.cos(math.pi/2-radTheta))
		if w1 < w2:
			dist = w1
		else:
			dist = w2
	elif theta < 180:
		#check walls 2 and 3
		w2 = left/math.fabs(math.cos(radTheta - math.pi/2))
		w3 = down/math.fabs(math.cos(math.pi-radTheta))
		if w2 < w3:
			dist = w2
		else:
			dist = w3
	elif theta < 270:
		#check walls 3 and 4
		w3 = down/math.fabs(math.cos(radTheta-math.pi))
		w4 = right/math.fabs(math.cos(3*math.pi/2-radTheta))
		if w3 < w4:
			dist = w3
		else:
			dist = w4
	else:
		#check walls 4 and 1
		w4 = right/math.fabs(math.cos(-radTheta))
		w1 = up/math.fabs(math.cos(radTheta-3*math.pi/2))
		if w4 < w1:
			dist = w4
		else:
			dist = w1

	return dist

def main():
	thetas = np.zeros((361,))
	dists = np.zeros((361,))
	length = 100
	width = 100
	up = 50
	right = 50

	for theta in range(361):
		dists[theta] = calcRealDist(theta,length, width, up, right)
		thetas[theta] = math.radians(theta)
		print dists[theta]

	ax = subplot(111, polar=True)
	c = scatter(thetas, dists, s=2)
	c.set_alpha(0.75)

	show()



if __name__ == '__main__':
    main()