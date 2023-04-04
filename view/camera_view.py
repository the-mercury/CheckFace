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
