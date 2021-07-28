from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.sql import and_, or_
import cv2
import numpy as np
import os
import pymysql


db = SQLAlchemy()
app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', (f'mysql+pymysql://abak2000:romator123@192.168.100.121/register'))


class User(db.Model):
    __tablename__ = "register"
    idregister = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.id


db.init_app(app)


nameid = []
authorised = False


@app.route('/')
def index():
    if authorised:
        print('HELL YEAH!!!')
    return render_template('index.html')
u = {"0": {"kab": "1", "time": "18:00", "surname": "adasd", "name": "asdasdd"}, "1": {"kab": "1", "time": "19:00", "surname": "adasd", "name": "asdasdd"}, }
k = {"0": {"kab": "2", "time": "13:00", "surname": "hjkhjk", "name": "asdasdd"}, "1": {"kab": "2", "time": "18:00", "surname": "adasd", "name": "asdasdd"}, }

@app.route('/show1', methods=['PUT'])
def show1():
    cabinet = request.args['button']
    if request.method == 'PUT':
        if int(cabinet) == 1:
            return jsonify(x=u)
        elif int(cabinet) == 2:
            return jsonify(x=k)
    return render_template('show.html')
@app.route('/show')
def show():
    return render_template('show.html')

@app.route('/register', methods=['POST', 'GET', 'PUT'])
def register():
    if request.method == 'POST':
        connection = pymysql.connect(host="192.168.100.121", user="abak2000", passwd="romator123", database="register")
        surname = request.form['surname']
        name = request.form['name']
        middle_name = request.form['middle_name']

        cursor = connection.cursor()
        cursor.execute("Select idregister  from register WHERE surname=(%s) AND name=(%s) AND middle_name=(%s) ",
                       (surname, name, middle_name))
        rows = cursor.fetchall()
        tempnameid = list(rows)
        tempnameid = str(nameid)[1:-2]
        cursor.execute("INSERT INTO records (iduser, cabinet, time) VALUES(%s, %s, %s) ",
                       (int(tempnameid), int(request.form['cab']), request.form['time']))
        connection.close()
        print('ПЕРЕВОЖУ ДИНЕРРО НА ИХ СЧЁТИК, ПУСТЬ ОПТИМА ПО-ДА-ВИ-ТСЯ')
        return redirect('/')

    elif request.method == 'PUT':
        times = {'10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'}
        connection = pymysql.connect(host="192.168.100.121", user="abak2000", passwd="romator123", database="register")
        cursor = connection.cursor()
        cabinet = request.args['button']
        cursor.execute("SELECT format(time, 'hh:mm:ss') from records WHERE cabinet=(%s) group by time ", int(cabinet))
        rows = cursor.fetchall()
        rows = list(rows)
        for i in range(len(rows)):
            rows[i] = str(rows[i])[2:4] + ':' + str(rows[i])[-8] + str(rows[i])[-6]
        rows = set(rows)
        times = list(times - rows)
        times.sort()
        timedict = {}
        for i in range(len(times)):
            timedict.update({i: {'id': i, 'time': times[i]}})
        return jsonify(z=timedict)

    else:
        return render_template('register.html')


@app.route('/fio_input', methods=['POST', 'GET'])
def fio_input():

    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        middle_name = request.form['middle_name']

        connection = pymysql.connect(host="192.168.100.121", user="abak2000", passwd="romator123", database="register")
        cursor = connection.cursor()
        cursor.execute("Select idregister  from register WHERE surname=(%s) AND name=(%s) AND middle_name=(%s) ",
                       (surname, name, middle_name))
        rows = cursor.fetchall()
        connection.commit()

        global nameid
        nameid = list(rows)
        for i in range(len(nameid)):
            nameid[i] = str(nameid[i])[1:-2]
        connection.close()
        return redirect('/face_check')
    else:
        return render_template('fio_input.html')


@app.route('/face_check', methods=['POST', 'GET'])
def face_check():
    video_capture = cv2.VideoCapture(0)
    img_path = gb.glob(r'C:\PythonProjects\SAIT-Back\SAIT-Back\webcam/*.jpg')
    known_face_names = []
    known_face_encodings = []

    for i in img_path:
        picture_name = i.replace('/*.jpg', '')
        picture_newname = picture_name.replace('.jpg', '')
        if picture_newname[picture_newname.rfind('\\')+1:] in nameid:
            someone_img = face_recognition.load_image_file(i)
            someone_face_encoding = face_recognition.face_encodings(someone_img)[0]
            known_face_names.append(picture_newname)
            known_face_encodings.append(someone_face_encoding)
        someone_img = []
        someone_face_encoding = []

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        global authorised

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for i in face_encodings:
                match = face_recognition.compare_faces(known_face_encodings, i, tolerance=0.39)
                if True in match:
                    match_index = match.index(True)
                    authorised = True
                    name = "match"
                    # To print name
                    print(known_face_names[match_index])
                else:
                    match_index = match.index(False)
                    name = "unknown"
                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            if match_index:
                answer = known_face_names[match_index][known_face_names[match_index].rfind('\\') + 1:]
                cv2.putText(frame, answer, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if (cv2.waitKey(1) & 0xFF == ord('q')) or authorised:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return redirect('/')


@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/info_new', methods=['POST'])
def info_new():
    connection = pymysql.connect(host="192.168.100.121", user="abak2000", passwd="romator123", database="register")
    cursor = connection.cursor()
    cursor.execute("Select * from register order by surname")
    rows = cursor.fetchall()
    connection.close()
    user = list(rows)
    userdict = {}
    for i in range(len(user)):
        userdict.update({user[i][0]: {'name': user[i][1], 'surname': user[i][2], 'middle_name': user[i][3]}})
    return jsonify(x=userdict)


if __name__ == '__main__':
    app.run(debug=True)

