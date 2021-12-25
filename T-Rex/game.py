import mss
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
from skimage import util
import pyautogui


DYNO_BBOX = None
DYNO = None
# захардкожено
SPEED = 1

JUMPS_TOTAL = 0

def find_dyno(labeled):
    global DYNO_BBOX
    global DYNO

    if not DYNO_BBOX and not DYNO:
        mean_area = np.mean([region.area for region in regionprops(labeled)])
        min_bbox = None
        for region in regionprops(labeled):
            # фильтруем изображения поверхности
            if region.area > mean_area: 
                min_row, min_col, _, _ = region.bbox
                if not min_bbox:
                    min_bbox = region.bbox
                elif min_row < min_bbox[0] and min_col < min_bbox[1]:
                    min_bbox = region.bbox
        if min_bbox:
            DYNO = min_bbox
            min_bbox = list(min_bbox) 
            # height
            min_bbox[0] -= 10 
            # width
            # захардкожено (динозавр смещается немного вперед после старта)
            min_bbox[3] += 100
            DYNO_BBOX = min_bbox
            # plt.imshow(labeled[DYNO_BBOX[0]:DYNO_BBOX[2], DYNO_BBOX[1]:DYNO_BBOX[3]])
            # plt.show()
            return True
    return False


def has_vline(region):
    for x in range(region.image.shape[1]):
        if np.all(region.image[:, x]):
            return True
    return False


def has_interception(region, type):
    if type == 'cacti':
        if region.bbox[1] < DYNO_BBOX[3]:
            return True
    elif region.bbox[1] < DYNO_BBOX[3] and region.bbox[2] > DYNO[0]:
        return True
    return False
        

def run(labeled):
    global JUMPS_TOTAL
    labeled[DYNO[0]:DYNO[2], DYNO[1]:DYNO[3]] = 0
    copy = np.zeros_like(labeled)

    mean_area = np.mean([region.area for region in regionprops(labeled)])
    for region in regionprops(labeled):
        if region.bbox == DYNO:
            return

        if region.area >= mean_area and region.image.shape[0] > 20:
            if has_vline(region):
                if has_interception(region, type='cacti'):
                    pyautogui.press('up')
                    # time.sleep(1 - 0.01 * SPEED)
                    # pyautogui.press('down')
                    # copy[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]] = region.image
                    # plt.imshow(copy)
                    # plt.show()
                    JUMPS_TOTAL += 1  
            # elif has_interception(region, type='pterodactyl'):
            #     copy[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]] = region.image
            #     plt.imshow(copy)
            #     plt.show()
            #     pyautogui.press('up')


def process_image(image):
    gs = rgb2gray(image)
    threshold = threshold_otsu(gs)
    binarized = (threshold > gs).astype('uint8')
    return label(binarized)


def increase_speed(last_time):
    global SPEED
    if time.time() - last_time > 20:
        DYNO_BBOX[3] += 10
        SPEED += 1
        return True
    return False
    # global JUMPS_TOTAL
    # global DYNO_BBOX

    # if JUMPS_TOTAL % 20 == 0 and JUMPS_TOTAL > 0:
    #     DYNO_BBOX[3] += 20
    #     pass

def validate_day(binarized, current_time):
    est_time = binarized[0, 0] == 0 if 'day' else 'night'
    if est_time != current_time:
        return util.invert(binarized), est_time


# захардкожено
monitor = {"top": 250, "left": 650, "width": 600, "height": 100}

time.sleep(3)

with mss.mss() as sct:
    # start the game
    pyautogui.press('up')
    current_time = 'day'
    last_time = time.time()

    while (True): 
        screen = sct.grab(monitor)
        image = np.array(Image.frombytes("RGB", screen.size, screen.bgra, "raw", "BGRX"))
        # binarized = process_image(image)
        processed_image = process_image(image)

        # binarized, current_time = validate_day(binarized, current_time)

        if not DYNO_BBOX:
            # hardcoded, dyno moves at the start of the game
            time.sleep(2)
            find_dyno(processed_image)
            last_time = time.time()

        if increase_speed(last_time):
            last_time = time.time()

        run(processed_image)