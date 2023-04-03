from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from utils.read_file import ReadFile


class ToastView(QLabel):
    def __init__(self, widget, style_sheet_path):
        super(ToastView, self).__init__(widget)
        self.__init_ui(style_sheet_path)

    def __init_ui(self, style_sheet_path):
        self.setVisible(False)
        self.setStyleSheet(ReadFile.read_style_sheet(style_sheet_path))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
