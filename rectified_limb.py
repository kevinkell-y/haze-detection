"""
Created: Feb 12, 2024
Author: Kevin Kelly, MFA
Program Description: Rectifies the Jovian limb along Jupiter's polyline
                     Exports .PNG files of the entire limb and individual limb fragments   
"""
import os
from JunoCamImageProcessing import create_raw_image, divide_image, trace_limb_polyline, rectify_limb


# Load the PDS .IMG file
filename = 'JNCR_2018197_14C00024_V01.IMG'  # change this to whichever .IMG file you're processing
raw_image = create_raw_image(filename)  # create raw image
framelets = divide_image(raw_image)  # divide the raw image into its individual framelets
framelet = framelets[4]  # change this index to whichever framelet you're trying to process
framelet_pixels = framelet.load()

# Create an index of "endpoints" for each limb fragment along the polyline
limb_fragments = trace_limb_polyline(framelet, raw_image)

x_step = 20 # number of steps taken in the x-direction to rectify the limb
y_step = 80 # number of steps taken in the y-direction to rectify the limb
width = x_step * len(limb_fragments) # width of rectified limb image
height = y_step # height of rectified limb image

# Output directory for rectified limb images
output_dir = 'rectified_limbs'
os.makedirs(output_dir, exist_ok=True)

#====================================================================
#    
#   Rectify the whole limb:
#
#=====================================================================
rect_limb, rect_limb_exact, _ = rectify_limb(framelet, limb_fragments, x_step, y_step, width, height)

# Extract the base name of the file without the .IMG extension
base_filename = os.path.splitext(os.path.basename(filename))[0]

rect_limb.save(os.path.join(output_dir, f'rectified_limb_{base_filename}.png'))

#====================================================================
#    
#   Loop through each pair of limb fragments, rectify individually
#
#=====================================================================
for fragment_index, ((x1, y1), (x2, y2)) in enumerate(zip(limb_fragments, limb_fragments[1:]), start=1):
    # Obtain the rectified limb image, rectified limb pixel value arrays (with exact values), and the
    # boundary points of each rectangle of the polyline segment
    rect_limb, rect_limb_exact, boundary_points = rectify_limb(framelet, [[x1, y1], [x2,y2]], x_step, y_step, width, height)

    # Save the rectified limb as a PNG file
    rect_limb.save(os.path.join(output_dir, f'rectified_limb_{base_filename}_fragment{fragment_index}.png'))