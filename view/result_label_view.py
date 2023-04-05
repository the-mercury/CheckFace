from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class ResultLabelView(QLabel):
    def __init__(self, widget, file_path):
        super(ResultLabelView, self).__init__(widget)
        self.__init_ui(file_path)

    def __init_ui(self, file_path):
        self.result_image = QPixmap(QImage(file_path))
