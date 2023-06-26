import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter, QFont
from PyQt5.QtCore import Qt, QSize, QRect, QThreadPool
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QScrollArea, QFileDialog, QMessageBox, QWidget, QGridLayout, QLabel, QMenu 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QStyle
import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QDialog, \
   QVBoxLayout, QGroupBox, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QListView, QRadioButton, \
   QCheckBox, QComboBox, QDialogButtonBox, QGraphicsItem
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
import asyncio
from threading import Thread
from MarianaThreadPool import Worker
#Python asyncio event loop in a separate thread
#https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058

#This sketch is a server for the telemetrix and telemetrix-aio Python clients.
#https://github.com/MrYsLab/Telemetrix4Arduino
#User Manual https://mryslab.github.io/telemetrix/

#telemetrix-aio API
#https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-aio/blob/master/html/telemetrix_aio/index.html
#source code
#https://github.com/MrYsLab/telemetrix-aio


import asyncio
import time
import os, sys

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QPen

class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)
        self.statusLabel = None

    # mouse hover event
    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def test(self, event):
        if event.buttons() == QtCore.Qt.NoButton:
            print("Simple mouse motion")
        elif event.buttons() == QtCore.Qt.LeftButton:
            print("Left click drag")
        elif event.buttons() == QtCore.Qt.RightButton:
            print("Right click drag")

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        self.updateMsg()

    def move(self, deltaX, deltaY):
        current_pos = self.pos()
        self.moveTo(current_pos.x()+deltaX, current_pos.y()+deltaY)
    
    def moveTo(self, x, y):
        self.setPos(QPointF(x, y))
        self.updateMsg()

    def mouseReleaseEvent(self, event):
        self.updateMsg()
    
    def setStatusLabel(self, statusLabel):
        self.statusLabel = statusLabel
    
    def updateMsg(self, msg=None):
        if msg:
            pass
        else: 
            msg = ('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        if self.statusLabel:
            self.statusLabel.setText(msg)
        else :
            print(msg)


class MotorDialog(QDialog):
    def __init__(self, parent=None, title="Custom Dialog"):
        super().__init__(parent)
        self.parent = parent
        self.board = parent.board
        
        self.setWindowTitle(title)
        self.motor_is_running = False
        self.ctrl = {'break': False}
 
        mainLayout = QGridLayout(self)

        iCol = 0
        iRow = 0
        nCol = 12
        label = self.createQLabel("Step Motor Control", QFont('Arial', 14, QFont.Bold))
        label.setFixedHeight(20)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainLayout.setRowStretch(iRow, 0)
        mainLayout.addWidget(label, iRow, iCol,1,nCol)

        iRow += 1
        mainLayout.setRowStretch(iRow, 1)

        iCol = 0
        iRow += 1
        mainLayout.setRowStretch(iRow, 0)
        label = self.createQLabel("X Axis", QFont('Arial', 12, QFont.Bold))
        mainLayout.addWidget(label, iRow, iCol,1,1)
        
        iCol += 1
        self.toLeftBtnX = self.createQPushButton('arrows_left.png', 1)
        mainLayout.addWidget(self.toLeftBtnX, iRow, iCol,1,1)
        
        iCol += 1
        self.toRightBtnX = self.createQPushButton('arrows_right.png', 10)
        mainLayout.addWidget( self.toRightBtnX, iRow, iCol,1,1)

        iCol = 0
        iRow += 1
        mainLayout.setRowStretch(iRow, 0)
        label = self.createQLabel("Y Axis", QFont('Arial', 12, QFont.Bold))
        mainLayout.addWidget(label, iRow, iCol,1,1)
        
        iCol += 1
        self.toLeftBtnY = self.createQPushButton('arrows_up.png', 20)
        mainLayout.addWidget(self.toLeftBtnY, iRow, iCol,1,1)
        
        iCol += 1
        self.toRightBtnY = self.createQPushButton('arrows_down.png', 30)
        mainLayout.addWidget( self.toRightBtnY, iRow, iCol,1,1)

        iCol = 0
        iRow += 1
        mainLayout.setRowStretch(iRow, 0)
        label = self.createQLabel("Z Axis", QFont('Arial', 12, QFont.Bold))
        mainLayout.addWidget(label, iRow, iCol,1,1)
        
        iCol += 1
        self.toLeftBtnZ = self.createQPushButton('arrows_left.png', 40)
        mainLayout.addWidget(self.toLeftBtnZ, iRow, iCol,1,1)
        
        iCol += 1
        self.toRightBtnZ = self.createQPushButton('arrows_right.png', 50)
        mainLayout.addWidget(self.toRightBtnZ, iRow, iCol,1,1)

        nRow = iRow
        iRow = 1
        iCol += 1
        graphics_view = QGraphicsView()
        graphics_scene = QGraphicsScene()
        graphics_view.setScene(graphics_scene)
        graphics_view.setSceneRect(0, 0, 600, 600)

        self.moveObject = MovingObject(50, 50, 40)
        horizontal_line = self.createQGraphicsLineItem(300-50, 300, 300+50, 300)
        graphics_scene.addItem(horizontal_line)
        vertical_line = self.createQGraphicsLineItem(300, 300-50, 300, 300+50)
        graphics_scene.addItem(vertical_line)
        graphics_scene.addItem(self.moveObject)
        mainLayout.addWidget(graphics_view, iRow, iCol,nRow+1,nCol-iCol)

        iRow = nRow+1
        mainLayout.setRowStretch(iRow, 1)

        iRow = nRow+2
        mainLayout.setRowStretch(iRow, 0)
        iCol = 0
        self.statusLabel = self.createQLabel("status", QApplication.font(), Qt.AlignRight)
        self.statusLabel.setFixedHeight(20)
        self.statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        mainLayout.addWidget(self.statusLabel, iRow, iCol ,1,nCol)

        self.moveObject.setStatusLabel(self.statusLabel)
             
        self.setLayout(mainLayout)
        
    def createQPushButton(self, iconFileName, actionId, iconSize=QtCore.QSize(50, 30)):
        b = QPushButton()
        b.setIcon(QIcon(os.path.join(self.parent.path_images, iconFileName)))
        b.setIconSize(iconSize)
        b.clicked.connect(lambda: self.move(actionId))
        return b
    
    def createQLabel(self, text, font=QApplication.font(), alignment=Qt.AlignCenter):
        label = QLabel()
        label.setText(text)
        label.setFont(font)
        label.setAlignment(alignment)
        return label
    
    def createQGraphicsLineItem(self, x1, y1, x2, y2):
        # Define the brush (fill).
        #brush = QBrush(Qt.red)
        #line.setBrush(brush)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        line.setFlag(QGraphicsItem.ItemIsMovable, False)
        line.setFlag(QGraphicsItem.ItemIsSelectable, False)
        return line

    def move(self, actionId):
        print(f'actionId={actionId} self.motor_is_running={self.motor_is_running}')
        board = self.parent.board
        if board == None:
            return
        
        if self.motor_is_running:
            return
        
        self.motor_is_running = True

        if self.moveObject:
            if actionId==1:
                self.moveObject.move(-10, 0)
            elif actionId==10:
                self.moveObject.move(10, 0)
            elif actionId==20:
                self.moveObject.move(0, 10)
            elif actionId==30:
                self.moveObject.move(0, -10)

        #loop = asyncio.new_event_loop()
        loop = asyncio.get_event_loop()
        worker = Worker(self.start_background_loop, loop, actionId=actionId)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        #worker.signals.progress.connect(self.progress_fn)
        self.parent.threadpool.start(worker)
    
    def start_background_loop(self, *args, **kwargs) -> None:
        loop = args[0]
        actionId = kwargs['actionId']
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.moveImpl(actionId))
        except asyncio.CancelledError:
            print("Async function was stopped programmatically.")

        
    async def moveImpl(self, actionId):
        print(f'actionId2={actionId} self.motor_is_running={self.motor_is_running}')
        motorIndex = 0
        if actionId>=1 and actionId<=19:
            motorIndex = 0
        elif actionId>=20 and actionId<=39:
            motorIndex = 1
        elif actionId>=40 and actionId<=59:
            motorIndex = 2
        test = False
        if test:
            stepPin = 6
            #12 6 4
            dirPin = 7
            #13 7 5
            motor = self.board.set_pin_mode_stepper(interface=1, pin1=stepPin, pin2=dirPin)
            time.sleep(.5)
            
            self.board.stepper_set_max_speed(motor, 400)
            self.board.stepper_set_acceleration(motor, 800)
            self.board.stepper_set_speed(motor, 400)
            #self.board.stepper_move_to(motor, 200)
        else:
            motor = self.parent.motors[motorIndex]

        if actionId==1:
            self.board.stepper_move(motor, 100)
        elif actionId==10:
            self.board.stepper_move(motor, -100)
        elif actionId==20:
            self.board.stepper_move(motor, 300)
        elif actionId==30:
            self.board.stepper_move(motor, -300)
        elif actionId==40:
            self.board.stepper_move(motor, 400)
        elif actionId==50:
            self.board.stepper_move(motor, -400)

        # run the motor
        #self.board.stepper_run_speed_to_position(motor, completion_callback=self.the_callback)
        self.board.stepper_run(motor, completion_callback=self.the_callback)
        #time.sleep(2)
    
    def the_callback(self, data):
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
        print(f'Motor {data[1]} runSpeedToPosition motion completed at: {date}.')

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        self.motor_is_running = False
        print(f'self.motor_is_running3={self.motor_is_running}')
        print("THREAD COMPLETE!")
    
    
    