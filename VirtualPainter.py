import base64
from distutils.log import debug
from io import StringIO
import io
import sys
import traceback
from turtle import width
from PIL import Image
import cv2
from flask import Flask, Response, render_template, jsonify, make_response
from matplotlib.pyplot import contour
import numpy as np
import time
import os
import HandTrackingModule as htm
import random
import socketio
import numpy as np
# from trying import SerializableGenerator
from flask_socketio import SocketIO, send, emit
import imutils
import sys
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Rules for drawing
# to move use make sure your palm is open
# to draw make sure just your index finger is open
# to erase make sure just your thumn and index finger is open
####
#########
# put startDrawing cursor to 0 when ever our finger position changes from up to down or anything if constant keep it same (for later ignore for now)
##
win = Flask(__name__)
sio = SocketIO(win, cors_allowed_origins="*")
# sio.init_app(win, cors_allowed_origins="*")

# @win.route('/')
# def index():
#     return render_template('index.html')


class RedLight_GreenLight():

    def __init__(self):
        self.color = (255, 0, 255)  # drawColor varaible
        self.brushThickness = 20
        self.eraserThickness = 65
        self.currentLight = False
        self.resetTimer = 15
        self.eraser = False
        self.points = 0
        self.isDrawn = False
        self.shapes = "FUck off"  #transfer this variable
        self.startDrawingPosition = (0, 0)  # storing co-ordinate value , xp,yp
        self.currentDrawingPosition = (0, 0)  # x1,y1 variable

    def start(self, frame):
        # cam = self.getCAM()
        # self.initializing()

        self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        frameCount = 0
        while True:
            self.changeLight()

            # success, self.image = cam.read()
            self.image = frame  #suspect
            self.image = cv2.resize(self.image, (1280, 720))
            # if not success:
            #     break

            self.image = cv2.flip(self.image, 1)

            frameCount += 1
            fgmask = self.motion.apply(self.image)
            count = np.count_nonzero(fgmask)
            # stop = self.alertWarning(frameCount, count,cam)
            stop = 0

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
            # self.gray = cv2.resize(self.gray, (1280, 720))
            imgInv = cv2.cvtColor(
                cv2.threshold(self.gray, 50, 255, cv2.THRESH_BINARY_INV)[1],
                cv2.COLOR_GRAY2BGR)
            print("imagcanvas", self.imgCanvas.shape)
            print("imgInverse", imgInv.shape)
            print("image", self.image.shape)
            self.image = cv2.bitwise_and(self.image, imgInv)
            self.image = cv2.bitwise_or(self.image, self.imgCanvas)

            # if (not np.all((self.imgCanvas == np.zeros(
            #     (720, 1280, 3), np.uint8)))):
            #     self.imgCanny = cv2.Canny(gray, 23, 20)
            #     kernel = np.ones((5, 5))
            #     imgDil = cv2.dilate(self.imgCanny, kernel, iterations=1)
            #     self.drawContour(imgDil, self.imgCanny)
            # cv2.imshow("Drawing", self.imgCanny)

            # cv2.imshow("Image", self.image)

            # _, buffer = cv2.imencode('.jpg', self.image)
            # self.image = buffer.tobytes()
            # self.image = buffer
            # for exiting purpose
            k = cv2.waitKey(1) & 0xff
            if k == 27 or stop == 1:
                # cam.release()
                # cv2.destroyAllWindows()
                break

            ####
            # transer count veriable to our index.html page
            count += 1
            if (count % self.fps == 0):
                # if this happen you should pass the count veriable to our website
                count = 0
                ## try to pass with the below yield if multiple parameter is possible passing with response.
                pass

            _, imgencode = cv2.imencode('.jpg', self.image)
            stringData = base64.b64encode(imgencode).decode('utf-8')
            b64_src = 'data:image/jpg;base64,'
            frame = b64_src + stringData
            # data = json.JSONEncoder().iterencode(
            #     SerializableGenerator(stringData))
            return frame
            # emit('response_back', frame)

            # print(frame)
            # break
            # yield jsonify(frame)
        # it'll return self.image toflask app

        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + self.image + b'\r\n')

    def initializing(self):
        self.hand = htm.handDetector(maxHands=1)  # detector variable
        self.motion = cv2.createBackgroundSubtractorMOG2(300, 400,
                                                         True)  # fgbh variable

    def getCAM(self):
        cap = cv2.VideoCapture(0)  # for single camera devices.
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        cap.set(3, 1280)
        cap.set(4, 720)
        return cap

    def changeLight(self):
        if (self.resetTimer == 0):
            self.resetTimer = random.randint(10, 20) * 30  # 30 tha
            self.currentLight = not self.currentLight
        else:
            self.resetTimer -= 1

    def showState(self):
        cv2.putText(self.image, ("GREEN" if self.currentLight else "RED"),
                    (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    ((0, 255, 0) if self.currentLight else
                     (0, 0, 255)), 2, cv2.LINE_AA)

    def alertWarning(self, frameCount, count, camera):
        #print('Frame: %d, Pixel Count: %d' % (frameCount, count))
        if self.currentLight == False:
            if (frameCount > 1 and count > 15000):
                # print('Halu nkos bhava')

                cv2.putText(self.image, 'Dont move too much', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            cv2.LINE_AA)

                return 1
            else:
                return 0
        else:
            return 0

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

        else:
            # for all finger close check
            pass

    detect_shape = ""

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
                cv2.putText(
                    self.image, "line" if ls == 2 else
                    ("Tringle" if ls == 3 else
                     ("Square" if ls == 4 else "Try Again")), (1100, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (48, 49, 148), 2, cv2.LINE_AA)

                self.detect_shape = "line" if ls == 2 else (
                    "Tringle" if ls == 3 else
                    ("Square" if ls == 4 else "Try Again"))

                print(ls)
                if (ls in list(range(1, 4)) and not self.isDrawn):
                    self.points += 1
                    self.isDraw = True


if __name__ == '__main__':
    user1 = RedLight_GreenLight()
    # user1.start()

    @win.route('/video_feed')
    def video_feed():
        return Response(user1.start(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @win.route('/getPoints')
    def getPoints():
        # return str(user1.points)
        return render_template("func.html", values=str(user1.points))

    @win.route('/getShapes')
    def getShapes():
        return render_template("getShapes.html",
                               shapesValues=str(user1.shapes))

    @win.route('/')
    def index():
        return render_template('index.html', values=user1.points)

    @sio.on("message")
    def sending(message):
        print("hladjfdspafpsdahf ")
        # print(sid)
        print(message)

    def changeLight(resetTimer, currentLight):
        if (resetTimer == 0):
            resetTimer = random.randint(10, 20) * 30  # 30 tha
            currentLight = not currentLight
        else:
            resetTimer -= 1
        return resetTimer, currentLight

    def checkShape(a):
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

    def drawContour(grayImage, frame):
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
                points = checkShape(data)
                # count the number of points
                ls = len(points)
                # printing name of the Shape
                cv2.putText(frame, "" * 15, (1100, 250),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (48, 49, 148), 2,
                            cv2.LINE_AA)
                cv2.putText(
                    frame, "line" if ls == 2 else
                    ("Tringle" if ls == 3 else
                     ("Square" if ls == 4 else "Try Again")), (1100, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (48, 49, 148), 2, cv2.LINE_AA)

                detect_shape = "line" if ls == 2 else (
                    "Tringle" if ls == 3 else
                    ("Square" if ls == 4 else "Try Again"))

                print(ls)
                if (ls in list(range(1, 4))):
                    points += 1
                return frame

    @sio.on('image')
    def image(data_image):
        try:
            # sbuf = StringIO()
            # sbuf.write(data_image)
            # print(data_image)

            # decode and convert into image
            b = io.BytesIO(base64.b64decode(data_image))
            pimg = Image.open(b)

            ## converting RGB to BGR, as opencv standards
            frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
            # print(frame)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Process the image frame
            frame = imutils.resize(frame, width=1280, height=720)
            # frame = cv2.flip(frame, 1)
            # stringData = user1.start(frame)
            # frame2 = cv2.flip(frame2, 1)
            imgencode = cv2.imencode('.jpg', frame)[1]

            # base64 encode
            stringData = base64.b64encode(imgencode).decode('utf-8')
            b64_src = 'data:image/jpg;base64,'
            stringData = b64_src + stringData
            # print(stringData)
            # emit('response_back', next(user1.start(frame)))
            # for i in user1.start(frame):
            #     emit('response_back', i)

            # user1.start(frame)
            # sys.exit()
            # emit the frame back

            # # motion part
            fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)
            # frameCount = 0
            # end

            # if not working properly add detectioncon=0.85
            detector = htm.handDetector(maxHands=1)
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)
            earse = False
            currentLight = False
            brushThickness = 20
            eraserThickness = 65
            if 'shapes' not in locals():
                shapes = None

            # checking if it exist or not
            if 'points' not in locals():
                points = 0

            if 'resetTimer' not in locals():
                resetTimer = 15

            if 'startDrawingPosition' not in locals():
                startDrawingPosition = (0, 0)

            if 'currentDrawingPosition' not in locals():
                currentDrawingPosition = (0, 0)

            if 'color' not in locals():
                color = (255, 0, 255)

            ####
            framecount = 0
            while True:
                resetTimer, currentLight = changeLight(resetTimer,
                                                       currentLight)
                framecount += 1
                fgmask = fgbg.apply(frame)

                count = np.count_nonzero(fgmask)
                #     #print('Frame: %d, Pixel Count: %d' % (frameCount, count))
                if currentLight == False:
                    if (framecount > 1 and count > 15000):
                        # print('Halu nkos bhava')
                        cv2.putText(frame, 'Dont move too much', (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                    2, cv2.LINE_AA)
                        stop = 1
                    else:
                        stop = 0
                else:
                    stop = 0
                # end

                ## This will display word on frame
                cv2.putText(frame, ("GREEN" if currentLight else "RED"),
                            (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            ((0, 255, 0) if currentLight else
                             (0, 0, 255)), 2, cv2.LINE_AA)

                #     # 2. Find Hand Landmarks
                frame = detector.findHands(frame)
                lmList, bbox = detector.findPosition(frame, draw=False)

                if len(lmList) != 0:
                    # tip of index and middle fingers
                    currentDrawingPosition = lmList[8][
                        1:]  # tip of index finger

                    # 3. Check which fingers are up
                    fingers = detector.fingersUp()

                    #self.modes
                    if all(x == True for x in fingers):
                        startDrawingPosition = 0, 0
                        if (not np.all((imgCanvas == np.zeros(
                            (720, 1280, 3), np.uint8)))):
                            imgCanny = cv2.Canny(imgGray, 23, 20)
                            kernel = np.ones((5, 5))
                            imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
                            frame = drawContour(imgDil, imgCanny)

                    # new Erasing
                    elif fingers[0] and fingers[1]:
                        if startDrawingPosition == (0, 0):
                            startDrawingPosition = currentDrawingPosition
                        color = (0, 0, 0)
                        cv2.circle(image, currentDrawingPosition, 15, color,
                                   cv2.FILLED)

                        cv2.line(image, startDrawingPosition,
                                 currentDrawingPosition, color,
                                 eraserThickness)
                        cv2.line(imgCanvas, startDrawingPosition,
                                 currentDrawingPosition, color,
                                 eraserThickness)

                        startDrawingPosition = currentDrawingPosition

                    # new Drawing
                    elif fingers[1]:
                        color = (255, 0, 255)
                        if startDrawingPosition == (0, 0):
                            startDrawingPosition = currentDrawingPosition

                        cv2.circle(image, currentDrawingPosition, 15, color,
                                   cv2.FILLED)

                        cv2.line(image, startDrawingPosition,
                                 currentDrawingPosition, color, brushThickness)
                        cv2.line(imgCanvas, startDrawingPosition,
                                 currentDrawingPosition, color, brushThickness)

                        startDrawingPosition = currentDrawingPosition

                    else:
                        # for all finger close check
                        pass

                imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
                # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
                imgInv = cv2.cvtColor(
                    cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)[1],
                    cv2.COLOR_GRAY2BGR)
                frame = cv2.bitwise_and(frame, imgInv)
                frame = cv2.bitwise_or(frame, imgCanvas)

                k = cv2.waitKey(1) & 0xff
                if k == 27 or stop == 1:
                    break

                ####
                # transer count veriable to our index.html page
                count += 1
                if (count % 22 == 0):
                    # if this happen you should pass the count veriable to our website
                    count = 0
                    ## try to pass with the below yield if multiple parameter is possible passing with response.
                    pass

                _, imgencode = cv2.imencode('.jpg', frame)
                stringData = base64.b64encode(imgencode).decode('utf-8')
                b64_src = 'data:image/jpg;base64,'
                frame = b64_src + stringData

                emit('response_back', frame)

            # emit('response_back', user1.start(frame))
            # emit('response_back', stringData)
            # emit(
            #     'response_back',
            #     Response(user1.start(stringData),
            #              mimetype='multipart/x-mixed-replace; boundary=frame'))
            pass
        except Exception as e:
            # traceback.print_exc()

            print("Zindagi jhand baa fir bhi ghamand")
            pass

    @sio.on("connect")
    def connecting():
        print("Client connected")

    # win.run(debug=True, port=80)
    sio.run(win, port=80, debug=True)

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
