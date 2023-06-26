import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect, QThreadPool
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QScrollArea, QFileDialog, QMessageBox, QWidget, QGridLayout, QLabel, QMenu 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QDialog, \
   QVBoxLayout, QGroupBox, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QListView, QRadioButton, \
   QCheckBox, QComboBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem


class InfoDialog(QDialog):
    def __init__(self, parent=None, title="Custom Dialog"):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(title)
 
        mainVerticalLayout = QVBoxLayout(self)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        self.text_edit = QTextEdit()
        #self.text_edit.setReadOnly(True)
        self.text_edit.setText("Information:")

        scroll_area.setWidget(self.text_edit)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mainVerticalLayout.addWidget(scroll_area)
        
        buttonBox = QDialogButtonBox()
        buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.setText("Fetch")
        mainVerticalLayout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.dialogAccepted)
             
        self.setLayout(mainVerticalLayout)
    
    def dialogAccepted(self):
        board = self.parent.board
        if board == None:
            return
        print("Board")

    def get_output(self):
        return self._output
    
    def dialogRejected(self):
        print("Exited dialog via cancel button or closing window")
        self.close()

