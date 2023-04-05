from PyQt6.QtWidgets import QProgressBar

from utils.read_file import ReadFile


class CollectProgressBar(QProgressBar):

    def __init__(self, widget, style_sheet_path, maximum):
        super(CollectProgressBar, self).__init__(widget)
        self.__init_ui(style_sheet_path, maximum)

    def __init_ui(self, style_sheet_path, maximum):
        self.setStyleSheet(ReadFile.read_style_sheet(style_sheet_path))
        self.setVisible(False)
        self.setTextVisible(False)
        self.setMaximum(maximum)
