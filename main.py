import sys

from PyQt6.QtWidgets import QApplication

from controller.camera_controller import CameraController
from model.camera_model import CameraModel
from view.camera_view import CameraView

SQUARE_FRAME_SIZE = 300


def main():
    app = QApplication([])
    camera_model = CameraModel.get_instance(SQUARE_FRAME_SIZE, CameraController.mutex, CameraController.wait_condition)
    camera_view = CameraView()
    camera_controller = CameraController(camera_model, camera_view)
    camera_controller.start()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
