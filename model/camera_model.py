import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal


class CameraModel(QThread):
    _instance = None
    update_frame_signal = pyqtSignal(np.ndarray)
    on_frame_size_chosen = pyqtSignal(int)

    @staticmethod
    def get_instance(frame_size, mutex, condition):
        if CameraModel._instance is None:
            CameraModel(frame_size, mutex, condition)
        return CameraModel._instance

    def __init__(self, frame_size, mutex, condition):
        if CameraModel._instance is not None:
            raise Exception('>>>NOTE: An instance of "CameraModel" already exists!')
        else:
            super(CameraModel, self).__init__()
            CameraModel._instance = self
            # To run the app on a Windows machine:
            # self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            # On Mac:
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_size)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_size)
            self.mutex = mutex
            self.condition = condition

    def run(self):
        frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print('raw camera frame size is {}*{}'.format(frame_width, frame_height))
        min_size = min(frame_width, frame_height)
        self.on_frame_size_chosen.emit(min_size)
        frame_center = (frame_width // 2, frame_height // 2)
        frame_roi_width = (frame_center[0] - min_size // 2, frame_center[0] + min_size // 2)
        frame_roi_height = (frame_center[1] - min_size // 2, frame_center[1] + min_size // 2)

        while self.capture.isOpened():
            _status, frame = self.capture.read()
            if not _status:
                raise Exception('>>>Error: No camera detected, or permission to access the camera is not granted!')
            frame = cv2.flip(frame, 1)
            frame_roi = frame[frame_roi_height[0]:frame_roi_height[1], frame_roi_width[0]:frame_roi_width[1]]
            rgb_frame = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2RGB)
            self.update_frame_signal.emit(rgb_frame)
            self.condition.wait(self.mutex)

    def stop(self):
        self.capture.release()
