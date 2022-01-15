from flask import Flask, render_template, Response
import cv2
win = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read() #Read the camera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  #concat frame one by one and show result

@win.route('/')
def index():
    return render_template('index.html')

@win.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    win.run(debug=True, port=8000)