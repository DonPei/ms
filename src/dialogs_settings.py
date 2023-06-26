import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect, QThreadPool
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QScrollArea, QFileDialog, QMessageBox, QWidget, QGridLayout, QLabel, QMenu 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QPushButton
import sys, random
from PyQt5.QtWidgets import QTabWidget, QMainWindow, QPushButton, QGridLayout, QWidget, QDialog, \
   QVBoxLayout, QGroupBox, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QListView, QRadioButton, \
   QCheckBox, QComboBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem

import json


class ContentWidget(QWidget):
    def __init__(self, parent, section: dict):
        super().__init__(parent)
        layout = QFormLayout(self)

        for key, value in section.items():
            layout.addRow(QLabel(key), value)

        self.setLayout(layout)
    
class ScrollWidget(QWidget):
    def __init__(self, parent, section: dict):
        super().__init__(parent)
        self.contentWidget = ContentWidget(parent, section)
        scroll = QScrollArea(self)
        scroll.setWidget(self.contentWidget)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def sizeHint(self) -> QSize:
        return self.contentWidget.sizeHint() + QSize(50, 0)
    
class SettingsDialog(QDialog):
    def __init__(self, parent=None, title="Custom Dialog"):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(title)

        parser = self.parent.config
        self.parser_dict = {}
        
        for section in parser.sections():
            temp_dict = {}
            for key, value in parser.items(section):
                lineEdit = QLineEdit(self)
                lineEdit.setText(value)
                temp_dict[key] = lineEdit
            self.parser_dict[section] = temp_dict

        tabWidget = QTabWidget(self)
        for section in parser.sections():
            tabWidget.addTab(ScrollWidget(self.parent, self.parser_dict[section]), section)

        mainVerticalLayout = QVBoxLayout(self)

        mainVerticalLayout.addWidget(tabWidget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        mainVerticalLayout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_changes)
             
        self.setLayout(mainVerticalLayout)
    
    def accept(self):
        self.apply_changes()
        super().accept()

    def reject(self):
        super().reject()

    def apply_changes(self):
        parser = self.parent.config
        self.parser_dict = {}

        for section, nested_dict in self.parser_dict.items():
            for key, value in nested_dict:
                parser.set(section, key, value.text())
        parser.save()


