import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError('Camera doesnt work')

cv2.namedWindow('ROI', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('cam', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('template', cv2.WINDOW_KEEPRATIO)

roi = None

while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)
    gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gs = cv2.GaussianBlur(gs, (15, 15), 0)

    if roi is not None:
        res = cv2.matchTemplate(gs, roi, cv2.TM_CCORR_NORMED)
        cv2.imshow('template', res)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + roi.shape[1], top_left[1] + roi.shape[0])
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    cv2.imshow('camera', image)
 
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('r'):
        r = cv2.selectROI('ROI Selection', gs)
        roi = gs[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        cv2.imshow('ROI', roi)
        cv2.destroyWindow('ROI Selection')

cam.release()
cv2.destroyAllWindows()