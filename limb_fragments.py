"""
Created: Feb 12, 2024
Author: Kevin Kelly, MFA
Program Description: Mark the "endpoints" of Jupiter's limb fragments with a blue dot. 
"""

from JunoCamImageProcessing import create_raw_image, divide_image, trace_limb_polyline
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


# Load the PDS .IMG file
filename = './images/test2.IMG' # change this to whichever .IMG file you're processing
raw_image = create_raw_image(filename) # create raw image
framelets = divide_image(raw_image) # divide the raw image into its individual framelets
framelet = framelets[17] # change this index to whichever framelet you're trying to process
framelet_pixels = framelet.load()

# Create an index of "endpoints" for each limb fragment along the polyline
limb_fragments = trace_limb_polyline(framelet, raw_image)

# Load the PNG image
image_path = './images/test1.PNG' # change this to whichever .PNG file you're processing (it should match the .IMG file above)
img = Image.open(image_path)

# Create a figure and axis
fig, ax = plt.subplots()

# Display the PNG image on the axis
ax.imshow(img)

# Add a blue dot to every limb fragment's (x,y) coordinates
dot_radius = 0.5
for x, y in limb_fragments:
    blue_dot = patches.Circle((x,y), dot_radius, color='blue')
    ax.add_patch(blue_dot)
    
# Save or show the modified image
output_path = './images/limb_fragments.png'
plt.savefig(output_path, bbox_inches='tight', pad_inches=0, transparent=True)
plt.show()
