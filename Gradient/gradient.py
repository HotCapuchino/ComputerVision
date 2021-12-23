import matplotlib.pyplot as plt
import numpy as np

def lerp(color1, color2, t):
    return (1 - t) * color1 + t * color2

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = [255, 128, 0]
color2 = [0, 128, 255] 

for j, v in enumerate(np.linspace(0, 1, image.shape[0])):
  for i, p in enumerate(np.linspace(0, 1, image.shape[1])):
      temp = (v + p) / 2
      r = lerp(color1[0], color2[0], temp)
      g = lerp(color1[1], color2[1], temp)
      b = lerp(color1[2], color2[2], temp)
      image[i, j, :] = [r, g, b]

plt.imshow(image)
plt.show()