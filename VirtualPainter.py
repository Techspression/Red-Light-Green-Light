import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

#######################
brushThickness = 25
eraserThickness = 100
########################

drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)  #for single camera devices.
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
earse = False

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]  # tip of index finger
        x2, y2 = lmList[12][1:]  # tip of middle finger

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # if fingers[1] and fingers[2]:
        #     print("Selection")
        # if fingers[1] and fingers[2] == False:
        #     print("Drawing")
        # 4. If Selection Mode - Two finger are up

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
        #     print("Selection Mode")
        #     # # Checking for the click
        #     if y1 &lt; 125:
        #         if 250 &lt; x1 &lt; 450:
        #             header = overlayList&#91;0]
        #             drawColor = (255, 0, 255)
        #         elif 550 &lt; x1 &lt; 750:
        #             header = overlayList&#91;1]
        #             drawColor = (255, 0, 0)
        #         elif 800 &lt; x1 &lt; 950:
        #             header = overlayList&#91;2]
        #             drawColor = (0, 255, 0)
        #         elif 1050 &lt; x1 &lt; 1200:
        #             header = overlayList&#91;3]
        #             drawColor = (0, 0, 0)
        #     cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor,
                         eraserThickness)

            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor,
                         brushThickness)

            xp, yp = x1, y1

            # # Clear Canvas when all fingers are up
        if all(x >= 1 for x in fingers):
            earse = not earse
            if earse:
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image for changing color n all
    # img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)