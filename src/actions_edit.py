from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog


class EditActions(QAction):
    def __init__(self, parent, actionName):
        self.parent = parent
        self.actionName = actionName
        super().__init__("", parent)
        self.triggered.connect(self.handle_action)

        self.setText(actionName)
        if(self.actionName=="Rotate 90"):
            self.setIcon(QIcon('images/open_file.png'))
            self.setShortcut('Ctrl+O')
            self.setStatusTip('Rotate image 90º clockwise')
        elif(self.actionName=="Rotate 180"):
            self.setIcon(QIcon('images/save_file.png'))
            self.setShortcut('Ctrl+S')
            self.setStatusTip('Rotate image 180º clockwise')
    

    def handle_action(self):
        if(self.actionName=="Rotate 90"):
            self.rotateImage90(self.parent)
        elif(self.actionName=="Rotate 180"):
            self.rotateImage180(self.parent)
        
    def rotateImage90(self, parent):
        """
        Rotate image 90º clockwise
        """
        if parent.image.isNull() == False:
            transform90 = QTransform().rotate(90)
            pixmap = QPixmap(parent.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)

            parent.image_label.setPixmap(rotated.scaled(parent.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            parent.image = QPixmap(rotated) 
            parent.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def rotateImage180(self, parent):
        """
        Rotate image 180º clockwise
        """
        if parent.image.isNull() == False:
            transform180 = QTransform().rotate(180)
            pixmap = QPixmap(parent.image)

            rotated = pixmap.transformed(transform180, mode=Qt.SmoothTransformation)

            parent.image_label.setPixmap(rotated.scaled(parent.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # .......... To keep being allowed to rotate the image
            parent.image = QPixmap(rotated) 
            parent.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    