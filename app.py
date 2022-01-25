from io import StringIO, BytesIO
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from PIL import Image
import numpy as np
import cv2
import base64

app = Flask(__name__)
socket_io = SocketIO(app)

#LOGIC AND OPEN CV FUNC
#load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#=================================================WEB WEB WEB WEB=====================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/detect/", methods=["POST", "GET"])
def detect():
    return render_template("detect.html")


@socket_io.on('image')
def image(data_image):
    b = BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)
    
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    #do python ml stuff to frame here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 3) #src, scale factor (multipiter to be pyramid (shrink)), minNeighbohr (rectangle overlap for AC)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)


    # frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]
    stringData = base64.b64encode(imgencode).decode('utf-8')
    emit('response_back', f'data:image/jpg;base64,{stringData}')
    


if __name__ == "__main__":
    # socket_io.run(app)
    app.run()

