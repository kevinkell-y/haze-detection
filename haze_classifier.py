"""
Programmer: Kevin Kelly
Organization: NASA Jet Propulsion Laboratory - Juno Mission
Department: Planetary & Atmospheric Science - Group 3222
Program Title: A Jovian Haze Classification System in Python 
Program Description: This image processing program accesses SPICE & ISIS3 spacecraft data to detect 
and measure detached haze layers in the atmosphere of Jupiter using JunoCam images and the Python. 
Legacy code inherited from SIRI programmers at CalTech & Pasadena City.
Date: July 3, 2024

This program assumes a working knowledge of ISIS (the Integrated Software for Imagers and Spectrometers) 
and the SPICE observation geometry information system from the Navigation and Ancillary Information Facility. 
To learn more, visit: https://naif.jpl.nasa.gov/naif/index.html

"""

import os
import glob
import csv
import math
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from pysis.isis import junocam2isis, spiceinit, campt, isis2std
from pysis.exceptions import ProcessError
from pysis.util import file_variations
import pandas as pd
from trace_polyline import find_starting_limb_point, find_next_limb_point

# Other necessary imports (e.g., for peak-finding, image processing, etc.)

# Define functions for each major task
def download_img_files():
    # Implement the function to download .IMG files from the Juno PDS database
    pass

def convert_img_to_cub(img_file):
    # Implement the function to break .IMG files into their RGB framelets
    (cub, label) = file_variations(img_file, ['.cub', '.LBL'])
    junocam2isis(from_=label, to=cub)

def apply_spiceinit(cub_file):
    spiceinit(from_=cub_file)

def convert_cub_to_png(cub_file):
    # Implement the function to generate .PNG version of the .cub file
    (cub_name, png_name) = file_variations(cub_file, ['.cub', '.png'])
    isis2std(from_=cub_name, to=png_name, format='png')

def trace_polyline(framelet):
    # Implement the function to find Jupiter's polyline. Note the 'find_starting_limb_point' & 'find_next_limb_point' functions are imported, trace_polyline function included here for continuity.
    limb_endpoints = []
    curr_point = find_starting_limb_point(framelet)
    limb_endpoints.append(curr_point)
    while curr_point[0] > 0 and curr_point[0] < framelet.size[0] and curr_point[1] > 0 and curr_point[1] < framelet.size[1]:
        curr_point = find_next_limb_point(framelet, curr_point, 10) 
        limb_endpoints.append(curr_point)
    return limb_endpoints

def mark_limb_fragments(draw, polyline, color=(38, 247, 253), dot_size=1):
    # Implement the function to trace the polyline and marks each limb fragment with light-blue dots
    for point in polyline:
        x, y = point
        draw.ellipse((x - dot_size, y - dot_size, x + dot_size, y + dot_size), fill=color)

def plot_perpendicular_line(ax, x0, y0, ax_value, ay_value, radius, dl, color=(255, 0, 0), dot_size=1):
    # Implement the function to plot perpendicular lines at the center of each limb fragment
    fragment_coordinates = []
    for i in np.arange(-radius, radius, dl):
        xx = x0 + ax_value * i
        yy = y0 + ay_value * i
        ax.plot(xx, yy, 'ro', markersize=dot_size)  # Place dotted lines at each loop iteration
        fragment_coordinates.append([xx, yy])
    return fragment_coordinates

def find_center(point1, point2, dl):
    # Implement the function to find the Cartesian center between any two points on a line (in this example, we use a limb fragment)
    Delta_x = point2[0] - point1[0]
    Delta_y = point2[1] - point1[1]
    x0 = point1[0] + Delta_x / 2.0
    y0 = point1[1] + Delta_y / 2.0
    Dist = math.sqrt(Delta_x * Delta_x + Delta_y * Delta_y)
    cos = Delta_x / Dist
    sin = Delta_y / Dist
    ax_value = -sin * dl
    ay_value = cos * dl
    return x0, y0, ax_value, ay_value

def process_limb_fragments(ax, limb_fragments, dl, radius, output_file):
    # Function draws perpendicular dotted lines between each limb fragment
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        for (x1, y1), (x2, y2) in zip(limb_fragments, limb_fragments[1:]):
            P, Q = [x1, y1], [x2, y2]  # Directly unpack the fragment pair

            # Find the Cartesian center and direction vector between P and Q
            x0, y0, ax_value, ay_value = find_center(P, Q, dl)

            # Plot the dotted line perpendicular to the limb
            fragment_coordinates = plot_perpendicular_line(ax, x0, y0, ax_value, ay_value, radius, dl)

            # Append the initial limb fragment point
            writer.writerow([x1, y1])

            # Append the coordinates for the perpendicular line
            for coord in fragment_coordinates:
                writer.writerow(coord)
    
def get_lat_long_slantdistance(cub_file, campt_data, limb_fragments):
    # Implement the ISIS "campt" function to retrieve SPICE data for lat/long/slantdistance on every (x,y) coordinate pairs of our limb fragments
    campt(from_=cub_file, to=campt_data, coordtype='Image', usecoordlist=True, coordlist=limb_fragments, format='flat')
          
def rectify_limb(limb):
    # Implement the function to rectify the limb for the whole limb and for each limb fragment
    pass

def plot_graph(lat_long_slant, rectified_limb):
    # Implement the function to plot the graph using actual lat/long/slantdistance data
    pass

def find_peaks(data):
    # Implement the peak-finding function
    pass

def export_to_csv(data, output_csv):
    data.to_csv(output_csv, index=False)

def visualize_data(data):
    # Implement the function to visualize all the data
    pass

def main():
    
    # Format the JunoCam .IMG to get it ready for SPICE/ISIS processing    
    filename = 'JNCR_2018197_14C00024_V01.IMG' # Change to whichever IMG you're processing
    convert_img_to_cub(filename) # Break the IMG into .cub files
    cub_file = 'JNCR_2018197_14C00024_V01_GREEN_0004.cub' # For each .cub:
    apply_spiceinit(cub_file) # Attach SPICE data
    convert_cub_to_png(cub_file) # Convert .cub to .png
    png_file = Image.open('JNCR_2018197_14C00024_V01_GREEN_0004.png')
    limb_endpoints = trace_polyline(png_file)
    
    # Load the original image with original color
    if png_file.mode != 'RGB':
        png_file = png_file.convert('RGB')
    draw = ImageDraw.Draw(png_file)
    
    # Trace the polyline with blue dots along each limb fragment
    mark_limb_fragments(draw, limb_endpoints, color=(38, 247, 253), dot_size=1)
    
    # Display the image of the framelet with the polyline traced
    fig, ax = plt.subplots(dpi=300)  # Increase DPI for higher resolution
    ax.imshow(png_file)

    # Specify the output CSV file
    limb_fragments = 'output_file.csv'
    campt_data = 'campt_data.csv'
    
    # Process limb fragments and append the data to the output file
    process_limb_fragments(ax, limb_endpoints, 0.5, 20.0, limb_fragments)
    get_lat_long_slantdistance(cub_file, campt_data, limb_fragments)
    
    plt.show()
    
    print("Checkpoint.")     

if __name__ == "__main__":
    main()
