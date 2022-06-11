import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import csv


def main():
    filename = 'JNCR_2018197_14C00024_V02.IMG' # change the filename to the name of the .IMG that is being processed
    raw_image = create_raw_image(filename) # create raw image

    framelets = divide_image(raw_image) # divide the raw image into its indivudal framelets
    framelet = framelets[4] # change this index to whichever framelet to process
    framelet_pixels = framelet.load()
    limb_endpoints = trace_limb_polyline(framelet, raw_image) # list of indices of the endpoints of the limb polyline

    x_step = 20 # number of steps taken in the x-direction to rectify the limb
    y_step = 80 # number of steps taken in the y-direction to rectify the limb
    width = x_step * len(limb_endpoints) # width of rectified limb image
    height = y_step # height of rectified limb image

    # obtains the rectified limb image, rectified limb pixel value arrays (with exact values), and the
    # boundary points of each rectangle of the polyline segment
    rect_limb, rect_limb_exact, boundary_points = rectify_limb(framelet, limb_endpoints, x_step, y_step, width, height)

    # label the haze using bright green pixels on the raw framelet being processed
    label_haze(framelet, boundary_points)

    # condenses the rectified limb image with respect to the x-axis
    condensed_range = 72
    width_condensed = int(width / condensed_range)
    rect_limb_condensed, rect_limb_condensed_exact = condense_rectified_limb(rect_limb_exact, width, height,
                                                                             condensed_range, width_condensed)

    # plot the cross section of the haze
    plot_graph(height, width_condensed, rect_limb_condensed_exact)

    # displays the raw framelet with haze labeled with bright green hazes
    framelet.show()

    # displays the plots of the cross section of the hazes
    plt.show()

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

# rectifies the limb given the polyline
def rectify_limb(framelet, limb_endpoints, x_step, y_step, width, height):
    rect_limb = Image.new("RGB", (width, height))
    rect_limb_pixels = rect_limb.load()
    rect_limb_exact = []
    for i in range(width):
        rect_limb_exact.append([0] * height)
    count = 0
    boundary_points = []
    for p in range(len(limb_endpoints)):
        if p > 0:
            difference_x = limb_endpoints[p][0] - limb_endpoints[p - 1][0]
            difference_y = limb_endpoints[p][1] - limb_endpoints[p - 1][1]
            distance = math.sqrt(difference_x ** 2 + difference_y ** 2)
            if distance < 9 or distance > 11:
                continue
            angle = math.atan(difference_y / difference_x)
            radius = 10

            #if indices of boundary rectange are out of bounds, disregard segment
            point1_x = limb_endpoints[p - 1][0] - radius * math.sin(angle)
            if point1_x < 0 or point1_x >= 1648:
                continue
            point1_y = limb_endpoints[p - 1][1] + radius * math.cos(angle)
            if point1_y < 0 or point1_y >= 128:
                continue
            point2_x = limb_endpoints[p - 1][0] + radius * math.sin(angle)
            if point2_x < 0 or point2_x >= 1648:
                continue
            point2_y = limb_endpoints[p - 1][1] - radius * math.cos(angle)
            if point2_y < 0 or point2_y >= 128:
                continue
            point3_x = limb_endpoints[p][0] - radius * math.sin(angle)
            if point3_x < 0 or point3_x >= 1648:
                continue
            point3_y = limb_endpoints[p][1] + radius * math.cos(angle)
            if point3_y < 0 or point3_y >= 128:
                continue
            point4_x = limb_endpoints[p][0] + radius * math.sin(angle)
            if point4_x < 0 or point4_x >= 1648:
                continue
            point4_y = limb_endpoints[p][1] - radius * math.cos(angle)
            if point4_y < 0 or point4_y >= 128:
                continue

            diff_col_x = point2_x - point1_x
            diff_col_y = point2_y - point1_y
            diff_row_x = point3_x - point1_x
            diff_row_y = point3_y - point1_y
            boundary_points.append([point1_x, point1_y, point2_x, point2_y, point3_x, point3_y])
            for i in range(x_step):
                starting_point_x = point1_x + i / x_step * diff_row_x
                starting_point_y = point1_y + i / x_step * diff_row_y
                for j in range(height):
                    val = get_pixel_value(starting_point_x + j / height * diff_col_x,
                                          starting_point_y + j / height * diff_col_y, framelet)
                    rect_limb_exact[count * x_step + i][y_step - 1 - j] = val
                    rect_limb_pixels[count * x_step + i, y_step - 1 - j] = (int(val), int(val), int(val))
            count += 1
    return (rect_limb, rect_limb_exact, boundary_points)

#labels the haze using bright green pixels on the original raw framelet
def label_haze(framelet, boundary_points):
    framelet_pixels = framelet.load()
    haze_points_rows = [["X Index", "Y Index"]]
    for b in range(len(boundary_points)):
        diff_col_x = boundary_points[b][2] - boundary_points[b][0]
        diff_col_y = boundary_points[b][3] - boundary_points[b][1]
        diff_row_x = boundary_points[b][4] - boundary_points[b][0]
        diff_row_y = boundary_points[b][5] - boundary_points[b][1]
        for i in range(23, 38):
            starting_point_x = boundary_points[b][0] + (1 - i / 79.0) * diff_col_x
            starting_point_y = boundary_points[b][1] + (1 - i / 79.0) * diff_col_y
            for j in range(20):
                index_x = float(starting_point_x + j / 20.0 * diff_row_x)
                index_y = float(starting_point_y + j / 20.0 * diff_row_y)
                if framelet_pixels[index_x, index_y][1] != 255 and framelet_pixels[index_x, index_y][0] != 0:
                    framelet_pixels[index_x, index_y] = (0, 255, 0)
                    haze_points_rows.append([str(index_x) + "\t", str(index_y) + "\t"])
        with open('haze_points.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(haze_points_rows)

# condenses the rectified limb image along the x-direction
def condense_rectified_limb(rect_limb_exact, width, height, condensed_range, width_condensed):
    rect_limb_condensed = Image.new("RGB", (width_condensed, height))
    rect_limb_condensed_pixels = rect_limb_condensed.load()
    rect_limb_condensed_exact = []
    for i in range(width_condensed):
        rect_limb_condensed_exact.append([0] * height)
    for i in range(width_condensed):
        for j in range(height):
            sum = 0
            for k in range(condensed_range):
                sum += rect_limb_exact[i * condensed_range + k][j]
            avg = sum / condensed_range
            rect_limb_condensed_exact[i][j] = avg
            rect_limb_condensed_pixels[i, j] = (int(avg), int(avg), int(avg))
    return (rect_limb_condensed, rect_limb_condensed_exact)

# plots the graphs with respect to the y-direction
def plot_graph(height, width_condensed, rect_limb_condensed_exact):
    plt.title("Pixel Values as a Function of Y Position")
    plt.xlabel("Y Position")
    plt.ylabel("Pixel Value Derivative")
    x = []
    for i in range((height - 1)):
        x.append(i)
    count = 0
    csv_rows = [["Column", "Y Index", "Pixel Value"]]
    for j in range(width_condensed):
        y = []
        for i in range((height - 1)):
            val2 = rect_limb_condensed_exact[j][i + 1] - rect_limb_condensed_exact[j][i]
            # val2 = rect_limb_condensed_exact[j][i]
            csv_rows.append([str(j) + "\t", str(i) + "\t", val2])
            y.append(val2)
        all_zero = True
        for s in range(len(y)):
            if (y[s] != 0):
                all_zero = False
                break
        if not all_zero:
            std = np.std(y)
            error = std / math.sqrt(len(y) - 1)
            error_list = [error] * len(y)
            plt.scatter(x, y)
            plt.errorbar(x, y, yerr=error_list, fmt="o")
            plt.plot(x, y)
            count += 1
    with open('pixel_values.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(csv_rows)

if __name__ == "__main__":
    main()
