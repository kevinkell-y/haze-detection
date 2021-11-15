# Programmer: Kevin Kelly
# Date: 11//13/2021
# Astronomy & Physics Club Hackathon

#====================================================================
#
#   Description:
#
#   A first attempt at finding peaks in graphed data, this program
#   creates a plotted graph from input data and uses the numpy & scipy
#   libraries to find/output local maximia and minima for the dataset.
#   Based on the peak detection tutorial from the PeakUtils documentation:
#   https://peakutils.readthedocs.io/en/latest/tutorial_a.html#importing-the-libraries
#
#====================================================================

# Importing the libraries
import numpy
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot



# Preparing noisy data from two Gaussians
# Learn more about Gaussians here: https://en.wikipedia.org/wiki/Gaussian_function
centers = (30.5, 72.3)
x = numpy.linspace(0, 120, 121) # Returns evenly spaced numbers over a specified interval. https://numpy.org/doc/stable/reference/generated/numpy.linspace.html#numpy-linspace
y = (peakutils.gaussian(x, 5, centers[0], 3) +
     peakutils.gaussian(x, 7, centers[1], 10) +
     numpy.random.rand(x.size))
pyplot.figure(figsize=(10,6))
pyplot.plot(x, y)
pyplot.title("Data with noise")


# Getting a first estimate of the peaks
indexes = peakutils.indexes(y, thres=0.5, min_dist=30)
print(indexes)
print(x[indexes], y[indexes])
pyplot.figure(figsize=(10,6))
pplot(x, y, indexes)
pyplot.title('First estimate')


# Enhance the resolution by interpolation
peaks_x = peakutils.interpolate(x, y, ind=indexes)
print(peaks_x)


# Estimating and removing the baseline
y2 = y + numpy.polyval([0.002, -0.08, 5], x)
pyplot.figure(figsize=(10,6))
pyplot.plot(x, y2)
pyplot.title("Data with baseline")


# Display everything to the screen
pyplot.show()
