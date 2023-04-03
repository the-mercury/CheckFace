from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QLabel


class GifView(QLabel):
    def __init__(self, widget, file_path):
        super(GifView, self).__init__(widget)
        self.__init_ui(file_path)

    def __init_ui(self, file_path):
        self.movie = QMovie(file_path)
        self.setMovie(self.movie)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
