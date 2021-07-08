from flask import Flask, render_template, url_for, request, redirect
import cv2
import numpy as np
import os
import pymysql


cam = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX
connection = pymysql.connect(host="192.168.200.121",user="abak2000",passwd="romator123",database="abakdb" )


app = Flask(__name__)
'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)'''
id_to_check = 0
nameid=0


'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
    return '<User %r>' % self.id
'''

@app.route('/')
def index():
    return render_template('index.html')


'''''@app.route('/info')
def info():
    user = User.query.filter(User.id == id_to_check)
    return render_template('info.html', user=user)
'''

@app.route('/fio_input', methods=['POST', 'GET'])
def fio_input():

    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        middle_name = request.form['middle_name']

        '''user = User(surname=surname, name=name, middle_name=middle_name)'''
        #user = User.query.filter(User.surname == surname, User.name == name, User.middle_name == middle_name).all()
        #global id_to_check
        #id_to_check = int(user[0].id)
        cursor = connection.cursor()
        cursor.execute("Select idregister  from register WHERE surname=(%s) AND name=(%s) AND middle_name=(%s) ",
                       (surname, name, middle_name))
        rows = cursor.fetchone()
        for row in rows: print(row)
        connection.commit()

        connection.close()

        nameid=row
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
        face_id=row
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
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

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
    if request.method == 'POST':

        id = 0

        ### names related to ids: example ==> Marcelo: id=1,  etc
        #names = ['None', 'Roman', 'Paula', 'Ilza', 'Z', 'W']

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video widht
        cam.set(4, 480)  # set video height

        ### Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (nameid==id):
                    idname='Compleate'
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    idname = 'Warning'
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(idname), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('camera', img)

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()

        ##if (id_to_check == face_id)
            ##return redirect('/info')
    else:
        return render_template('face_check.html')


if __name__ == '__main__':
    app.run(debug=True)
