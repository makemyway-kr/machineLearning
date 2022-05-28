import tensorflow as tf
from glob import glob
import json
import numpy as np
import cv2
import os
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, BatchNormalization
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import load_img, img_to_array

baseDir = '/mnt/hdd/vision_data/'
with tf.device("/GPU:0"):
    images = glob(baseDir+'data1/images/*.jpg')
    faces = []
    face_result_data = []
    face_whole = []
    #dataset 얼굴범위 인식 결과 로드
    with open('./result.json','r',encoding='utf-8') as f:
        face_whole = json.load(f)
    face_result_data = list(face_whole.keys()) 
    #이미지 리사이징
    image_array = np.float32(np.zeros((2000,256,256,3)))#램 제한으로 인한 데이터 수 줄임
    labels = np.float64(np.zeros((2000,4)))
    count = 0
    for k in face_result_data: #라벨과 이미지 담기
        if count == 2000:
            break
        print(k)
        try:
            #face = cv2.imread(k)
            coordinate = face_whole[k]['face']
            if len(coordinate) != 0 :
                #cv2.imwrite(baseDir+'onlyMask/'+str(k.split('/')[6]),face[coordinate[1]:coordinate[3],coordinate[0]: coordinate[2] , :])
                img = load_img(baseDir + 'onlyMask/'+str(k.split('/')[6]),target_size = (256 , 256))
                i = img_to_array(img)
                i = np.expand_dims(i,axis = 0)
                i = preprocess_input(i)
                image_array[count,:,:,:] = i
                this_label = int(k.split('_')[2][0])
                labels[count][this_label-1] = 1
            else:
                continue
        except Exception as ex:
            print(ex)
            continue
        count += 1

    #TRAIN / test data 나누기
    trainImgCount = int(np.round(labels.shape[0]*0.8)) #80퍼센트 트레이닝 데이터로
    testImgCount = int(np.round(labels.shape[0]*0.8))

    trainImg = image_array[0:trainImgCount,:,:,:]
    testImg = image_array[trainImgCount:,:,:,:]

    trainLabel = labels[0:trainImgCount]
    testLabel = labels[trainImgCount:]

    imgShape = (256,256,3)

    #resnetBase = ResNet50(input_shape = imgShape , weights = 'imagenet',include_top = False)
    #resnetBase.trainable = True
    #resnetBase.summary()
    efficientNetBase = EfficientNetB0(include_top = False, weights = 'imagenet', input_shape = imgShape,classes = 4, classifier_activation='softmax')
    efficientNetBase.trainable = True
    efficientNetBase.summary()
    fL = Flatten()
    dL1 = Dense(256,activation = 'relu')
    bnL1 = BatchNormalization()
    dL2 = Dense(256,activation = 'relu')
    bnL2 = BatchNormalization()
    dL3 = Dense(256,activation = 'relu')
    bnL3 = BatchNormalization()
    dL4 = Dense(4,activation = tf.keras.activations.softmax) #라벨과 같은 4개로 분류, softmax사용

    model = Sequential([
        efficientNetBase,
        fL,
        dL1,
        bnL1,
        dL2,
        bnL2,
        dL4,]
    )
    learningRate = 0.00001
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=learningRate), loss = tf.keras.losses.CategoricalHinge() , metrics = ['accuracy',tf.keras.metrics.AUC()])
    model.summary()

    model.fit(trainImg,trainLabel,epochs = 60 , batch_size  = 10 , validation_data = (testImg,testLabel))

    model.save("model_M1_3_E.h5")


