import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError('Camera doesnt work')

cv2.namedWindow('camera', cv2.WINDOW_KEEPRATIO)

position = []

def on_mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y, x]

cv2.setMouseCallback('camera', on_mouse_click)

measures = []
bg_color = []
hsv_color = []
while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)

    if position:
        pxl = image[position[0], position[1]]
        measures.append(pxl)

        if len(measures) > 10:

            bg_color = np.uint8([[np.average(measures, 0)]])
            hsv_color = cv2.cvtColor(bg_color, cv2.COLOR_BGR2HSV)
            bg_color = bg_color[0, 0]
            hsv_color = hsv_color[0, 0]
            measures.clear()
        cv2.circle(image, (position[1], position[0]), 5, (0, 255, 0), 2)

    cv2.putText(image, f'Color back = {bg_color}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
    cv2.putText(image, f'Color hsv = {hsv_color}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
    cv2.imshow('camera', image)
 
    #
    # red = 177 170 228
    # yellow = 25 148 217
    # green = 59 122 222
    #

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()