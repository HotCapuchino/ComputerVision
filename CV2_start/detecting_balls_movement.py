import cv2
import time

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError('Camera doesnt work')

cv2.namedWindow('camera', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('mask', cv2.WINDOW_KEEPRATIO)

lower = (10, 120, 180)
upper = (50, 255, 255)

prev_time = time.time()
curr_time = time.time()
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
d = 5.6e-2
radius = 1

while True:
    _, image = cam.read()
    curr_time = time.time()
    image = cv2.flip(image, 1)
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv_image = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
    mask = cv2.inRange(hsv_image, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow('mask', mask)

    contours, _ =  cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c_max = max(contours, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c_max)
        if radius > 10:
            cv2.circle(image, (int(curr_x), int(curr_y)), int(radius), (0, 255, 255), 2)

    time_diff = curr_time - prev_time
    pxl_per_m = d / radius
    dist = ((prev_x - curr_x) ** 2 + (prev_y - curr_y) ** 2) * 0.5
    speed = dist / time_diff * pxl_per_m
    cv2.putText(image, 'Speed: {0:.5f}m/s'.format(speed), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
    cv2.imshow('camera', image)
    
    #   
    # red = 177 170 228
    # yellow = 25 148 217
    # green = 59 122 212
    #

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    prev_time = curr_time
    prev_x, prev_y = curr_x, curr_y

cam.release()
cv2.destroyAllWindows()