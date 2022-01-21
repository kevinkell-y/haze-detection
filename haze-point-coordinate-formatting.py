# Programmer: Kevin Kelly
# Program Name: Haze Point Coordinate Formatting
# Version: 1.0
# Date: January 20, 2022

# ====================================================================================
#
#   This program typecasts X/Y coordinates from strings into floating point numbers 
#   and appends them to a list called "polyline_coordinates"
# 
#   The haze_points.csv file is output after successfully compiling the JunoCamProcessing.py script. 
#   This program depends upon that specific file, but designed to be "general" enough to be helpful elsewhere.
#
# ====================================================================================

import csv


# Declare a variable to keep our list of coordinates
polyline_coordinates = []


# Open file in read mode
with open( 'haze_points.csv', 'r') as csv_file:

    # Pass the file object to the reader() method to get the reader object
    csv_reader = csv.reader(csv_file)

    # Extract the rows from the .csv file and store them in a list
    rows = []
    for row in csv_reader:
        rows.append(row)

    # Checkpoint
    # print(rows)

    # Format data from strings (the default .CSV output) to floating point numbers, skip the first row (header/labels)
    for row in rows[1:]:


        # Make sure the elements can be typecast into floats
        try:
            float(row[0].strip())
        except: 
            continue 


        # Clean up each element and make it a number
        x = float(row[0].strip())
        y = float(row[1].strip())
     
    
        polyline_coordinates.append([x, y])

    
print("==============================")
print(polyline_coordinates)