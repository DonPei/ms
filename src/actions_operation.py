from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QDialog)
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from moviepy.editor import VideoFileClip
import numpy as np


from PIL import Image

import os
import time
import traceback, sys
from pathlib import Path

from PyQt5.QtCore import Qt, QThread, pyqtSignal

from dialogs_info import InfoDialog
from dialogs_led import LedDialog
from dialogs_motor import MotorDialog

#https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/

class OperationActions(QAction):
    def __init__(self, parent, actionName):
        root = Path(os.path.abspath(__file__)).parents[0]
        path_parent = Path(os.path.abspath(__file__)).parents[1]
        self.data_path = os.path.join(path_parent, 'examples')
        self.parent = parent
        self.actionName = actionName
        super().__init__("", parent)
        self.triggered.connect(self.handle_action)

        self.setText(actionName)
        if(self.actionName=="Board Info"):
            self.setStatusTip('Retrieve Ayduino board information')
        elif(self.actionName=="Control LED"):
            self.setStatusTip('Control LED')
        elif(self.actionName=="Control Step Motor"):
            self.setStatusTip('Control Step Motor')
        elif(self.actionName=="Scan"):
            self.setIcon(QIcon('images/open_file.png'))
            self.setShortcut('Ctrl+O')
            self.setStatusTip('Scan open stage')
        elif(self.actionName=="Move Left"):
            self.setIcon(QIcon('images/moveToLeft.png'))
            self.setShortcut('Ctrl+L')
            self.setStatusTip('Move one step to the left of the current position')
        elif(self.actionName=="Move Right"):
            self.setIcon(QIcon('images/moveToRight.png'))
            self.setShortcut('Ctrl+R')
            self.setStatusTip('Move one step to the right of the current position')
        elif(self.actionName=="Test"):
            self.setIcon(QIcon('images/moveToRight.png'))
            self.setShortcut('Ctrl+R')
            self.setStatusTip('Test')
    

    def handle_action(self):
        if(self.actionName=="Board Info"):
            self.boardInfo(self.parent)
        elif(self.actionName=="Control LED"):
            self.controlLed(self.parent)
        elif(self.actionName=="Control Step Motor"):
            self.controlStepMotor(self.parent)
        elif(self.actionName=="Scan"):
            self.scanStage(self.parent)
        elif(self.actionName=="Move Left"):
            self.moveToLeft(self.parent)
        elif(self.actionName=="Move Right"):
            self.moveToRight(self.parent)
        elif(self.actionName=="Test"):
            self.test(self.parent)
        
    def boardInfo(self, parent):
        print("Board")
        dialog = InfoDialog(parent, "Board Info")
        dialog.setFixedSize(800, 600)
        dialog.show()

    def controlLed(self, parent):
        print("Control LED")
        dialog = LedDialog(parent, "LED Control")
        dialog.setFixedSize(300, 200)
        dialog.show()
    
    def controlStepMotor(self, parent):
        print("Control Step Motor")
        dialog = MotorDialog(parent, "Step Motor Control")
        dialog.setFixedSize(1000, 700)
        dialog.show()
        
    def scanStage(self, parent):
        print("scan")
        worker = Worker(self.movieClipToImage) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.display_scan_results)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        parent.threadpool.start(worker)

    def moveToLeft(self, parent):
        print("moveToLeft")
    
    def moveToRight(self, parent):
        print("moveToRight")
    
    def progress_fn(self, n):
        count = n[0]
        array = n[1]
        #print("%d%% done" % count)
        self.update_pixmap(array, self.parent)

    def display_scan_results(self, n):
        count = n[0]
        array = n[1]
        print("Total count: %d" % (count))
        self.update_pixmap(array, self.parent)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def movieClipToImage(self, progress_callback):
        inputFileName = os.path.join(self.data_path, 'spidermanTrailer.mp4')
        clip = VideoFileClip(inputFileName)
        print('%s is %i fps, for %i seconds at %s' % (inputFileName, clip.fps, clip.duration, clip.size))
        #clip = clip.subclip(20, 30)
        #print('subclip is %i fps, for %i seconds at %s' % (clip.fps, clip.duration, clip.size))

        # np.zeros is how we generate an empty ndarray
        img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')

        currentX = 0
        slitwidth = 1

        slitpoint = clip.size[0] // 2

        # generate our target fps with width / duration
        target_fps = clip.size[0] / clip.duration

        for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
            if currentX < (clip.size[0] - slitwidth):
                img[:,currentX:currentX + slitwidth,:] = i[:,slitpoint:slitpoint+slitwidth,:]
            currentX += slitwidth
            #progress_callback.emit((currentX, img))
            if currentX%10==0:
                progress_callback.emit((currentX, img))
            #self.update_pixmap(img, parent)
        return (currentX, img)

    def update_pixmap(self, array, parent):
        parent = self.parent
        '''
        converts a NumPy array to a QPixmap object and update display
        '''
        height, width = array.shape[:2]
        bytes_per_line = 3 * width
        q_image = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        parent.image = QPixmap.fromImage(q_image)

        parent.image_label.setPixmap(parent.image.scaled(parent.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
    

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(tuple)
    progress = pyqtSignal(tuple)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
