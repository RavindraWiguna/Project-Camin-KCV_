from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__)

#LOGIC AND OPEN CV FUNC
listCam = []
didCheck = False
camId = 0

def change():
    # print("changing")
    global camId
    camId+=1
    camId %= len(listCam)

def generateFrame():
    try:
        cap = cv2.VideoCapture(listCam[camId])
    except IndexError:
        print(f'cam list len: {len(listCam)}, camId: {camId}')
        cap = cv2.VideoCapture(0)
        if(cap.isOpened()):
            print("ABLE TO OPEN")
        else:
            print("cant even run capture 0")
    while True:
        success, frame = cap.read()
        if(not success):
            break
        else:
            '''did tensorflow here'''
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route("/")
def home():
    global didCheck
    if(not didCheck):
        for i in range(0, 10):
            cap = cv2.VideoCapture(i)
            if(not cap.isOpened()):
                continue
            listCam.append(i)

    # print(listCam)
    return render_template("home.html")

@app.route("/detect/", methods=["POST", "GET"])
def detect():
    if(request.method=='POST'):
        if("changeCam" in request.form):
            change()
    return render_template("detect.html")


@app.route('/video')
def video():
    return Response(generateFrame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    # getAvailCam()
    app.run(debug=True)

