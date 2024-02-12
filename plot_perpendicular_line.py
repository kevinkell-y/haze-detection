#============================================================================
#
#  Programmer: Kevin Kelly
#  NASA Jet Propulsion Laboratory - Juno Mission
#  Planetary & Atmospheric Science - Group 3222
#  Date: 05/27/2022
#  Version: 2.0
#  This program plots a dotted line perpendicular between two points.
#
#============================================================================

# Importing packages
import math
import numpy
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as mpimg

# Import our framelet & make it a grayscale
#============================================================================
#    -This program assumes the JunoCamImageProcessing.py file has already run.
#       In so doing, you should have an image of a framelet with a bright green
#	line running along the polyline of Jupiter. If you do not have that image,
#	stop what you're doing and run that program first and save the image
#	to the directory in which this program runs.
#============================================================================
img = mpimg.imread('framelet_4_green_polyline.png')
imgplot = plt.imshow(img, cmap='gray')

# Define x and y values (i.e, points along the polyline: (Px, Py), (Qx, Qy))
# x = [7, 42]
# y = [8, 44]

# Pick two points along the polyline:
x = [1446, 1396]
y = [59, 90]

P = [x[0], y[0]]
Q = [x[1], y[1]]

# Create your search step length for each loop iteration
dl = 0.5;

# Create radius of the line over which to loop
radius = 20.0;


#======================================================================
#
#  Computational Geometry:
#  Algorithm to find the Cartesian center between two points on a line
#
#======================================================================
Delta_x = x[1] - x[0]
Delta_y = y[1] - y[0]
x0 = x[0] + Delta_x / 2.0
y0 = y[0] + Delta_y / 2.0
Dist = math.sqrt(Delta_x * Delta_x + Delta_y * Delta_y)

cos = Delta_x / Dist
sin = Delta_y / Dist

ax = -sin * dl

# standard
ay = cos * dl

# Plot a simple line between our two starting points P and Q, first argument is list of x-coordinates x = [P[0], Q[0]], second argument is list of y-coordinates y = [P[1], Q[1]]
plt.plot(x, y, linewidth=1, color='blue')


#======================================================================
#
# Plot the line perpendicular to the limb
#
#======================================================================

# Create 2D Array to store (x,y) pixel coordinates of the perpendicular line
perpendicular_line_coordinates = []
perpendicular_line_coordinates.append(P)
perpendicular_line_coordinates.append(Q)


# NB: Python range() function cannot increment using floating point numbers
# We must instead use numpy's arange() function to increment by floats
for i in numpy.arange(-radius, radius, dl):
    xx = x0 + ax * i
    yy = y0 + ay * i

    perpendicular_line_coordinates.append([xx, yy])
#   write_function_to_do_next_step(xx, yy)
    plt.plot(xx, yy, 'ro') # Place dotted lines at each loop iteration


#  Checkpoint:
#  Display (x,y) coordinates of the perpendicular line
#  print(perpendicular_line_coordinates)


# Create a new file on which to write our haze-boundary coordinates
with open("new_coords.csv", "a") as new_csv:
    for row in perpendicular_line_coordinates:
            out = csv.writer(new_csv, delimiter=',')
            output = (row[0], row[1])
            out.writerow(output)

plt.show()
