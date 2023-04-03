from PyQt6.QtWidgets import QPushButton

from utils.read_file import ReadFile


class ButtonView(QPushButton):

    def __init__(self, widget, style_sheet_path):
        super(ButtonView, self).__init__(widget)
        self.__init_ui(style_sheet_path)

    def __init_ui(self, style_sheet_path):
        self.setStyleSheet(ReadFile.read_style_sheet(style_sheet_path))
