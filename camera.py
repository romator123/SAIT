import cv2
import time
class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://192.168.201.121:8080/h264_ulaw.sdp')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()