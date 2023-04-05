from PyQt6.QtCore import QObject, QMutex, QWaitCondition

from controller.overlay_controller import OverlayController


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

    def start(self):
        CameraController.mutex.lock()
        self.camera_model.start()
        self.camera_view.show()

    def on_close(self):
        self.camera_model.stop()
