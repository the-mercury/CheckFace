import os
import shutil
from enum import Enum
from threading import Timer

import numpy as np
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QPixmap, QImage

from helper.face_detector import FaceDetector
from helper.face_net import FaceNet

MASK_FRAME_RATIO = 0.9
FACE_BUFFER_NUMBER = 1
TIMES_UP_LIMIT = 7  # seconds


class OverlayController(QObject):
    class AppMode(Enum):
        PRE_START = 0
        DATA_COLLECT = 1
        MODEL_GENERATE = 2
        VERIFY = 3
        VERIFIED = 4
        REJECTED = 5

    def __init__(self, overlay_view, on_face_status_update,
                 on_app_mode_update, collect_data_progress_update):
        super(OverlayController, self).__init__()
        self.__on_face_status_update = on_face_status_update
        self.__on_app_mode_update = on_app_mode_update
        self.__collect_data_progress_update = collect_data_progress_update
        self.__mask_frame_ratio = MASK_FRAME_RATIO
        self.overlay_view = overlay_view
        self.__face_detector = FaceDetector()
        self.__face_net = FaceNet()
        self.__previous_face_status = FaceDetector.FaceStatus.UNKNOWN
        if os.path.isfile('./face_model/face_embedding.npy'):
            self.__app_mode = self.AppMode.VERIFY
        else:
            self.__app_mode = self.AppMode.PRE_START
        self.__on_app_mode_update(self.__app_mode)
        self.__face_buffer = []
        self.__times_up_limit = TIMES_UP_LIMIT
        self.__timer = Timer(self.__times_up_limit, self.__on_times_up)
        self.__model_generate_timer = Timer(0.01, self.__on_model_generate_times_up)

    def __create_overlay_mask(self, square_frame_size: int) -> QPixmap:
        mask_frame = np.zeros((square_frame_size, square_frame_size, 4), dtype='uint8')
        mask_frame.fill(225)

        y, x = np.ogrid[0:square_frame_size, 0:square_frame_size]
        cy, cx = square_frame_size // 2, square_frame_size // 2
        a = self.__mask_frame_ratio
        b = a / 1.6

        ellipse_roi = (((y - cy) ** 2) / a ** 2 + ((x - cx) ** 2) / b ** 2) <= (cx * cy)
        mask_frame[ellipse_roi] = 0
        convert_to_qt_format = QImage(mask_frame.data.tobytes(), square_frame_size, square_frame_size,
                                      QImage.Format.Format_RGBA8888)
        mask_pix_map = QPixmap.fromImage(convert_to_qt_format)
        self.rect_roi = (cx, cy, b * square_frame_size, a * square_frame_size)

        return mask_pix_map

    def update_overlay_mask(self, square_frame_size: int):
        mask_pix_map = self.__create_overlay_mask(square_frame_size)
        self.overlay_view.setFixedSize(square_frame_size, square_frame_size)
        self.overlay_view.set_pix_map(mask_pix_map)

    def detect_face_status(self, frame: np.ndarray):
        x_roi = int(self.rect_roi[0] - self.rect_roi[2] / 2)
        y_roi = int(self.rect_roi[1] - self.rect_roi[3] / 2)
        rect_width = int(self.rect_roi[2])
        rect_height = int(self.rect_roi[3])
        cx_roi = x_roi + rect_width // 2
        cy_roi = y_roi + rect_height // 2
        # cv2.rectangle(frame, (x_roi, y_roi), (x_roi + rect_width, y_roi + rect_height), (0, 255, 255), 2)

        face_coordinates, detection_confidence = self.__face_detector.detect(frame)
        if face_coordinates is None or detection_confidence is None:
            face_status = self.__face_detector.FaceStatus.OUT_OF_FRAME
        else:
            x_face, y_face, face_width, face_height = face_coordinates[0], face_coordinates[1], \
                                                      face_coordinates[2], face_coordinates[3]
            cx_face = x_face + face_width // 2
            cy_face = y_face + face_height // 2
            # cv2.rectangle(frame, (x_face, y_face), (x_face + face_width, y_face + face_height), (0, 255, 0), 2)
            # cv2.imshow('faces', frame)
            face_status = self.__face_detector.check_face_position((cx_face, cy_face, face_width, face_height,
                                                                    cx_roi, cy_roi, rect_width, rect_height))

            if self.__app_mode == self.AppMode.DATA_COLLECT and face_status == FaceDetector.FaceStatus.FINE:
                self.__face_buffer.append(frame[y_face:y_face + face_height, x_face:x_face + face_width])
                self.__collect_data_progress_update(True, len(self.__face_buffer) * 100 // FACE_BUFFER_NUMBER)
                # cv2.imshow('perfect faces', frame[y_face:y_face + face_height, x_face:x_face + face_width])
                if len(self.__face_buffer) == FACE_BUFFER_NUMBER:
                    self.__app_mode = self.AppMode.MODEL_GENERATE
                    self.__on_app_mode_update(self.__app_mode)
                    self.__model_generate_timer.start()

        if self.__previous_face_status != face_status and face_status != FaceDetector.FaceStatus.UNKNOWN:
            self.__previous_face_status = face_status
            self.__on_face_status_update(face_status, self.__app_mode)

    def __create_face_embedding(self, faces: list[np.ndarray]) -> np.ndarray:
        return self.__face_net.create_face_embedding(faces)

    def __verification_confidence(self, face_embedding_buffer: np.ndarray):
        existing_model = np.load('./face_model/face_embedding.npy')
        embeddings_difference = np.linalg.norm(existing_model - face_embedding_buffer)
        similarity = 100 * (existing_model @ face_embedding_buffer.T)

        if similarity > 50 and embeddings_difference < 1.1:
            print('l2 distance: {:.2f}'.format(embeddings_difference))
            print('similarity: {:.2f}%'.format(similarity))
            self.__app_mode = self.AppMode.VERIFIED
            self.__on_app_mode_update(self.__app_mode)

        else:
            print('l2 distance: {:.2f}'.format(embeddings_difference))
            print('similarity: {:.2f}%'.format(similarity if similarity > 0 else 0))
            self.__app_mode = self.AppMode.REJECTED
            self.__on_app_mode_update(self.__app_mode)

    def on_learn_button_pressed(self):
        self.__app_mode = self.AppMode.DATA_COLLECT
        self.__on_app_mode_update(self.__app_mode)
        if not self.__timer.is_alive():
            self.__timer.start()

    def on_verify_button_pressed(self):
        self.__app_mode = self.AppMode.DATA_COLLECT
        self.__on_app_mode_update(self.__app_mode)
        if not self.__timer.is_alive():
            self.__timer.start()

    def on_reset_button_pressed(self):
        shutil.rmtree('./face_model')
        self.__face_buffer = []
        self.__app_mode = OverlayController.AppMode.PRE_START
        self.__on_app_mode_update(self.__app_mode)

    def on_continue_button_pressed(self):
        self.__app_mode = self.AppMode.VERIFY
        self.__on_app_mode_update(self.__app_mode)

    def on_try_again_button_pressed(self):
        self.__app_mode = self.AppMode.VERIFY
        self.__on_app_mode_update(self.__app_mode)

    def __on_model_generate_times_up(self):
        face_embedding_buffer = self.__create_face_embedding(self.__face_buffer)
        self.__app_mode = self.AppMode.VERIFY
        self.__on_app_mode_update(self.__app_mode)
        self.__face_buffer = []

        if os.path.isfile('./face_model/face_embedding.npy'):
            self.__verification_confidence(face_embedding_buffer)
        else:
            os.mkdir('./face_model')
            np.save('./face_model/face_embedding.npy', face_embedding_buffer)

        self.__model_generate_timer = Timer(0.01, self.__on_model_generate_times_up)

    def __on_times_up(self):
        if self.__app_mode == self.AppMode.DATA_COLLECT:
            print('Time is up! Please frame your face and start the process again.')
            self.__face_buffer = []
            self.__timer = Timer(self.__times_up_limit, self.__on_times_up)
            if os.path.isfile('./face_model/face_embedding.npy'):
                self.__app_mode = self.AppMode.VERIFY
                self.__on_app_mode_update(self.__app_mode)
            else:
                self.__app_mode = self.AppMode.PRE_START
                self.__on_app_mode_update(self.__app_mode)
        else:
            self.__timer = Timer(self.__times_up_limit, self.__on_times_up)
