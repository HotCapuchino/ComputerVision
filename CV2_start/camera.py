import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError('Camera doesnt work')

cv2.namedWindow('back', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('cam', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)

back = None
prev_gray = None
buffer = []
buffer_size = 10
frame_counter = 0

while True:
    _, image = cam.read()
    frame_counter += 1
    image = cv2.flip(image, 1)
    gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gs = cv2.GaussianBlur(gs, (21, 21), 0)
    # gs = cv2.flip(gs, 1)
    cv2.putText(gs, 'two fucking slaves staring at each other', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0))
    
    if frame_counter % 20 == 0:
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gs)   
            buffer.append(diff.mean())
            if len(buffer) > buffer_size:
                buffer.pop(0)
                std = np.std(buffer)
                print(f'std, {std}')
                if std < 4:
                    back = gs.copy()
                    buffer.clear()

    # if prev_gray is not None:
    #     diff = cv2.absdiff(prev_gray, gs)
    #     mx = np.max(diff)
    #     if mx < 10:
    #         back = gs.copy()
 
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    # if key == ord('b'):
    #     back = gs.copy()
    if back is not None:
        delta = cv2.absdiff(back, gs)
        threshold = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)
        contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 400:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('back', threshold)
    cv2.imshow('image', image)

    prev_gray = gs
    # cv2.imshow('cam', gs)

cam.release()
cv2.destroyAllWindows()