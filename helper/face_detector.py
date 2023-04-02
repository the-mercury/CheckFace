import math
import os
from enum import Enum

import cv2
# import mediapipe as mp


class FaceDetector:
    class FaceStatus(Enum):
        UNKNOWN = -3
        OUT_OF_FRAME = -2
        NOT_CENTER = -1
        FINE = 0
        LITTLE_CLOSE = 0.5
        CLOSE = 1
        LITTLE_FAR = 1.5
        FAR = 2

    def __init__(self):
        # ToDo: change to mediapipe face detector
        cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
        self.detector = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_alt.xml'))
        # self.detector = mp.solutions.face_detection

    def detect(self, frame, scale_factor=1.1, min_neighbours=5):
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_coordinates = self.detector.detectMultiScale(grayscale_frame, scale_factor, min_neighbours)
        # face_coordinates = self.detector.FaceDetection

        return face_coordinates

    @staticmethod
    def check_face_position(face_and_roi_coordinates):
        face_roi_height_ratio = face_and_roi_coordinates[3] / face_and_roi_coordinates[7]
        face_roi_center_diff = int(
            math.sqrt((face_and_roi_coordinates[0] // 2 - face_and_roi_coordinates[4] // 2) ** 2 +
                      (face_and_roi_coordinates[1] // 2 - face_and_roi_coordinates[5] // 2) ** 2))

        face_status = FaceDetector.FaceStatus.UNKNOWN

        if face_roi_center_diff >= 14:
            face_status = FaceDetector.FaceStatus.NOT_CENTER

        elif face_roi_center_diff < 14:
            if 0.80 >= face_roi_height_ratio >= 0.65:
                face_status = FaceDetector.FaceStatus.FINE

            elif 0.90 >= face_roi_height_ratio > 0.80:
                face_status = FaceDetector.FaceStatus.LITTLE_CLOSE

            elif face_roi_height_ratio > 0.95:
                face_status = FaceDetector.FaceStatus.CLOSE

            elif 0.65 > face_roi_height_ratio >= 0.60:
                face_status = FaceDetector.FaceStatus.LITTLE_FAR

            elif face_roi_height_ratio < 0.55:
                face_status = FaceDetector.FaceStatus.FAR

        return face_status
