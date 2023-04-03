from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class OverlayView(QLabel):
    def __init__(self, widget):
        super(OverlayView, self).__init__(widget)

    def set_pix_map(self, pix_map: QPixmap):
        self.setPixmap(pix_map)
