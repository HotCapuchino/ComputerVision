import cv2
import numpy as np

mush = cv2.imread('./mushroom.jpg')
logo = cv2.imread('./logo.png')

# logo = cv2.resize(logo, (logo.shape[1] // 2, logo.shape[0] // 2))
# gray_logo = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)

# ret, mask = cv2.threshold(gray_logo, 10, 255, cv2.THRESH_BINARY)
# roi = mush[:logo.shape[0], :logo.shape[1]]
# mask_inv = cv2.bitwise_not(mask)

# background = cv2.bitwise_and(roi, roi, mask=mask_inv)
# foreground = cv2.bitwise_and(logo, logo, mask=mask)
# combined = cv2.add(background, foreground)

# mush[:combined.shape[0], :combined.shape[1]] = combined

# cv2.namedWindow('Image', cv2.WINDOW_KEEPRATIO)
# cv2.imshow('Image', mush)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# rose = cv2.imread('./rose.jpg')
# rose_hsv = cv2.cvtColor(rose, cv2.COLOR_BGR2HSV)
# lower = np.array([0, 200, 100])
# upper = np.array([0, 255, 255])

# mask = cv2.inRange(rose_hsv, lower, upper)
# res = cv2.bitwise_and(rose, rose, mask=mask)

# cv2.namedWindow('Image', cv2.WINDOW_KEEPRATIO)
# cv2.imshow('Image', res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

news = cv2.imread('./news.jpg')
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError('Camera doesnt work')


# cheburek = cv2.imread('./cheburashka.jpg')
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
images = []

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, (frame_width,frame_height))
cv2.namedWindow("Image")
while True: 
    ret, cheburek = cam.read()
    cheburek = cv2.flip(cheburek, 1)

    rows, cols, _ = cheburek.shape
    pts1 = np.float32([(0, 0), (0, rows), (cols, 0), (cols, rows)])
    pts2 = np.float32([(19, 25), (39, 294), (434, 51), (434, 266)])
    M = cv2.getPerspectiveTransform(pts1, pts2)

    aff_img = cv2.warpPerspective(cheburek, M, (cols, rows))
    aff_img = aff_img[:-150, :-150]
    gray = cv2.cvtColor(aff_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    roi = news[:aff_img.shape[0], :aff_img.shape[1]]
    mask_inv = cv2.bitwise_not(mask)

    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    image = cv2.add(aff_img, bg)
    news[:image.shape[0], :image.shape[1]] = image
    cv2.imshow("Image", news)
    images.append(news)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()

# for i in range(len(images)):
#     out.write(images[i])

cam.release()
out.release()