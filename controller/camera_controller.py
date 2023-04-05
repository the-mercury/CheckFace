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

    def __connect_signals(self):
        self.camera_model.update_frame_signal.connect(self.__update_view)
        self.camera_model.on_frame_size_chosen.connect(self.__update_view_size)
        self.camera_view.learn_button.clicked.connect(self.__on_learn_button_pressed)
        self.camera_view.verify_button.clicked.connect(self.__on_verify_button_pressed)
        self.camera_view.reset_button.clicked.connect(self.__on_reset_button_pressed)
        self.camera_view.continue_button.clicked.connect(self.__on_continue_button_pressed)
        self.camera_view.try_again_button.clicked.connect(self.__on_try_again_button_pressed)

    @pyqtSlot(np.ndarray)
    def __update_view(self, frame):
        CameraController.mutex.lock()
        height, width = frame.shape[:2]
        convert_to_qt_format = QImage(frame.data.tobytes(), width, height, QImage.Format.Format_RGB888)
        image_pix_map = QPixmap.fromImage(convert_to_qt_format)
        self.camera_view.set_pix_map(image_pix_map)
        self.overlay_controller.detect_face_status(frame)
        CameraController.mutex.unlock()
        CameraController.wait_condition.wakeAll()

    @pyqtSlot(int)
    def __update_view_size(self, square_frame_size):
        self.camera_view.square_frame(square_frame_size)
        self.overlay_controller.update_overlay_mask(square_frame_size)

    def __on_face_status_update(self, face_status, app_mode):
        if app_mode is not OverlayController.AppMode.MODEL_GENERATE and \
                app_mode is not OverlayController.AppMode.VERIFIED and \
                app_mode is not OverlayController.AppMode.REJECTED:

            is_visible = False
            toast_message = None
            learn_button_is_enabled = True
            verify_button_is_enabled = True

            if face_status == FaceDetector.FaceStatus.FINE or face_status == FaceDetector.FaceStatus.UNKNOWN:
                is_visible = False
                toast_message = None

            elif face_status == FaceDetector.FaceStatus.LITTLE_CLOSE or face_status == FaceDetector.FaceStatus.CLOSE:
                is_visible = True
                toast_message = 'Move Away'

            elif face_status == FaceDetector.FaceStatus.LITTLE_FAR or face_status == FaceDetector.FaceStatus.FAR:
                is_visible = True
                toast_message = 'Move Closer'

            elif face_status == FaceDetector.FaceStatus.NOT_CENTER:
                is_visible = True
                toast_message = 'Center Your Face'

            elif face_status == FaceDetector.FaceStatus.OUT_OF_FRAME:
                is_visible = True
                toast_message = 'Frame Your Face...'
                learn_button_is_enabled = False
                verify_button_is_enabled = False

            self.camera_view.face_status_toast(verify_button_is_enabled, learn_button_is_enabled,
                                               is_visible, toast_message)

    def start(self):
        CameraController.mutex.lock()
        self.camera_model.start()
        self.camera_view.show()

    def on_close(self):
        self.camera_model.stop()
