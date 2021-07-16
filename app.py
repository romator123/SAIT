from flask import Flask, render_template, url_for, request, redirect
import face_recognition
import glob2 as gb
import cv2
import numpy as np
import os
import pymysql

connection = pymysql.connect(host="192.168.100.121",user="abak2000",passwd="romator123",database="register" )


app = Flask(__name__)

nameid = []
authorised = False


@app.route('/')
def index():
    if authorised:
        print('HELL YEAH!!!')
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
        rows = cursor.fetchall()
        connection.commit()

        global nameid
        nameid = list(rows)
        for i in range(len(nameid)):
            nameid[i] = str(nameid[i])[1:-2]

        return redirect('/face_check')
    else:
        return render_template('fio_input.html')


@app.route('/face_check', methods=['POST', 'GET'])
def face_check():
    video_capture = cv2.VideoCapture(0)
    #img_path = gb.glob(r'C:\PythonProjects\SAIT-Back\SAIT-Back\webcam/*.jpg')
    img_path = gb.glob(r'\home\dev\github\photo/*.jpg')
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


if __name__ == '__main__':
    app.run(debug=True)

