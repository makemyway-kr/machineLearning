import base64
from itsdangerous import base64_encode
import cv2
import socketio
import time
#영상 전송 서버(단속 현장)

#소켓 연결
videoSocket = socketio.Client()
videoSocket.connect('') #서버 주소

#영상 input
videoStream = cv2.VideoCapture(0)
videoStream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
videoStream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while(True):
    time.sleep(0.5) #0.5초마다 비디오 인풋전송
    status , frame = videoStream.read()

    if not status:
        print("영상 입력이 없음")
        break
    res , frame = cv2.imencode('.jpg',frame , encode_param)
    b64_encoded = base64.encode(frame)
    videoSocket.emit('videoIncoming',b64_encoded)
videoSocket.disconnect()

