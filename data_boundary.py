# Programmer: Kevin Kelly
# JPL Planetary Science Group #3222
# Date: June 5th, 2022
# Description: Program to find the boundary between VALID & NULL data

#===============================================================================
#
#   Overview: This program uses Pandas dataframes to read & parse ISIS3
#   campt output to find the boundary point between VALID & NULL data.
#   While this is written specifically for Jupiter's detached haze layers, it
#   should be able to be modified to parse over any other dataset.
#
#===============================================================================
import pandas as pd
import numpy as np
isis_data = pd.read_csv('coord_final.csv', index_col=0)

# Print out the first five rows, make sure your data's correct.
isis_data.head()

# Parse the campt output and add X-coordinate (Sample), Y-coordinate (Line),
# Latitude, Longitude, and Slant Distance to a csv
isis_data.loc[:, ['Sample','Line','PlanetocentricLatitude','PositiveWest360Longitude','SlantDistance']].to_csv('isis_data2.csv')

# Create a Series of data with the Latitude column
# https://pandas.pydata.org/docs/reference/api/pandas.Series.html
latitudes = isis_data["PlanetocentricLatitude"]

# Confirm its a data Series
type(latitudes)

# Run a lazy iterator to find the boundary between VALID data & NULL data
counter = -1
for latitude in latitudes:
    if np.isnan(latitude):
        break # "continue" might be better here, if NULL data at start of file?
    else:
        counter += 1

print(counter)

#==================
# VALID DATA
#==================
lat = isis_data['PlanetocentricLatitude'][counter]
long = isis_data['PositiveWest360Longitude'][counter]
slantDistance = isis_data['SlantDistance'][counter]
sample = isis_data['Sample'][counter] # x-coordinate of valid data boundary
line = isis_data['Line'][counter] # y-coordinate of valid data boundary
#==================
# NULL DATA
#==================
NULL_sample = isis_data['Sample'][counter + 1] # x-coordinate for NULL data boundary
NULL_line = isis_data['Line'][counter + 1] # y-coordinate for NULL data boundary
NULL_lat = isis_data['PlanetocentricLatitude'][counter + 1] # should be NaN


# Checkpoint
print(f"Valid Data Boundary for Detached Haze Layer:\nX: {sample}\nY: {line}\nLatitude: {lat}\nLongitude: {long}\nSlant Distance: {slantDistance}\n")
print(f"NULL Data Boundary for Detached Haze Layer:\nX: {NULL_sample}\nY: {NULL_line}\nLatitude: {NULL_lat}")
