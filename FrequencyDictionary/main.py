import numpy as np
import matplotlib.pyplot as plt
from skimage import draw
from skimage.measure import label, regionprops

def lakes_and_bays(image):
  binary = ~image
  labeled_binary = label(binary)
  regs = regionprops(labeled_binary)
  count_lakes = 0
  count_bays = 0
  for reg in regs:
    on_bound = False
    for y, x in reg.coords:
      if y == 0 or  x == 0 or y == image.shape[0] - 1 or x == image.shape[1] - 1:
        on_bound = True
        break
    if not on_bound:
      count_lakes += 1
    else:
      count_bays += 1
  return count_lakes, count_bays  

def has_vline(region):
  lines = np.sum(region.image, 0) // region.image.shape[0]
  return 1 in lines

def filling_factor(region):
  return np.sum(region.image) / region.image.size

def get_area(region, label): 
    return np.array(np.where(region == label, region)).flatten().size

def find_centroid(binary_image, axis='X', offset='end'):
  centerY, centerX = binary_image.shape[0] // 2, binary_image.shape[1] // 2
  if axis == 'X':
    if offset == 'start':
      return binary_image[centerY, 0] > 0
    elif offset == 'center':
      return binary_image[centerY, centerX] > 0
    elif offset == 'end':
      return binary_image[centerY, -1] > 0
  elif axis == 'Y':
    if offset == 'start':
      return binary_image[0, centerX] > 0
    elif offset == 'center':
      return binary_image[centerY, centerX] > 0
    elif offset == 'end':
      return binary_image[-1, centerX] > 0

def recognize(region):
  if np.all(region.image):
    return '-'
  cl, cb = lakes_and_bays(region.image)
  if cl == 2:
    if has_vline(region):
      return 'B'
    else: 
      return '8'
  if cl == 1:
    if cb == 3:
      return 'A'
    if cb == 2:
      if has_vline(region):
        if find_centroid(region.image, axis='Y', offset='center'):
          return 'P'
        else:
          return 'D'
    else:
      return '0'
  if cl == 0:
    if has_vline(region):
      return '1'
    if cb == 2:
      return '/'
    _, cut_cb = lakes_and_bays(region.image[2:-2, 2:-2])
    if cut_cb == 4:
      return 'X'
    if cut_cb == 5:  
      cy = region.image.shape[0] // 2
      cx = region.image.shape[1] // 2
      if region.image[cy, cx] != 0:
        return '*'
      else: 
        return 'W'
  return None



alphabet = plt.imread('./res/alphabet.png')
gray_alphabet = np.sum(alphabet, 2)
gray_alphabet[gray_alphabet > 0] = 1 

labeled_im = label(gray_alphabet)
regions = regionprops(labeled_im)
print(np.max(labeled_im))
    
d = {}
for region in regions:
  symbol = recognize(region)
  if symbol not in d:
    d[symbol] = 0
  d[symbol] += 1
print(d)

if None not in d:
  print('100%')
else:
  print('recognized: ', round((1.0 - d[None] / sum(d.values())) * 100, 2), '%')

plt.figure(figsize=(100, 100))
plt.imshow(gray_alphabet)
plt.show()