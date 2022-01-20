from flask import Flask, render_template, Response
import cv2
import numpy as np
from VirtualPainter import RedLight_GreenLight

win = Flask(__name__)


def gen_frames():
    # main class object
    user = RedLight_GreenLight()

    while np.any(user.start()):
        # this will return frame of image
        frame = user.start()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
               )  # concat frame one by one and show result


@win.route('/')
def index():
    return render_template('index.html')


@win.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    win.run(debug=True, port=8000)
