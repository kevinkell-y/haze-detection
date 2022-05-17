#=================================================================
#
# This function creates raw images from .IMG files from NASA PDS
# Part of the JunoCamImageProcessing.py script I worked on at NASA JPL's
# Planetary & Atmospheric Sciences Group 3222
#
#=================================================================
from PIL import Image

# Test the function with JunoCam .IMG file from Perijove 14
# filename = ('../JNCR_2018197_14C00024_V02.IMG')

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


# raw = create_raw_image(filename)
# print(raw)
## If successfully, terminal outputs:
## <PIL.Image.Image image mode=RGB size=1648x16128 at 0x7FEB69768040>
