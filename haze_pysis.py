#===============================================================================
#
# Programmer: Kevin Kelly
# NASA Jet Propulsion Laboratory - Juno Mission
# Planetary & Atmospheric Science - Group 3222
# Date: 02/01/2022
# Description: This program is a modularized group of functions designed to
# access SPICE & ISIS3 spacecraft data for JunoCam images using the Pysis wrapper.
#
# NB: This program has multiple dependencies:
#       -ISIS3 must be installed on your machine.
#       -The Python library "Pandas" must be installed to use Pysis, otherwise will throw "ModuleNotFoundError"
#
#
#===============================================================================
from pysis.isis import junocam2isis, spiceinit, campt
from pysis.util import file_variations

# Here we will call the image name from the original JunoCamImageProcessing.py file

# Test IMG & Framelet from PJ14
img_name = 'JNCR_2018197_14C00024_V01'
framelet = 'JNCR_2018197_14C00024_V01_BLUE_0008.cub'
framelet_csv = 'JNCR_2018197_14C00024_V01_BLUE_0008_campt.csv'
haze_points = 'haze_points.csv'


# First
#===============================================================================
#
#   Use the .LBL data label of the .IMG file to decompact each framelet
#   for red, green, and blue filters, outputting files in cube format.
#   From the command line, this was done with:
#   $ junocam2isis from=NAME_OF_IMAGE.LBL to=NAME_OF_IMAGE.cub
#
#===============================================================================

def junocam_framelets(img_name):

    (cub_name, label_name) = file_variations(img_name, ['.cub', '.LBL'])

    junocam2isis(from_=label_name, to=cub_name)
    print("Checkpoint 1: Inside Function 1")


junocam_framelets(img_name)
print("Checkpoint 2: Outside Function 1")



# Second
#===============================================================================
#
#   Get SPICE information for all 3 bands of the 15th framelet on image 23.
#   From the command line, this is achieved with the following:
#   $ spiceinit from=JNCR_2021052_32C00023_V01_BLUE_0015.cub
#   $ spiceinit from=JNCR_2021052_32C00023_V01_RED_0015.cub
#   $ spiceinit from=JNCR_2021052_32C00023_V01_GREEN_0015.cub
#
#   To process multiple images in tandem, use ISIS3's "parallel" program:
#   $ parallel spiceinit from=YOUR_IMAGE_{1}_{2}.cub ::: {RED,GREEN,BLUE} ::: {0001..0032}
#
#===============================================================================

def spice_data(framelet):

    spiceinit(from_=framelet)
    print("Checkpoint 3: Inside Function 2")


spice_data(framelet)
print("Checkpoint 4: Outside Function 2")



# Third
#===============================================================================
#
#   Run the campt program in ISIS to get the spacecraft's ancillary data for
#   latitude, longitude, and slant distance, for every pixel along the polyline
#
#===============================================================================

def isis_processing(framelet, framelet_csv, haze_points):

#    (cub_name, csv_name) = file_variations(framelet, ['.cub', '.csv'])
    campt(from_=framelet, to=framelet_csv, coordtype='Image', coordlist=haze_points, format='flat')
    print("Checkpoint5: Inside Function 3")




isis_processing(framelet, framelet_csv, haze_points)
print("Checkpoint6: Outside Function 3")
