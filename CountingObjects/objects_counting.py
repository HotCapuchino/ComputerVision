from matplotlib import pyplot as plt
import numpy as np
from skimage.measure import label
from scipy.ndimage.morphology import binary_opening


masks = []
first_mask = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
second_mask = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1]])
masks.append(first_mask)
masks.append(second_mask)

masks.append(np.rot90(first_mask))
for i in range(3):
    masks.append(np.rot90(second_mask, i + 1))

image = np.load('./res/ps.npy')
labeled_image = label(image)
print(f'Overall objects amount {np.max(labeled_image)}')

for mask in masks:
    masked_image = binary_opening(image, mask)
    labeled_masked_image = label(masked_image)
    print(f'There are {np.max(labeled_masked_image.ravel())} objects for {mask} mask')
    plt.imshow(masked_image)
    plt.show()
