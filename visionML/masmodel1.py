import tensorflow as tf
from glob import glob
import json
import numpy as np
import cv2
import os
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, BatchNormalization
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


images = glob('/content/drive/MyDrive/part_of_data/*.jpg')
faces = []
face_result_data = []
#dataset 얼굴범위 인식 결과 로드
with open('/content/drive/MyDrive/result.json','r',encoding='utf-8') as f:
    face_result_data = json.load(f)
#이미지 리사이징
image_array = np.float32(np.zeros((len(face_result_data.keys()),224,224,3)))
labels = np.float64(np.zeros((len(face_result_data),1)))
count = 0
for k in face_result_data.keys(): #라벨과 이미지 담기
    face = cv2.imread(k)
    coordinate = face_result_data[k]['face']
    cv2.imwrite('/content/drive/MyDrive/onlyMask'+str(k.split('\\')[1]),face[coordinate[1]:coordinate[3],coordinate[0]: coordinate[2] , :])
    img = load_img('/content/drive/MyDrive/onlyMask'+str(k.split('\\')[1]),target_size = (224 , 224))

    i = img_to_array(img)
    i = np.expand_dims(i,axis = 0)
    i = preprocess_input(i)
    image_array[count,:,:,:] = i
    labels[count] = k.split('_')[1] #이미지 이름에 라벨이 있음.

#TRAIN / test data 나누기
trainImgCount = int(np.round(labels.shape[0]*0.8)) #80퍼센트 트레이닝 데이터로
testImgCount = int(np.round(labels.shape[0]*0.8))

trainImg = image_array[0:trainImgCount,:,:,:]
testImg = image_array[trainImgCount:,:,:,:]

trainLabel = labels[0:trainImgCount]
testLabel = labels[trainImgCount:]

imgShape = (224,224,3)

resnetBase = ResNet50(input_shape = imgShape , weights = 'imagenet',include_top = False)
resnetBase.trainable = True
resnetBase.summary()

fL = Flatten()
dL1 = Dense(128,activation = 'relu')
bnL1 = BatchNormalization()
dL2 = Dense(4,activation = tf.keras.activations.softmax) #라벨과 같은 4개로 분류, softmax사용

model = Sequential(
    resnetBase,
    fL,
    dL1,
    bnL1,
    dL2,
)
learningRate = 0.001
model.compile(optimizer=tf.keras.optimizers.Adam(lr=learningRate), loss = tf.keras.losses.MeanSquaredError() , metrics = ['accuracy'])
model.summary()

with tf.device("/gpu:0"):
    model.fit(trainImg,trainLabel,epochs = 100 , batch_size  = 50 , validation_data = (testImg,testLabel))

model.save("model.M1")


