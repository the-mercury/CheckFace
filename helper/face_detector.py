import math
from enum import Enum

import mediapipe as mp
import numpy as np


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
        self.__detector = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)

    def detect(self, frame: np.ndarray) -> tuple[tuple[int, int, int, int], float]:
        results = self.__detector.process(frame)
        face_coordinates, detection_confidence = None, None
        frame_shape = frame.shape
        if results.detections is not None:
            for detection in results.detections:
                bounding_box = detection.location_data.relative_bounding_box
                x_min = bounding_box.xmin
                y_min = bounding_box.ymin
                width = bounding_box.width
                height = bounding_box.height
                relative_face_coordinates = x_min, y_min, width, height
                detection_confidence = detection.score[0]
                face_coordinates = self.__get_absolute_coordinate(relative_face_coordinates, frame_shape)

        return face_coordinates, detection_confidence

    @staticmethod
    def check_face_position(face_and_roi_coordinates: tuple[int, int, int, int, int, int, int, int]) -> FaceStatus:
        face_roi_height_ratio = face_and_roi_coordinates[3] / face_and_roi_coordinates[7]
        face_roi_center_diff = int(
            math.sqrt((face_and_roi_coordinates[0] // 2 - face_and_roi_coordinates[4] // 2) ** 2 +
                      (face_and_roi_coordinates[1] // 2 - face_and_roi_coordinates[5] // 2) ** 2))

        face_status = FaceDetector.FaceStatus.UNKNOWN

        if face_roi_center_diff >= 30:
            face_status = FaceDetector.FaceStatus.NOT_CENTER
        else:
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

    @staticmethod
    def __get_absolute_coordinate(face_coordinates: tuple[float, float, float, float],
                                  frame_shape: tuple[int, int, int]) -> tuple[int, int, int, int]:
        x_min = int(face_coordinates[0] * frame_shape[1])
        y_min = int(face_coordinates[1] * frame_shape[0])
        width = int(face_coordinates[2] * frame_shape[1])
        height = int(face_coordinates[3] * frame_shape[0])
        absolute_face_coordinates = x_min, y_min, width, height

        return absolute_face_coordinates
