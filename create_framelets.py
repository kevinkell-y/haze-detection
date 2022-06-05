#=================================================================
#
# Divides a raw image into its individual framelets
# Modularized component from NASA JPL's JunoCamImageProcessing_v2.py script
#
#=================================================================
from PIL import Image

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
