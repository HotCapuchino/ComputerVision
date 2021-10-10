import numpy as np


def find_object_area(image):
    left_top: [int, int] = [image.shape[1] + 1, image.shape[0] + 1]
    right_bottom: [int, int] = [-1, -1]
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 1:
                if x < left_top[0]:
                    left_top[0] = x
                if x > right_bottom[0]:
                    right_bottom[0] = x
                if y < left_top[1]:
                    left_top[1] = y
                if y > right_bottom[1]:
                    right_bottom[1] = y
    if left_top == [image.shape[1] + 1, image.shape[0] + 1] or right_bottom == [-1, -1]:
        return None
    return left_top, right_bottom


def calculate_offset(image1, image2) -> [int, int] or None:
    left_top_image1, right_bottom_image1 = find_object_area(image1)
    left_top_image2, right_bottom_image2 = find_object_area(image2)
    print(left_top_image1, right_bottom_image1)
    print(left_top_image2, right_bottom_image2)
    left_top_offset = list(map(abs, np.array(left_top_image1) - np.array(left_top_image2)))
    right_bottom_offset = list(map(abs, np.array(right_bottom_image1) - np.array(right_bottom_image2)))
    if left_top_offset != right_bottom_offset:
        return
    return left_top_offset


def read_image(path):
    image_file = open(path)
    image_buffer = image_file.read().split('#')[1]
    image_buffer = image_buffer.split('\n')
    image = []
    for row in image_buffer:
        if len(row):
            image.append(list(map(float, row.split())))
    return image


image1 = np.array(read_image('./res/img1.txt'))
image2 = np.array(read_image('./res/img2.txt'))

offset = calculate_offset(image1, image2)
if offset:
    print(f'Offset equals to {offset[0]} by X and {offset[1]} by Y')
else:
    print('Seems like one of the images is different')
