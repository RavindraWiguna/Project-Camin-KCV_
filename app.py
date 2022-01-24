import base64
from io import StringIO, BytesIO
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
import cv2
from PIL import Image, UnidentifiedImageError
import numpy as np

app = Flask(__name__)
socket_io = SocketIO(app)   
b64_src = 'data:image/jpg;base64,'
#LOGIC AND OPEN CV FUNC
# listCam = []
# didCheck = False
# camId = 0

# def change():
#     # print("changing")
#     global camId
#     if(len(listCam > 0)):
#         camId+=1
#         camId %= len(listCam)

# def generateFrame():
#     try:
#         cap = cv2.VideoCapture(listCam[camId])
#     except IndexError:
#         print(f'cam list len: {len(listCam)}, camId: {camId}')
#         cap = cv2.VideoCapture(0)
#         if(cap.isOpened()):
#             print("ABLE TO OPEN")
#         else:
#             print("cant even run capture 0")
#     while True:
#         success, frame = cap.read()
#         if(not success):
#             break
#         else:
#             '''did tensorflow here'''
            
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             yield(b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#=================================================WEB WEB WEB WEB=====================

@app.route("/")
def home():
    # global didCheck
    # if(not didCheck):
    #     didCheck = True
    #     for i in range(0, 10):
    #         cap = cv2.VideoCapture(i)
    #         if(not cap.isOpened()):
    #             continue
    #         listCam.append(i)

    # print(listCam)
    return render_template("home.html")

@app.route("/detect/", methods=["POST", "GET"])
def detect():
    # if(request.method=='POST'):
    #     if("changeCam" in request.form):
    #         # change()
    #         pass
    return render_template("detect.html")


# @app.route('/video')
# def video():
#     return Response(image(),mimetype='multipart/x-mixed-replace; boundary=frame')


@socket_io.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)
    b = BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)
    
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    # frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]
    stringData = base64.b64encode(imgencode).decode('utf-8')
    emit('response_back', f'{b64_src}{stringData}')
    


if __name__ == "__main__":
    app.run(debug=True)

