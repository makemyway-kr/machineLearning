import cvlib as cv
import cv2
import os
import json
import numpy as np
from glob import glob
def image_load_and_face(imagefileDir):
    os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    images = glob(r'D:\vision_data\data1\images\*.jpg')
    result = {}
    for image in images:
        try:
            img = cv2.imread(image)
        except Exception as ex:
            continue
        # 얼굴인식
        try:
            faces, confidences = cv.detect_face(img,enable_gpu = True)
            genders = []
            #for (x, y, x2, y2), conf in zip(faces, confidences):
        		# 확률 표시
                #cv2.putText(img, str(conf), (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        		# 얼굴위치 bbox 그리기
                #cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
                #label , gconf = cv.detect_gender(img[y:y2,x:x2],enable_gpu = True)
                #genders.append(label[np.argmax(gconf)])

            # 영상 출력
            #cv2.namedWindow('image',cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('image',500,700)
            #cv2.imshow('image', img)
            #key = cv2.waitKey(0)
            #cv2.destroyAllWindows()
            print(confidences)
            #type change from int32 into normal integer
            max = float(0.0)
            face = []
            for i in range(len(faces)):
                if confidences[i] > max:
                    max = confidences[i]
                    face = faces[i]
            for i in range(len(face)):
                face[i] = int(face[i])
            result[image] = {'face':face,'confidence':float(max)}
        except Exception as ex:
            print(ex)
            continue

        
    with open('./result.json','w',encoding='utf-8') as f:
        f.write(json.dumps(result,ensure_ascii=False,indent=4))
        '''
        print(i,confidences)
        for idx , f in enumerate(faces):
            (startX , startY) = f[0], f[1]
            (endX , endY) = f[2],f[3]
            if count % 4 == 0 :
                only_face = img[startY:endY,startX:endX].copy()
                cv2.imwrite('D:/github/2022_class/data/maskedface/'+i.split('\\')[4],only_face)
            else:
                only_face = img[startY:endY,startX:endX].copy()
                cv2.imwrite('./data/unmasked/'+i.split('\\')[4],only_face)
        count+=1'''

image_load_and_face('D:\vision_data\data1\images\*.jpg')