# Programmer: Kevin Kelly
# JPL Planetary Science Group #3222
# Date: 11/04/2021
# Program: Campt Output Formatting


#=============================================================================
#
#    Description:
#    This program takes as (CURRENTLY HARD-CODED) input the name of a CSV file to
#    format SPICE data gathered from running the ISIS program campt, specifically
#    ISIS Samples (X-axis), ISIS Line (Y-axis), Planetocentric Latitude,Positive
#    West 360 Longitude, and the Slant Distance (in this case, slant distance
#    is the distance from JunoCam to the pixel in the frame in kilometers)
#    and match it to a corresponding X,Y coordinates of a of Jovian limb,
#    outputting all data to .csv file
#
#    This progam assumes you have run ISIS and have SPICE data ready to parse.
#
#===============================================================================

import csv # https://docs.python.org/3/library/csv.html



# ===========================================================
#
#   Create a new file and store it in a variable
#
# ===========================================================

outfile = open("DESIRED_OUTPUT_FILE_NAME.csv", 'w')


# ===========================================================
#
#    Find pixel coordinate data and write it to a new file.
#
# ===========================================================

# Go into campt's .csv output file
with open("NAME_OF_YOUR_CAMPT_OUTPUT_FILE.csv", 'r') as csv_file:

    reader = csv.reader(csv_file, delimiter=',')

    header = next(reader) # Make a list of all the column titles

    # Create the "header" row of our new file:
    headers = "{},{},{},{},{}\n".format("X Axis", "Y Axis", header[6], header[10], header[22])

    # Write column headers to first row in the file
    outfile.write(headers)

    # Loop through campt output to find required data
    for column in reader:

        # Samples (X-axis)
        x_coordinate = column[1]

        # Lines (Y-axis)
        y_coordinate = column[2]

        # PlanetocentricLatitude
        lat = column[6]

        # PositiveWest360Longitude
        long = column[10]

        # SlantDistance (distance from JunoCam to pixel)
        slantdistance = column[22]

        # Assign each variable to a column in the row
        line = "{},{},{},{},{}\n".format(x_coordinate, y_coordinate, lat, long, slantdistance)

        # Write everything to the new file
        outfile.write(line)


# When we're all done and ready to terminate the program:
outfile.close()
