import base64
from configparser import Interpolation
import cvlib as cv
import cv2
import socketio
import time
import base64
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.models import load_model

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
# 영상 처리 서버

# 모델 import
model = load_model('../../visionML/model_M1_3_Densenet.h5')

# 소켓 연결
videoSocket = socketio.Client()
videoSocket.connect('http://localhost:6666')  # 서버 주소
frame = 0

# 비디오 디코딩 함수

@videoSocket.on('connection')
def connection():
    print('connected to io server')

#@videoSocket.event
def videoDecode(data):
    data = cv2.imdecode(np.frombuffer(
        base64.b64decode(data), dtype='uint8'), cv2.IMREAD_COLOR)
    global frame
    frame = data

@videoSocket.on('videoProcess')
def isMasked(data):
    with tf.device('/GPU:0'):
        videoDecode(data)
        face, confidence = cv.detect_face(frame)

        for i, f in enumerate(face):
            (headX, headY) = f[0], f[1]
            (tailX, tailY) = f[2], f[3]
            if 0 <= headX <= 640 and 0 <= tailX <= 640 and 0 <= headY <= 480 and 0 <= tailY <= 480:
                face_only = frame[headY: tailY, headX: tailX]

                face_resized = cv2.resize(
                    face_only, (256, 256), interpolation=cv2.INTER_AREA)

                i = img_to_array(face_resized)
                i = np.expand_dims(i, axis=0)
                i = preprocess_input(i)

                prediction = model.predict(i)
                print(prediction)
                bestPrediction = np.argmax(prediction)
                encoded_frame = ''
                if bestPrediction == 0 :  # 마스크 착용
                    print('masked')
                elif bestPrediction == 1 or bestPrediction == 2:  # 마스크 부분착용(턱스크 등)
                    print('턱스크')
                    res, ef = cv2.imencode('.jpg', face_only, encode_param)
                    encoded_frame = base64.b64encode(ef)
                    videoSocket.emit('partialMask', encoded_frame)
                elif bestPrediction == 3:  # 마스크 미착용 승객
                    print('noMask')
                    res, ef = cv2.imencode('.jpg', face_only, encode_param)
                    encoded_frame = base64.b64encode(ef)
                    videoSocket.emit('noMask', encoded_frame)
                    #cv2.imshow('noMASKInFRAME', frame)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()

'''
with tf.device("/GPU:0"):
    while(True):
        videoSocket.on('videoProcess', videoDecode)
        face, confidence = cv.detect_face(face)

        for i, f in enumerate(frame):
            (headX, headY) = f[0], f[1]
            (tailX, tailY) = f[2], f[3]

        if 0 <= headX <= 640 and 0 <= tailX <= 640 and 0 <= headY <= 480 and 0 <= tailY <= 480:
            face_only = frame[headY: tailY, headX: tailX]

            face_resized = cv2.resize(
                face_only, (256, 256), interpolation=cv2.INTER_AREA)

            i = img_to_array(face_resized)
            i = np.expand_dims(i, axis=0)
            i = preprocess_input(i)

            prediction = model.predict(i)

            if prediction < 1.5:  # 마스크 착용
                continue
            elif prediction >= 1.5 and prediction < 3.5:  # 마스크 부분착용(턱스크 등)
                res, ef = cv2.imencode('.jpg', face_only, encode_param)
                encoded_frame = base64.encode(ef)
                videoSocket.emit('partialMask', encoded_frame)
            elif prediction >= 3.5:  # 마스크 미착용 승객
                res, ef = cv2.imencode('.jpg', face_only, encode_param)
                encoded_frame = base64.encode(ef)
                videoSocket.emit('noMask', encoded_frame)
                cv2.imshow('noMASKInFRAME', frame)
        if cv2.waitkey(1) > 0:
            break
'''
videoSocket.wait()
videoSocket.disconnect()
