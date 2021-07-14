from flask import Flask, render_template, url_for, request, redirect,Response
import cv2
import numpy as np
import os
import pymysql
from camera import  VideoCamera

#cam = cv2.VideoCapture(1,cv2.CAP_DSHOW)
#cam = cv2.VideoCapture('rtsp://192.168.0.12:8080/h264_ulaw.sdp',cv2.CAP_DSHOW)
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades +'Cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
video_stream=VideoCamera()
#recognizer.read('C:\\Users\\tcach\\PycharmProjects\\WEBCAM\\trainer\\trainer.yml')
#cascadePath = "Cascades\\haarcascade_frontalface_default.xml"
recognizer.read('trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX
connection = pymysql.connect(host="192.168.100.121",user="abak2000",passwd="romator123",database="register" )


app = Flask(__name__)

nameid=0




@app.route('/')
def index():
    return render_template('index.html')




@app.route('/fio_input', methods=['POST', 'GET'])
def fio_input():

    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        middle_name = request.form['middle_name']


        cursor = connection.cursor()
        cursor.execute("Select idregister  from register WHERE surname=(%s) AND name=(%s) AND middle_name=(%s) ",
                       (surname, name, middle_name))
        rows = cursor.fetchone()
        for row in rows:
            print(row)
        connection.commit()

        global nameid
        nameid = int(rows[0])


        return redirect('/face_check')
    else:
        return render_template('fio_input.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    count=0
    face_id=0
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        middle_name = request.form['middle_name']
        cursor = connection.cursor()
        sql = "INSERT INTO register (name, surname,middle_name) VALUES (%s, %s, %s)"
        val = (name, surname, middle_name)
        cursor.execute(sql, val)
        cursor.execute("Select idregister  from register WHERE surname=(%s) AND name=(%s) AND middle_name=(%s) ",
                       (surname, name, middle_name))
        rows = cursor.fetchone()
        for row in rows: print(row)
        face_id = int(rows[0])
        connection.commit()
        connection.close()
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite(r"C:/User/tcach/PycharmProject/WEBCAM/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30:  # Take 30 face sample and stop video
                break
            cam.release()
            cv2.destroyAllWindows()
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/face_check', methods=['POST', 'GET'])
def face_check():
    return render_template('face_check.html')

def gen_frames(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def face_check():
    return render_template('face_check.html')

        ##if (id_to_check == face_id)
            ##return redirect('/info')
    #else:
        #return render_template('face_check.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

