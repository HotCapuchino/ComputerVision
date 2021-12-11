import cv2
import numpy as np


cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError('Camera doesnt work')

cv2.namedWindow('camera', cv2.WINDOW_KEEPRATIO)
# cv2.namedWindow('red', cv2.WINDOW_KEEPRATIO)
# cv2.namedWindow('green', cv2.WINDOW_KEEPRATIO)
# cv2.namedWindow('yellow', cv2.WINDOW_KEEPRATIO)

balls_color_bondaries = [
    [(44, 100, 150), (85, 255, 255), 'green'], # green
    [(130, 120, 160), (180, 255, 255), 'red'], # red
    [(10, 120, 180), (50, 255, 255), 'yellow'] # yellow
]

order = []
detected = []
remembered = False
was_printed = False
confirmed = False
shown_order = []

while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv_image = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    if not remembered or confirmed: 
        detected = []
        for color_bound in balls_color_bondaries:
            mask = cv2.inRange(hsv_image, color_bound[0], color_bound[1])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # cv2.imshow(color_bound[2], mask)

            contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                c_max = max(contours, key=cv2.contourArea)
                (curr_x, curr_y), radius = cv2.minEnclosingCircle(c_max)
                if radius > 10:
                    cv2.circle(image, (int(curr_x), int(curr_y)), int(radius), (255, 255, 255), 2)
                    detected.append({
                        'color': color_bound[2], 
                        'center': (curr_x, curr_y)
                    })

    if not was_printed and len(detected) == 3:
        detected = sorted(detected, key=lambda item: item['center'][0])
        order = []
        for ball in detected:
            order.append(ball['color'])
        was_printed = True

    if confirmed and len(detected) == 3:
        detected = sorted(detected, key=lambda item: item['center'][0])
        shown_order = []
        for ball in detected:
            shown_order.append(ball['color'])
        print(shown_order, order, end='\n')
        if shown_order != order:
            print('Wrong order!')
        else:
            print('Right order!')
        was_printed = True

    cv2.imshow('camera', image)
 
    #
    # red = 177 170 228
    # yellow = 25 148 217
    # green = 59 122 222
    #

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('r') and len(detected) == 3:
        remembered = True
    if key == ord('p'):
        was_printed = False
    if key == ord('c'):
        was_printed = False
        confirmed = True

cam.release()
cv2.destroyAllWindows()