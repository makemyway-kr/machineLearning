import tensorflow as tf
from glob import glob
import json
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, BatchNormalization
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
images = glob('/content/drive/MyDrive/part_of_data/*.jpg')
faces = []
face_result_data = []
#dataset 얼굴범위 인식 결과 로드
with open('/content/drive/MyDrive/result.json','r',encoding='utf-8') as f:
    face_result_data = json.load(f)
#이미지 리사이징
image_array = np.float32(np.zeros((len(face_result_data.keys(),224,224,3))))
labels = np.float64(np.zeros((len(face_result_data),1)))
count = 0
for k in face_result_data.keys():
    img = load_img(k,target_size = (224 , 224))

    i = img_to_array(img)
    i = np.expand_dims(x,axis = 0)
    i = preprocess_input(i)
    image_array[count,:,:,:] = i
    labels[count] = k.split('_')[1] #이미지 이름에 라벨이 있음.
    
