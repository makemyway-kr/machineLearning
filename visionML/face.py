import cvlib as cv
import cv2
import os
from glob import glob
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
def image_load_and_face(imagefileDir):
    images = glob(r'D:\vision_data\data1\images\*.jpg')
    count = 0
    for i in images:
        img = cv2.imread(i)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 얼굴 찾기
        faces, confidences = cv.detect_face(img)

        '''for (x, y, x2, y2), conf in zip(faces, confidences):
        		# 확률 출력하기
            cv2.putText(img, str(conf), (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        		# 얼굴위치 bbox 그리기
            cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)

        # 영상 출력
        cv2.imshow('image', img)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        print(i)
        for idx , f in enumerate(faces):
            (startX , startY) = f[0], f[1]
            (endX , endY) = f[2],f[3]
            if count % 4 == 0 :
                only_face = img[startY:endY,startX:endX].copy()
                cv2.imwrite('D:/github/2022_class/data/maskedface/'+i.split('\\')[4],only_face)
            else:
                only_face = img[startY:endY,startX:endX].copy()
                cv2.imwrite('./data/unmasked/'+i.split('\\')[4],only_face)
        count+=1

image_load_and_face('D:\vision_data\data1\images\*.jpg')