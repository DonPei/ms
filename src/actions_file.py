from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import os

from MarianaActions import MarianaActions

from dialogs_settings import SettingsDialog

class FileActions(MarianaActions):
    def __init__(self, parent, actionName):
        super().__init__(parent, actionName)
        if(self.actionName=="Open"):
            self.createSubMenu(actionName, 0, 'Open an image', 'Ctrl+O', 'open_file.png')
        elif(self.actionName=="Save"):
            self.createSubMenu(actionName, 1, 'Save image', 'Ctrl+S', 'save_file.png')
        elif(self.actionName=="Print"):
            self.createSubMenu(actionName, 10, 'Pint', 'Ctrl+P', 'print.png')
        elif(self.actionName=="Settings"):
            self.createSubMenu(actionName, 9, 'Settings', None, 'settings.png')
        elif(self.actionName=="Exit"):
            self.createSubMenu(actionName, 19, 'Quit program', 'Ctrl+Q', 'exit.png')
    
    def handle_action(self, actionId):
        if actionId==0:
            self.openImage(self.parent)
        elif actionId==1:
            self.saveImage(self.parent)
        elif actionId==9:
            self.editSettings(self.parent)
        elif actionId==10:
            self.printImage(self.parent)
        elif actionId==19:
            self.close(self.parent)

    def openImage(self, parent):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened. 
        """
        image_file, _ = QFileDialog.getOpenFileName(parent, "Open Image",
            "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")

        if image_file:
            parent.image = QPixmap(image_file)

            parent.image_label.setPixmap(parent.image.scaled(parent.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            QMessageBox.information(parent, "Error", 
                "Unable to open image.", QMessageBox.Ok)

        #self.print_act.setEnabled(True)
    
    def saveImage(self, parent):
        """
        Save the image.
        Display error message if image can't be saved. 
        """
        image_file, _ = QFileDialog.getSaveFileName(parent, "Save Image",
            "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")

        if image_file and parent.image.isNull() == False:
            parent.image.save(image_file)
        else:
            QMessageBox.information(parent, "Error", 
                "Unable to save image.", QMessageBox.Ok)

    def printImage(self, parent):
        """
        Print image.
        """
        # create printer object and print output defined by the platform
        # the program is being run on. 
        # QPrinter.NativeFormat is the default
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat) 

        # Create printer dialog to configure printer
        print_dialog = QPrintDialog(printer)
        
        # if the dialog is accepted by the user, begin printing
        if (print_dialog.exec_() == QPrintDialog.Accepted):
            # use QPainter to output a PDF file 
            painter = QPainter()
            # begin painting device
            painter.begin(printer)
            # Set QRect to hold painter's current viewport, which 
            # is the image_label 
            rect = QRect(painter.viewport())
            # get the size of image_label and use it to set the size 
            # of the viewport
            size = QSize(parent.image_label.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(parent.image_label.pixmap().rect())
            # scale the image_label to fit the rect source (0, 0) 
            painter.drawPixmap(0, 0, parent.image_label.pixmap())
            # end painting
            painter.end()

    def editSettings(self, parent):
        print("edit Settings")
        dialog = SettingsDialog(parent, "Edit Settings")
        dialog.setFixedSize(600, 600)
        dialog.show()

class TestAction(QAction):
    def __init__(self, parent):
        super(TestAction, self).__init__("Test", parent)
        self.triggered.connect(self.open_file)

    def open_file(self):
        # Implement the logic to open a file here
        print("Open File action triggered")