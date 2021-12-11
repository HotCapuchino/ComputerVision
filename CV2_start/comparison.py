import cv2
import numpy as np


cat_original = cv2.imread('./cat_original.jpg')
cat_replica = cv2.imread('./cat_replica.png', 0)

cat_original_gray = cv2.cvtColor(cat_original, cv2.COLOR_BGR2GRAY)

diff =  cv2.absdiff(cat_original_gray, cat_replica)
thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(cat_original, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.putText(cat_original, f'Differences = {len(contours)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0))

cv2.namedWindow('cat_original', cv2.WINDOW_KEEPRATIO)
cv2.imshow('cat_original', cat_original)
cv2.namedWindow('cat_replica', cv2.WINDOW_KEEPRATIO)
cv2.imshow('cat_replica', cat_replica)
# cv2.namedWindow('diff', cv2.WINDOW_KEEPRATIO)
# cv2.imshow('diff', diff)
# cv2.namedWindow('contours', cv2.WINDOW_KEEPRATIO)
# cv2.imshow('contours', contours)
cv2.waitKey(0)
cv2.destroyAllWindows()