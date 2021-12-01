import numpy as np
from skimage import color
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu



def get_colour(image):
    hue = np.unique(image[:, :, 0]) * 360
    hue = np.max(hue[hue > 0])
    if 0 < hue <= 20 or hue > 330: 
        return 'red'
    elif 20 < hue <= 40:
        return 'orange'
    elif 40 < hue <= 75:
        return 'yellow'
    elif 75 < hue <= 165:
        return 'green'
    elif 165 < hue <= 190:
        return 'turquoise'
    elif 190 < hue <= 275:
        return 'blue'
    elif 275 < hue <= 330:
        return 'purple'


image = plt.imread('./balls_and_rects.png')
threshold = threshold_otsu(color.rgb2gray(image))
binarized = image > threshold
hsv_image = color.rgb2hsv(image)
labeled = label(binarized)

figures = {
    'squares': {},
    'circles': {}
}

regions = regionprops(labeled)

for region in regions:
    y_min, x_min, _, y_max, x_max, _ = region.bbox

    coloured_image = hsv_image[y_min:y_max, x_min:x_max]
    target_color = get_colour(coloured_image)

    if target_color is None:
        plt.imshow(coloured_image)
        plt.show()
    
    target_figure = ''

    if (np.all(region.image)):
        target_figure = 'squares'
    else:
        target_figure = 'circles'

    found_color = None
    figures_color_keys = figures[target_figure].keys()
    for key_color in figures_color_keys:
        if key_color == target_color:
            found_color = key_color
            break

    if found_color:
        figures[target_figure].update({target_color: figures[target_figure][target_color] + 1})
    else:  
        figures[target_figure].update({target_color: 1})
    

overall_amount = 0

for figure_key in figures.keys():
    figure = figures[figure_key]
    for fig_color in figure.keys():
        overall_amount += figure[fig_color]
        print(f'There are {figure[fig_color]} {fig_color} {figure_key}')
    print('-----------')

print(f'Overall amount of objects: {overall_amount}')