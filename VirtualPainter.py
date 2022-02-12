import cv2
from flask import Flask, Response, render_template
from matplotlib.pyplot import contour
import numpy as np
import time
import os
import HandTrackingModule as htm
import random

# Rules for drawing
# to move use make sure your palm is open
# to draw make sure just your index finger is open
# to erase make sure just your thumn and index finger is open
####
#########
# put startDrawing cursor to 0 when ever our finger position changes from up to down or anything if constant keep it same (for later ignore for now)
##
win = Flask(__name__)


@win.route('/')
def index():
    return render_template('index.html')


class RedLight_GreenLight():

    def __init__(self):
        self.color = (255, 0, 255)  # drawColor varaible
        self.brushThickness = 20
        self.eraserThickness = 65
        self.currentLight = False
        self.resetTimer = 15
        self.eraser = False
        self.startDrawingPosition = (0, 0)  # storing co-ordinate value , xp,yp
        self.currentDrawingPosition = (0, 0)  # x1,y1 variable

    def start(self):

        cam = self.getCAM()
        self.initializing()

        self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        frameCount = 0
        while True:
            self.changeLight()

            success, self.image = cam.read()

            if not success:
                break

            self.image = cv2.flip(self.image, 1)

            frameCount += 1
            fgmask = self.motion.apply(self.image)
            count = np.count_nonzero(fgmask)
            self.alertWarning(frameCount, count)

            self.showState()

            self.image = self.hand.findHands(self.image)
            lmList, bbox = self.hand.findPosition(self.image, draw=False)

            if (len(lmList) != 0):

                self.currentDrawingPosition = lmList[8][1:]
                fingers = self.hand.fingersUp()

                self.modes(fingers)

            else:
                # print("Hand didn't detect.")
                pass
                # break

            self.gray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
            imgInv = cv2.cvtColor(
                cv2.threshold(self.gray, 50, 255, cv2.THRESH_BINARY_INV)[1],
                cv2.COLOR_GRAY2BGR)
            self.image = cv2.bitwise_and(self.image, imgInv)
            self.image = cv2.bitwise_or(self.image, self.imgCanvas)

            # if (not np.all((self.imgCanvas == np.zeros(
            #     (720, 1280, 3), np.uint8)))):
            #     self.imgCanny = cv2.Canny(gray, 23, 20)
            #     kernel = np.ones((5, 5))
            #     imgDil = cv2.dilate(self.imgCanny, kernel, iterations=1)
            #     self.drawContour(imgDil, self.imgCanny)
            # cv2.imshow("Drawing", self.imgCanny)

            cv2.imshow("Image", self.image)

            # _, buffer = cv2.imencode('.jpg', self.image)
            # self.image = buffer.tobytes()
            # for exiting purpose
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                cam.release()
                cv2.destroyAllWindows()
                break

            # it'll return self.image toflask app
            # yield (b'--frame\r\n'
            #         b'Content-Type: image/jpeg\r\n\r\n' + self.image + b'\r\n')

    def initializing(self):
        self.hand = htm.handDetector(maxHands=1)  # detector variable
        self.motion = cv2.createBackgroundSubtractorMOG2(300, 400,
                                                         True)  # fgbh variable

    def getCAM(self):
        cap = cv2.VideoCapture(0)  # for single camera devices.
        cap.set(3, 1280)
        cap.set(4, 720)
        return cap

    def changeLight(self):
        if (self.resetTimer == 0):
            self.resetTimer = random.randint(20, 35)
            self.currentLight = not self.currentLight
        else:
            self.resetTimer -= 1

    def showState(self):
        cv2.putText(self.image, ("GREEN" if self.currentLight else "RED"),
                    (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    ((0, 255, 0) if self.currentLight else
                     (0, 0, 255)), 2, cv2.LINE_AA)

    def alertWarning(self, frameCount, count):
        #print('Frame: %d, Pixel Count: %d' % (frameCount, count))
        if self.currentLight == False:
            if (frameCount > 1 and count > 5000):
                # print('Halu nkos bhava')
                cv2.putText(self.image, 'Halu nkos bhava', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            cv2.LINE_AA)

    def modes(self, fingers):
        # new Moving
        if all(x == True for x in fingers):
            self.startDrawingPosition = 0, 0
            if (not np.all((self.imgCanvas == np.zeros(
                (720, 1280, 3), np.uint8)))):
                self.imgCanny = cv2.Canny(self.gray, 23, 20)
                kernel = np.ones((5, 5))
                imgDil = cv2.dilate(self.imgCanny, kernel, iterations=1)
                self.drawContour(imgDil, self.imgCanny)

        # for moving
        # if fingers[1] and fingers[2] and all(x == False for x in fingers[3:]):
        #     self.startDrawingPosition = 0, 0

        # new Erasing
        elif fingers[0] and fingers[1]:
            if self.startDrawingPosition == (0, 0):
                self.startDrawingPosition = self.currentDrawingPosition
            self.color = (0, 0, 0)
            cv2.circle(self.image, self.currentDrawingPosition, 15, self.color,
                       cv2.FILLED)

            cv2.line(self.image, self.startDrawingPosition,
                     self.currentDrawingPosition, self.color,
                     self.eraserThickness)
            cv2.line(self.imgCanvas, self.startDrawingPosition,
                     self.currentDrawingPosition, self.color,
                     self.eraserThickness)

            self.startDrawingPosition = self.currentDrawingPosition

        # for Erasing
        # elif all(x == True for x in fingers[:2]) and all(x == False
        #                                                  for x in fingers[2:]):
        #     if self.startDrawingPosition == (0, 0):
        #         self.startDrawingPosition = self.currentDrawingPosition
        #     self.color = (0, 0, 0)
        #     cv2.circle(self.image, self.currentDrawingPosition, 15, self.color,
        #                cv2.FILLED)

        #     cv2.line(self.image, self.startDrawingPosition,
        #              self.currentDrawingPosition, self.color,
        #              self.eraserThickness)
        #     cv2.line(self.imgCanvas, self.startDrawingPosition,
        #              self.currentDrawingPosition, self.color,
        #              self.eraserThickness)

        #     self.startDrawingPosition = self.currentDrawingPosition

        # new Drawing
        elif fingers[1]:
            self.color = (255, 0, 255)
            if self.startDrawingPosition == (0, 0):
                self.startDrawingPosition = self.currentDrawingPosition

            cv2.circle(self.image, self.currentDrawingPosition, 15, self.color,
                       cv2.FILLED)

            cv2.line(self.image, self.startDrawingPosition,
                     self.currentDrawingPosition, self.color,
                     self.brushThickness)
            cv2.line(self.imgCanvas, self.startDrawingPosition,
                     self.currentDrawingPosition, self.color,
                     self.brushThickness)

            self.startDrawingPosition = self.currentDrawingPosition

        # for drawing
        # elif (fingers[1] and all(x == False for x in fingers[2:])):
        #     self.color = (255, 0, 255)
        #     if self.startDrawingPosition == (0, 0):
        #         self.startDrawingPosition = self.currentDrawingPosition

        #     cv2.circle(self.image, self.currentDrawingPosition, 15, self.color,
        #                cv2.FILLED)

        #     cv2.line(self.image, self.startDrawingPosition,
        #              self.currentDrawingPosition, self.color,
        #              self.brushThickness)
        #     cv2.line(self.imgCanvas, self.startDrawingPosition,
        #              self.currentDrawingPosition, self.color,
        #              self.brushThickness)

        #     self.startDrawingPosition = self.currentDrawingPosition

        # elif all(x == True for x in fingers):
        #     self.startDrawingPosition = self.currentDrawingPosition
        #     self.eraser = not self.eraser
        #     if self.eraser:
        #         self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        else:
            # for all finger close check
            # print(self.color)
            pass

    def checkShape(self, a):
        # (a[x][0] + 100 > i[0] and a[x][0] - 100 < i[0]) --> it check wheather it lies in less or more 100 in x axis
        # (a[x][1] + 100 > i[1] and a[x][1] - 100 < i[1]) --> it check wheather it lies in less or more 100 in y axis
        # a[x]!=i and a[x] in acopy -> it make sure that it doesn't delete itself and valid number(Present in acopy) is deleting the data.
        a = [x[0] for x in a]
        acopy = a
        for x in range(len(a) - 1):
            data = ([
                i for i in acopy
                if (a[x][0] + 100 > i[0] and a[x][0] - 100 < i[0]) and (
                    a[x][1] + 100 > i[1] and a[x][1] - 100 < i[1]) and (
                        a[x] != i and a[x] in acopy)
            ])
            if len(data) > 0:
                acopy = [i for i in acopy if i not in data]
        return acopy

    def drawContour(self, grayImage, mainImage):
        contours, hierarchy = cv2.findContours(grayImage, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)

        # print(contours)
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            data = approx.tolist()
            # print(data)
            # atleast checking it's having 2 cooridnates
            if (len(data) >= 2):
                points = self.checkShape(data)
                # count the number of points
                ls = len(points)
                # printing name of the Shape
                cv2.putText(self.image, "" * 15, (1100, 250),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (48, 49, 148), 2,
                            cv2.LINE_AA)
                cv2.putText(self.image,
                            ("line" if ls == 2 else
                             ("Triangle" if ls == 3 else
                              (" Sqaure" if ls == 4 else "Can't Identify"))),
                            (1100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (48, 49, 148), 2, cv2.LINE_AA)


if __name__ == '__main__':
    user1 = RedLight_GreenLight()
    user1.start()
    # @win.route('/video_feed')
    # def video_feed():
    #     return Response(user1.start(),
    #                     mimetype='multipart/x-mixed-replace; boundary=frame')

    # win.run(debug=True)

# #######################
# brushThickness = 8
# eraserThickness = 100
# ########################

# curr_light = False

# drawColor = (255, 0, 255)

# cap = cv2.VideoCapture(0)  # for single camera devices.
# cap.set(3, 1280)
# cap.set(4, 720)

# # motion part
# fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)
# frameCount = 0
# # end

# # if not working properly add detectioncon=0.85
# detector = htm.handDetector(maxHands=1)
# xp, yp = 0, 0
# imgCanvas = np.zeros((720, 1280, 3), np.uint8)
# earse = False

# resetTimer = 15

# while True:

#     if (resetTimer == 0):
#         resetTimer = random.randint(20, 35)
#         curr_light = not curr_light

#     else:
#         resetTimer -= 1

#     # 1. Import image
#     success, img = cap.read()
#     img = cv2.flip(img, 1)

#     # motion part
#     if not success:
#         break

#     frameCount += 1
#     fgmask = fgbg.apply(img)
#     count = np.count_nonzero(fgmask)
#     #print('Frame: %d, Pixel Count: %d' % (frameCount, count))
#     if curr_light == False:
#         if (frameCount > 1 and count > 5000):
#             print('Halu nkos bhava')
#             cv2.putText(img, 'Halu nkos bhava', (10, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
#                         cv2.LINE_AA)
#     # end
#     if curr_light == True:
#         cv2.putText(img, "GREEN ", (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                     (0, 255, 0), 2, cv2.LINE_AA)
#     else:

#         cv2.putText(img, "RED", (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                     (0, 0, 255), 2, cv2.LINE_AA)

#     # 2. Find Hand Landmarks
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img, draw=False)

#     if len(lmList) != 0:

#         # print(lmList[8][1:])  # coordinates of drawing

#         # tip of index and middle fingers
#         x1, y1 = lmList[8][1:]  # tip of index finger
#         x2, y2 = lmList[12][1:]  # tip of middle finger

#         # 3. Check which fingers are up
#         fingers = detector.fingersUp()
#         # print(fingers)

#         # if fingers[1] and fingers[2]:
#         #     print("Selection")
#         # if fingers[1] and fingers[2] == False:
#         #     print("Drawing")
#         # 4. If Selection Mode - Two finger are up

#         if fingers[1] and fingers[2]:
#             xp, yp = 0, 0
#         #     print("Selection Mode")
#         #     # # Checking for the click
#         # #     if 250 < x1 < 450:#if i m clicking at purple brush
#         #             header = overlayList[0]
#         #             drawColor = (255, 0, 255)
#         #         elif 550 < x1 < 750:#if i m clicking at blue brush
#         #             header = overlayList[1]
#         #             drawColor = (255, 0, 0)
#         #         elif 800 < x1 < 950:#if i m clicking at green brush
#         #             header = overlayList[2]
#         #             drawColor = (0, 255, 0)
#         #         elif 1050 < x1 < 1200:#if i m clicking at eraser
#         #             header = overlayList[3]
#         #             drawColor = (0, 0, 0)
#         #     cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

#         # # 5. If Drawing Mode - Index finger is up
#         if fingers[1] and fingers[2] == False:
#             cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
#             # print("Drawing Mode")
#             if xp == 0 and yp == 0:
#                 xp, yp = x1, y1  #check it purpose
#             if drawColor == (0, 0, 0):
#                 cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
#                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor,
#                          eraserThickness)

#             else:
#                 cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
#                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor,
#                          brushThickness)

#             xp, yp = x1, y1

#             # # Clear Canvas when all fingers are up
#         if all(x >= 1 for x in fingers):
#             earse = not earse
#             if earse:
#                 imgCanvas = np.zeros((720, 1280, 3), np.uint8)

#     # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
#     # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
#     imgInv = cv2.cvtColor(
#         cv2.threshold(cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY), 50, 255,
#                       cv2.THRESH_BINARY_INV)[1], cv2.COLOR_GRAY2BGR)
#     img = cv2.bitwise_and(img, imgInv)
#     img = cv2.bitwise_or(img, imgCanvas)

#     # Setting the header image for changing color n all
#     # img[0:125, 0:1280] = header
#     # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

#     cv2.imshow("Image", img)

#     # Exit button "ESC"
#     k = cv2.waitKey(1) & 0xff
#     if k == 27:
#         break
