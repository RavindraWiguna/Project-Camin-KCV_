from io import BytesIO
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from PIL import Image
import numpy as np
import cv2
import base64
from tensorflow import keras
from mtcnn import MTCNN

app = Flask(__name__)
socket_io = SocketIO(app)

#LOGIC AND OPEN CV FUNC
#load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = keras.models.load_model('./model/')
color = ((0, 255, 0), (0, 0, 255))
# [1, 0] --> pake masker
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# mtcnnDetector = MTCNN()
#=================================================WEB WEB WEB WEB=====================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/detect/", methods=["POST", "GET"])
def detect():
    return render_template("detect.html")


@socket_io.on('image')
def image(data_image):
    # print("HEREHEHREHREHRHEHREHRE")
    b = BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)
    
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    #do python ml stuff to frame here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5) #src, scale factor (multipiter to be pyramid (shrink)), minNeighbohr (rectangle overlap for AC)
    
    #mtcnn ver
    # mtFaces = mtcnnDetector.detect_faces(frame)

    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # faceBox = frame[x:x+w, y:y+h]
        faceBox = frame[y:y+h, x:x+w]
        # faceHSV = cv2.cvtColor(faceBox, cv2.COLOR_BGR2HSV)
        # faceHSV[:, :, 2] += 50
        # faceHSV[:, :, 2] = min(255, faceHSV[:, :, 2])
        # frame = faceBox
        # cv2.imshow('work', faceBox)
        # faceBox = cv2.cvtColor(faceHSV, cv2.COLOR_HSV2BGR)
        faceBox = cv2.resize(faceBox, (128, 128))
        faceBox = faceBox.reshape((1, 128, 128, 3))
        faceBox = faceBox.astype('float32')
        faceBox /=255
        pred = model.predict(faceBox)[0]
        # pred = np.argmax(pred)
        if(pred[1] > 0.09):
            pred = 1
        else:
            pred = 0
        cv2.rectangle(frame, (x, y), (x+w, y+h), color[pred], 2)
        # print(f'{pred[0]} vs {pred[1]}')

    # for face in mtFaces:
        # x, y, w, h = face['box']
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # cv2.imshow('test', frame)
    # cv2.waitKey(0)
    # print("here")
    # frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]
    stringData = base64.b64encode(imgencode).decode('utf-8')
    emit('response_back', f'data:image/jpg;base64,{stringData}')
    


if __name__ == "__main__":
    # socket_io.run(app)
    app.run()

