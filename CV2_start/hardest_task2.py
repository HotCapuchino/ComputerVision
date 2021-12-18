import cv2
import numpy as np

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Contours", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)

sensitivity = 20
lower_white = np.array([0,0,255-sensitivity])
upper_white = np.array([255,sensitivity,255])

test_phrase = 'I\'m dumb ass bitch'

cam.set(cv2.CAP_PROP_EXPOSURE, -4)

while cam.isOpened():
    _, image = cam.read()
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    cnts = cv2.Canny(gray, 20, 100)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_image, lower_white, upper_white)
    res = cv2.bitwise_and(image, image, mask) 

    contours, _ = cv2.findContours(cnts, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # mean_contour_area = 0
    
    # contours = contours[contours > mean_contour_area]
    # for contour in contours:
    #     cv2.drawContours(image, contour, -1, (0, 255, 0), 3)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    cv2.imshow("Camera", image)
    cv2.imshow("Contours", cnts)
    cv2.imshow("Mask", mask)


cam.release()
cv2.destroyAllWindows()