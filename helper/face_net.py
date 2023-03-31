# Weights downloaded from: https://github.com/nyoki-mtl/keras-facenet
# > Pretrained Keras model trained by MS-Celeb-1M dataset

import cv2
import numpy as np
from sklearn.preprocessing import Normalizer

from model.inception_resnet_v2 import InceptionResNetV2


class FaceNet:
    def __init__(self):
        self.__face_encoder = InceptionResNetV2('./assets/model/facenet_keras_weights.h5')
        self.__l2_normalizer = Normalizer('l2')

    def create_face_embedding(self, faces):
        normalized_faces = self.__normalize(faces)
        faces_array = np.asarray(normalized_faces)
        face_embedding = self.__face_encoder.model.predict(faces_array)
        face_embedding_average = np.average(face_embedding, axis=0)

        return self.__l2_normalizer.transform(np.expand_dims(face_embedding_average, axis=0))[0]

    @staticmethod
    def __normalize(faces):
        normalized_faces = []
        for face in faces:
            face = cv2.resize(face, (160, 160))
            mean, std = face.mean(), face.std()
            normalized_faces.append((face - mean) / std)

        return normalized_faces
