import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter, QFont
from PyQt5.QtCore import Qt, QSize, QRect, QThreadPool
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QScrollArea, QFileDialog, QMessageBox, QWidget, QGridLayout, QLabel, QMenu 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QDialog, \
   QVBoxLayout, QGroupBox, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QListView, QRadioButton, \
   QCheckBox, QComboBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem


import asyncio
from threading import Thread
#Python asyncio event loop in a separate thread
#https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058

class LedDialog(QDialog):
    def __init__(self, parent=None, title="Custom Dialog"):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(title)
        self.led_worker = None
        
        self.thread = QThread()
        self.ctrl = {'break': False}
 
        mainVerticalLayout = QVBoxLayout(self)

        label = QLabel()
        label.setText("Click start to light LED.\nClick stop to stop LED.")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Arial', 12, QFont.Bold))

        mainVerticalLayout.addWidget(label)
        
        buttonBox = QDialogButtonBox()
        buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.clicked.connect(self.on_start_clicked)
        ok_button.setText("Start")
        cancel_button = buttonBox.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Stop")
        cancel_button.clicked.connect(self.on_stop_clicked)

        mainVerticalLayout.addWidget(buttonBox)
             
        self.setLayout(mainVerticalLayout)
    
    def start_background_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)

    def on_start_clicked(self):
        print("Start button clicked")
        board = self.parent.board
        if board == None:
            return
        self.ctrl['break'] = False
        loop = asyncio.new_event_loop()
        t = Thread(target=self.start_background_loop, args=(loop,), daemon=True)
        t.start()
    
    def on_stop_clicked(self):
        self.ctrl['break'] = True
        