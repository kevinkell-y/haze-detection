# Programmer: Kevin Kelly
# JPL Planetary Science Group #3222
# Date: 10/14/2021
# Program: Coordlist File Formatting

# ===========================================================
#
#   Program Description: Take as input a flatfile of pixel 
#   coordinate data of ISIS "samples" (X-axis) and "lines" (Y-axis) 
#   Program then strips formatting, converts strings to floats, 
#   and outputs a new CSV file.
#
#
# ===========================================================


import csv  # https://docs.python.org/3/library/csv.html


# ===========================================================
#
#   Get a file from the user, check that it exists
#
# ===========================================================

file_name = input("Enter the file name: ")
try:
    file_handle = open(file_name, "r")
except:
    print("File cannot be opened: ", file_name)
    exit()

# Checkpoint
# print(f"Success, {file_name} is a real file.")



# ===========================================================
#
#    Find pixel coordinates and write them to a new file.
#
# ===========================================================

# Create a new file to write on
with open("coordlist.csv", "a") as new_file:

    # Go through each line in the user's original file
    for line in file_handle:

        # Get rid of the invisible newline character at the end of every line
        line = line.rstrip()

        # Split the string into a list
        line = line.split(" ")

        # Format how data will be written to new file
        writer = csv.writer( new_file, delimiter=',')


        # NB: We use [0] and [1] because ISIS outputs X/Y coordinates
        # as the first two items for every row. If that ever changes, will need to be readjusted

        # Typecast required list items from strings to floats
        output = float(line[0].strip()), float(line[1].strip())

        # Write the coordinates to a new file:
        writer.writerow(output)
