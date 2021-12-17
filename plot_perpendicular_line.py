#===============================================================================
#
#  The program plots a dotted line perpendicular between two points.
#
#
#===============================================================================

# Importing packages
import math
import numpy
import matplotlib.pyplot as plt

# Define x and y values (i.e, points along the polyline: (Px, Py), (Qx, Qy))
x = [7, 42]
y = [8, 44]

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
ay = cos * dl


# Plot a simple line between our two starting coordinates (7, 8) and (42, 44)
plt.plot(x, y, linewidth=1, color='black')


#======================================================================
#
# Plot the line perpendicular to the limb
#
#======================================================================

# Create 2D Array to store (x,y) pixel coordinates of the perpendicular line
perpendicular_line_coordinates = []


# NB: Python range() function cannot increment using floating point numbers
# We must instead use numpy's arange() function to increment by floats
for i in numpy.arange(-radius, radius, dl):
    x = x0 + ax * i
    y = y0 + ay * i

    perpendicular_line_coordinates.append([x, y])
#   write_function_to_do_next_step(x, y)
    plt.plot(x, y, 'ro') # Place dotted lines at each loop iteration


#  Checkpoint:
#  Display (x,y) coordinates of the perpendicular line
#  print(perpendicular_line_coordinates)


plt.show()
