from PyQt6 import QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QMainWindow, QWidget

from view.button_view import ButtonView
from view.collect_progress_bar_view import CollectProgressBar
from view.gif_view import GifView
from view.overlay_view import OverlayView
from view.result_label_view import ResultLabelView
from view.toast_view import ToastView


class CameraView(QMainWindow):

    def __init__(self):
        super(CameraView, self).__init__()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('CheckFace')
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.image_label = QLabel(self.widget)
        self.verified_view = ResultLabelView(self.widget, './assets/UI/verified.png')
        self.rejected_view = ResultLabelView(self.widget, './assets/UI/rejected.png')
        self.overlay_view = OverlayView(self.widget)
        self.learn_button = ButtonView(self.widget, 'view/styles/learn_button.css')
        self.verify_button = ButtonView(self.widget, 'view/styles/verify_button.css')
        self.reset_button = ButtonView(self.widget, 'view/styles/reset_button.css')
        self.continue_button = ButtonView(self.widget, 'view/styles/continue_button.css')
        self.try_again_button = ButtonView(self.widget, 'view/styles/try_again_button.css')
        self.toast_view = ToastView(self.widget, 'view/styles/toast_message.css')
        self.app_mode_toast_view = ToastView(self.widget, 'view/styles/app_mode_toast.css')
        self.collect_progress = CollectProgressBar(self.widget, 'view/styles/collect_progress_bar.css', maximum=100)
        self.loading_gif_view = GifView(self.widget, './assets/UI/loading_gif')

        self.on_closed = None

    def square_frame(self, square_frame_size):
        self.set_learn_button_style(square_frame_size)
        self.set_verify_button_style(square_frame_size)
        self.set_reset_button_style(square_frame_size)
        self.set_continue_button_style(square_frame_size)
        self.set_try_again_button_style(square_frame_size)
        self.set_verified_view_style(square_frame_size)
        self.set_rejected_view_style(square_frame_size)
        self.set_toast_view_style(square_frame_size)
        self.set_app_mode_toast_style(square_frame_size)
        self.set_progress_bar_style(square_frame_size)
        self.set_loading_gif_style(square_frame_size)
        self.setFixedSize(square_frame_size, square_frame_size + self.learn_button.height())
        self.image_label.setFixedSize(square_frame_size, square_frame_size)
        # print('square camera frame size is {}*{}'.format(self.image_label.width(), self.image_label.height()))

    def set_pix_map(self, pix_map: QPixmap):
        self.image_label.setPixmap(pix_map)

    def set_on_closed(self, on_closed):
        self.on_closed = on_closed

    def face_status_toast(self, verify_button_is_enabled, learn_button_is_enable, is_visible, toast_message):
        self.toast_view.setVisible(is_visible)
        self.toast_view.setText(toast_message)
        self.learn_button.setEnabled(learn_button_is_enable)
        self.verify_button.setEnabled(verify_button_is_enabled)

    def app_mode_toast(self, is_visible, toast_message):
        self.app_mode_toast_view.setVisible(is_visible)
        self.app_mode_toast_view.setText(toast_message)

    def set_toast_view_style(self, square_frame_size):
        toast_width = int(square_frame_size * 0.7)
        toast_height = square_frame_size * 0.14
        self.toast_view.setGeometry((square_frame_size - toast_width) // 2, 0, int(toast_width), int(toast_height))

    def progressbar_update(self, is_visible, value):
        self.collect_progress.setVisible(is_visible)
        self.collect_progress.setValue(value)

    def set_app_mode_toast_style(self, square_frame_size):
        toast_height = square_frame_size * 0.15
        toast_width = square_frame_size
        self.app_mode_toast_view.setGeometry((square_frame_size - toast_width) // 2, square_frame_size,
                                             int(toast_width), int(toast_height))

    def set_learn_button_style(self, square_frame_size):
        button_height = square_frame_size * 0.15
        button_width = square_frame_size
        self.learn_button.setText('Learn My Face')
        self.learn_button.setGeometry((square_frame_size - button_width) // 2, square_frame_size,
                                      int(button_width), int(button_height))

    def set_verify_button_style(self, square_frame_size):
        button_height = square_frame_size * 0.15
        button_width = square_frame_size * 0.75
        self.verify_button.setText('Verify My Face')
        self.verify_button.setGeometry(int(0.25 * square_frame_size), square_frame_size,
                                       int(button_width), int(button_height))

    def set_reset_button_style(self, square_frame_size):
        button_height = square_frame_size * 0.15
        button_width = square_frame_size * 0.25
        self.reset_button.setText('Reset')
        self.reset_button.setGeometry(0, square_frame_size,
                                      int(button_width), int(button_height))

    def set_continue_button_style(self, square_frame_size):
        button_height = square_frame_size * 0.15
        button_width = square_frame_size
        self.continue_button.setText('Continue')
        self.continue_button.setGeometry(int(square_frame_size - button_width) // 2, square_frame_size,
                                         int(button_width), int(button_height))

    def set_try_again_button_style(self, square_frame_size):
        button_height = square_frame_size * 0.15
        button_width = square_frame_size
        self.try_again_button.setText('Try Again')
        self.try_again_button.setGeometry(int(square_frame_size - button_width) // 2, square_frame_size,
                                          int(button_width), int(button_height))

    def set_progress_bar_style(self, square_frame_size):
        progress_bar_height = square_frame_size * 0.02
        progress_bar_width = square_frame_size
        self.collect_progress.setGeometry((square_frame_size - progress_bar_width) // 2,
                                          int(square_frame_size - progress_bar_height),
                                          progress_bar_width, int(progress_bar_height))

    def set_loading_gif_style(self, square_frame_size):
        gif_size = QSize(square_frame_size, square_frame_size)
        self.loading_gif_view.movie.setScaledSize(gif_size)
        self.loading_gif_view.setGeometry(0, 0, square_frame_size, square_frame_size)

    def set_verified_view_style(self, square_frame_size):
        resized_image = self.verified_view.result_image.scaled(square_frame_size, square_frame_size)
        self.verified_view.setPixmap(resized_image)

    def set_rejected_view_style(self, square_frame_size):
        resized_image = self.rejected_view.result_image.scaled(square_frame_size, square_frame_size)
        self.rejected_view.setPixmap(resized_image)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        super().closeEvent(a0)
        self.on_closed and self.on_closed()
