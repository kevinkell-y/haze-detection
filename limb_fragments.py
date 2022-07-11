import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



def main():
    filename = 'JNCR_2018197_14C00024_V02.IMG' # change the filename to the name of the .IMG that is being processed
    raw_image = create_raw_image(filename) # create raw image
    framelets = divide_image(raw_image) # divide the raw image into its individual framelets
    framelet = framelets[4] # change this index to whichever framelet to process
    framelet_pixels = framelet.load()
    limb_endpoints = trace_limb_polyline(framelet, raw_image) # list of indices of the endpoints of the limb polyline

    points = np.array(limb_endpoints)
    x, y = points.T

    for x,y in limb_endpoints:
        framelet_pixels[x, y] = (255, 0, 0) # Label each pixel containing limb fragment bright red

    # displays the raw framelet with limb fragments
    framelet.show()

    #plt.title("Limb Endpoints")
    #plt.scatter(x,y)
    #plt.show()

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

# finds the left-most point of the limb, using it as a starting point to start tracing out the limb
def find_starting_limb_point(img):
    pixels = img.load()
    max_diff = 0
    max_index_x, max_index_y = 0, 0
    for i in range(img.size[0]):
        prev_pixel = 0
        for j in range(img.size[1]):
            diff = pixels[i, j][0] - prev_pixel
            if diff > max_diff:
                max_index_x = i
                max_index_y = j
                max_diff = diff
                prev_pixel = pixels[i, j][0]
        if max_diff > 50:
            break
    return (max_index_x, max_index_y)

# finds the next endpoint on the limb polyline
def find_next_limb_point(img, prev_point, radius):
    next_point = (0, 0)
    max_diff = 0
    prev_point_x, prev_point_y = prev_point
    for index in range(-9000, 9100, 4):
        deg = index/100.0
        new_x = prev_point_x + radius * math.cos(deg * math.pi / 180)
        if new_x < 0:
            new_x = 0
        if new_x >= img.size[0]:
            new_x = img.size[0] - 1
        new_y = prev_point_y + radius * math.sin(deg * math.pi / 180)
        if new_y < 0:
            new_y = 0
        if new_y >= img.size[1]:
            new_y = img.size[1] - 1

        deg_range = 0.01

        new_min_x = prev_point_x + radius * math.cos((deg - deg_range) * math.pi / 180)
        if new_min_x < 0:
            new_min_x = 0
        if new_min_x >= img.size[0]:
            new_min_x = img.size[0] - 1
        new_min_y = prev_point_y + radius * math.sin((deg - deg_range) * math.pi / 180)
        if new_min_y < 0:
            new_min_y = 0
        if new_min_y >= img.size[1]:
            new_min_y = img.size[1] - 1

        new_max_x = prev_point_x + radius * math.cos((deg + deg_range) * math.pi / 180)
        if new_min_x < 0:
            new_max_x = 0
        if new_max_x >= img.size[0]:
            new_max_x = img.size[0] - 1
        new_max_y = prev_point_y + radius * math.sin((deg + deg_range) * math.pi / 180)
        if new_max_y < 0:
            new_max_y = 0
        if new_max_y >= img.size[1]:
            new_max_y = img.size[1] - 1

        point1 = get_pixel_value(new_min_x, new_min_y, img)
        point2 = get_pixel_value(new_max_x, new_max_y, img)

        diff = abs(point1 - point2)
        if diff > max_diff:
            next_point = (new_x, new_y)
            max_diff = diff
    return next_point

# gets subpixel values using bilinear interpolation, using weighted average of neighboring pixels
def get_pixel_value(x, y, img):
    pixels = img.load()
    center_x = int(x) + 1
    center_y = int(y) + 1
    if center_x >= img.size[0]:
        center_x = img.size[0] - 1
    if center_y >= img.size[1]:
        center_y = img.size[1] - 1
    val = 0
    val += (center_x - x) * (center_y - y) * pixels[int(x), int(y)][0]
    val += (center_x - x) * (y - center_y + 1) * pixels[int(x), center_y][0]
    val += (x - center_x + 1) * (center_y - y) * pixels[center_x, int(y)][0]
    val += (x - center_x + 1) * (y - center_y + 1) * pixels[center_x, center_y][0]
    return val

# traces the entire limb polyline of the framelet
def trace_limb_polyline(framelet, raw_image):
    limb_endpoints = []
    curr_point = find_starting_limb_point(framelet)
    limb_endpoints.append(curr_point)
    while curr_point[0] > 0 and curr_point[0] < raw_image.size[0] and curr_point[1] > 0 and curr_point[1] < \
            raw_image.size[1]:
        curr_point = find_next_limb_point(framelet, curr_point, 10)
        limb_endpoints.append(curr_point)
    return limb_endpoints

# #labels the haze using bright green pixels on the original raw framelet
# def label_haze(framelet, boundary_points):
#     framelet_pixels = framelet.load()
#     haze_points_rows = [["X Index", "Y Index"]]
#     for b in range(len(boundary_points)):
#         diff_col_x = boundary_points[b][2] - boundary_points[b][0]
#         diff_col_y = boundary_points[b][3] - boundary_points[b][1]
#         diff_row_x = boundary_points[b][4] - boundary_points[b][0]
#         diff_row_y = boundary_points[b][5] - boundary_points[b][1]
#         for i in range(23, 38):
#             starting_point_x = boundary_points[b][0] + (1 - i / 79.0) * diff_col_x
#             starting_point_y = boundary_points[b][1] + (1 - i / 79.0) * diff_col_y
#             for j in range(20):
#                 index_x = float(starting_point_x + j / 20.0 * diff_row_x)
#                 index_y = float(starting_point_y + j / 20.0 * diff_row_y)
#                 if framelet_pixels[index_x, index_y][1] != 255 and framelet_pixels[index_x, index_y][0] != 0:
#                     framelet_pixels[index_x, index_y] = (0, 255, 0)
#                     haze_points_rows.append([str(index_x) + "\t", str(index_y) + "\t"])
#         with open('haze_points.csv', 'w') as file:
#             writer = csv.writer(file)
#             writer.writerows(haze_points_rows)

if __name__ == "__main__":
    main()
