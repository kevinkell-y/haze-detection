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
from pysis.isis import junocam2isis, spiceinit
from pysis.util import file_variations

# Here we will call the image name from the original JunoCamImageProcessing.py file

# Test IMG from PJ14
img_name = 'JNCR_2018197_14C00024_V01'




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
    spiceinit(from_=cub_name)


junocam_framelets(img_name)

# Second
#===============================================================================
#
#   Get SPICE information for all 3 bands of the 15th framelet on image 23.
#   From the command line, this is achieved with the following:
#   $ spiceinit from=JNCR_2021052_32C00023_V01_BLUE_0015.cub
#   $ spiceinit from=JNCR_2021052_32C00023_V01_RED_0015.cub
#   $ spiceinit from=JNCR_2021052_32C00023_V01_GREEN_0015.cub
#
#   If you want to process multiple images in tandem, use parallel:
#   $ parallel spiceinit from=YOUR_IMAGE_{1}_{2}.cub ::: {RED,GREEN,BLUE} ::: {0001..0032}
#
#===============================================================================



#     9. Run the campt program in ISIS to get SlantDistance, PlanetocentricLatitude, PositiveWestLongitude
# 	Ex:
# 	campt from=image.cub coordlist=coords.csv format=flat to=output_table.csv
#
# NB: You must manually edit the haze_point.csv file exported from Daniel Wen’s code. You must delete the the first row (because it contains text) and you must delete the middle “buffer” column between the two columns (there can be no empty columns between each column) Once edited, proceed:
#
# campt from=JNCR_2021052_32C00023_V01_RED_0015.cub  coordtype=Image coordlist=haze_points.csv format=flat to=JNCR_2021052_32C00023_V01_RED_15_campt.csv
