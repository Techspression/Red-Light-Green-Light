
from VirtualPainter import RedLight_GreenLight as rg

import cv2
import numpy as np


def empty(img):
    pass


cap = cv2.VideoCapture(0)

cv2.namedWindow("trackBar")
cv2.resizeWindow("trackBar", 500, 400)
cv2.createTrackbar("hue_min", "trackBar", 0, 179, empty)
cv2.createTrackbar("hue_max", "trackBar", 179, 179, empty)
cv2.createTrackbar("sat_min", "trackBar", 0, 255, empty)
cv2.createTrackbar("sat_max", "trackBar", 255, 255, empty)
cv2.createTrackbar("val_min", "trackBar", 0, 255, empty)
cv2.createTrackbar("val_max", "trackBar", 255, 255, empty)

while True:
    ret, image = cap.read()
    cv2.imshow("Frame", image)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", hsv)

    hue_min = cv2.getTrackbarPos("hue_min", "trackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "trackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "trackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "trackBar")
    val_min = cv2.getTrackbarPos("val_min", "trackBar")
    val_max = cv2.getTrackbarPos("val_max", "trackBar")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("mask", mask)

    cnts, hee = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 50:
            x, y, w, h = cv2.boundingRect(c)
            print(x+w, y+h)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cap.destroyAllWindows()
