from numpy.lib.function_base import append, percentile
from skimage.measure import regionprops, label
from skimage.filters import threshold_yen
from skimage.morphology import square, opening
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.ndimage as ndi
from skimage.segmentation import clear_border
import re


images_folder = './images'
available_formats = ['.jpg', '.jpeg', '.png']

TARGET_PENCILS_AMOUNT = 21

target_amount_by_image = {
    '1': 0,
    '2': 1,
    '3': 1,
    '4': 2,
    '5': 2,
    '6': 3,
    '7': 3,
    '8': 1,
    '9': 2,
    '10': 2,
    '11': 3,
    '12': 1
}

def get_neighbours(y, x):
    return (y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)


def get_boundaries(labeled_image, label=1):
    boundaries = []
    for y in range(labeled_image.shape[0]):
        for x in range(labeled_image.shape[1]):
            if labeled_image[y, x] == label:
                neighbours = get_neighbours(y, x)
                for yn, xn in neighbours:
                    if yn < 0 or yn > labeled_image.shape[0] - 1:
                        boundaries.append([y, x])
                        break
                    elif xn < 0 or xn > labeled_image.shape[1] - 1:
                        boundaries.append([y, x])
                        break
                    elif labeled_image[yn, xn] != label:
                        boundaries.append([y, x])
                        break
    return boundaries


def get_distance(px1, px2):
  return ((px1[0] - px2[0]) ** 2 + (px1[1] - px2[1]) ** 2) ** 0.5


def calculate_centroid(labeled_image, label=1):
    pxs = np.where(labeled_image == label)
    centroid_y = np.mean(pxs[0])
    centroid_x = np.mean(pxs[1])
    return (centroid_y, centroid_x)


def get_radial_distances(img):
    centroid = calculate_centroid(img)
    boundaries = get_boundaries(img)
    radial_distances = []
    for yn, xn in boundaries:
        radial_distances.append(get_distance((int(centroid[1]), int(centroid[0])), (xn, yn)))
    return radial_distances


def calculate_pencils(image, pic_num):
    labeled = clear_border(label(image))
    regions = np.array(regionprops(labeled))
    img_options = []
    
    for region in regions:
        filled_holes = ndi.binary_fill_holes(region.image).astype('uint8')
        rad_dists = np.array(get_radial_distances(filled_holes))
        mean_radial = np.mean(rad_dists)
        width = np.min(rad_dists) * 2
        height = np.max(rad_dists) * 2
        greater_mean_len = len(rad_dists[rad_dists > mean_radial])
        less_mean_len = len(rad_dists[rad_dists <= mean_radial])
        if abs(greater_mean_len - less_mean_len) <= len(rad_dists) * 0.05 and width / height < 0.05:
            img_obj = {
                'area': region.area,
                'perimeter': region.perimeter_crofton,
                'pic_num': pic_num
            }
            img_options.append(img_obj)
    
    return img_options


def prepare_image(image):
    grayscale_image = rgb2gray(image)
    threshold = threshold_yen(grayscale_image)

    binary = grayscale_image < threshold
    binary = opening(binary, square(5))
    binary = ndi.filters.gaussian_filter(binary, 3)
    return binary


def get_img_num(filename): 
    num_re = re.compile(r'(\(\d{1,}\))')
    result = re.search(num_re, filename)
    return result.group(0).replace('(', '').replace(')', '')

areas = []
perimiters = []

pencils_amount = 0
img_options = []

for filename in os.listdir(images_folder):
    if (os.path.splitext(filename)[-1].lower() in available_formats):
        image = plt.imread(f'{images_folder}/{filename}')
        binary = prepare_image(image)
        img_opts = calculate_pencils(binary, get_img_num(filename))
        img_options.extend(img_opts)

for img_option in img_options:
    areas.append(img_option['area'])
    perimiters.append(img_option['perimeter'])

mean_area = np.mean(areas)
mean_perimeter = np.mean(perimiters)
img_options = list(filter(lambda obj: obj['area'] > mean_area and obj['perimeter'] > mean_perimeter, img_options))

failed = False
if len(img_options) > TARGET_PENCILS_AMOUNT:
    print('Oops! Seems like I\'ve recognized more pencils than it has to be!')
    failed = True
else:
    recognition_percent = (len(img_options) / TARGET_PENCILS_AMOUNT) * 100 
    print(f'Recognized: {recognition_percent}%')
    if recognition_percent != 100:
        failed = True

print('Images, where troubles emerged:')
if failed:
    for image in target_amount_by_image.keys():
        recognized = len(list(filter(lambda obj: obj['pic_num'] == image, img_options)))
        if recognized != target_amount_by_image.get(image):
            print(f'Recognized: {recognized}, should be: {target_amount_by_image.get(image)}; pic number: {image}')
