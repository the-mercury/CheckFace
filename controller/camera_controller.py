import numpy as np
from PyQt6.QtCore import pyqtSlot, QObject, QMutex, QWaitCondition
from PyQt6.QtGui import QPixmap, QImage

from controller.overlay_controller import OverlayController
from helper.face_detector import FaceDetector


class CameraController(QObject):
    mutex = QMutex()
    wait_condition = QWaitCondition()

    def __init__(self, camera_model, camera_view):
        super(CameraController, self).__init__()
        self.camera_model = camera_model
        self.camera_view = camera_view
        self.overlay_controller = OverlayController(self.camera_view.overlay_view,
                                                    self.__on_face_status_update,
                                                    self.__on_app_mode_update,
                                                    self.__on_collect_data_progressbar_update)
        self.__connect_signals()
        self.camera_view.set_on_closed(self.on_close)

    def start(self):
        CameraController.mutex.lock()
        self.camera_model.start()
        self.camera_view.show()

    def on_close(self):
        self.camera_model.stop()
