import cv2
import numpy as np

#NOW IT'S a scrap we can use for referencing purpose

# import VirtualPainter as vp


# Video Capture
# capture = cv2.VideoCapture(0)
def trackingUser(video):
    # capture = cv2.VideoCapture(0)
    capture = video

    # History, Threshold, DetectShadows
    # fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
    fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

    # Keeps track of what frame we're on
    frameCount = 0

    while (1):
        # Return Value and the current frame
        ret, frame = capture.read()

        #  Check if a current frame actually exist
        if not ret:
            break

        frameCount += 1
        # Resize the frame
        resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

        # Get the foreground mask
        fgmask = fgbg.apply(resizedFrame)

        # Count all the non zero pixels within the mask
        count = np.count_nonzero(fgmask)

        print('Frame: %d, Pixel Count: %d' % (frameCount, count))

        # Determine how many pixels do you want to detect to be considered "movement"
        # if (frameCount > 1 and cou`nt > 5000):
        if (frameCount > 1 and count > 5000):
            print('Warning')
            cv2.putText(resizedFrame, 'Warning', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                        cv2.LINE_AA)

        cv2.imshow('Frame', resizedFrame)
        cv2.imshow('Mask', fgmask)

        # k = cv2.waitKey(1) & 0xff
        # if k == 27:
        #     break


# capture.release()
# cv2.destroyAllWindows()