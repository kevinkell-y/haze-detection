#==============================================================
#
# Plot the Grayscale of Pixel Coordinates of a JunoCam Framelet
#
#==============================================================
import os
from PIL import Image
import matplotlib.pyplot as plt
import pdr

# This is the URL for the data file on the PDS server
image_url = 'https://pds-imaging.jpl.nasa.gov/data/juno/JNOJNC_0012/DATA/RDR/JUPITER/ORBIT_14/JNCR_2018197_14C00024_V02.IMG'
filename = image_url.split('/')[-1]

# Load the IMG into a numpy array
# juno_data = pdr.read(filename)
# print(f'The keys are {juno_data.keys()}')


raw_image = create_raw_image(filename) # create raw image
framelets = divide_image(raw_image) # divide the raw image into its indivudal framelets
framelet = framelets[4] # change this index to whichever framelet to process
framelet_pixels = framelet.load()





# creates the raw images from the .IMG files from NASA PDS
def create_raw_image(filename):
    raw_label = []
    with open(filename, 'rb') as inf:
        while True:
            line = inf.readline()
            raw_label += line
            if line.strip() == b'END' or line == b'':
                break
    pixels = []
    max_pixel_val = 0
    for i in range(1, len(raw_label), 2):
        val = 256 * raw_label[i - 1] + raw_label[i]
        # val = val * 256 / 2880.0
        if val > max_pixel_val:
            max_pixel_val = val
        pixels.append(val)

    for i in range(len(pixels)):
        pixels[i] = pixels[i] * 256 / (max_pixel_val + 1)
    width = 1648
    height = int(len(pixels) / width)
    raw_framelet = Image.new("RGB", (width, height))
    raw_framelet_pixels = raw_framelet.load()
    for i in range(len(pixels)):
        raw_framelet_pixels[i % width, int(i / width)] = (int(pixels[i]), int(pixels[i]), int(pixels[i]))
    return raw_framelet

# Create Framelets (technically: rows on the image)
def divide_image(image):
    width, height = image.size
    length = int(height/128)
    image_list = []
    ref_pixels = image.load()
    for i in range(length):
        img = Image.new("RGB", (width, 128))
        pixels = img.load()
        for w in range(width):
            for h in range(128):
                val = ref_pixels[w, i * 128 + h]
                pixels[w, h] = val
        image_list.append(img)
    return image_list




print(framelet_pixels)
print("Checkpoint")
